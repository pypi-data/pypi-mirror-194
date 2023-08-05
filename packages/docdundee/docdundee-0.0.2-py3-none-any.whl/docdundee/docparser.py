from ctypes import ArgumentError
from os import path, makedirs
from typing import Dict, List, Tuple
import json
import ast
import inspect
from importlib import import_module

from docutils.core import publish_parts
from docstring_parser import parse

from docdundee.interfaces import (
    ExampleParam,
    ParsedDocstring,
    DocstringsDict,
    FileSourcesDict,
)


def parse_class(mod: str, cls: str, private=False, verbose=False) -> DocstringsDict:
    """Parse a class to a methods dict

    All the methods of the class will be parsed
    and the docstrings returned in a dict

    .. code-block:: python

      from docdundee.docparser import parse_class, parse_docstrings
      from docdundee.interfaces import DocstringsDict, ParsedDocstring

      parsed_methods: DocstringsDict = parse_class("mypackage.myfile", "MyClassName")
      docs: Dict[str, ParsedDocstring] = parse_docstrings(parsed_methods)

    :param mod: module import path
    :type mod: str
    :param cls: class name
    :type cls: str
    :param private: parse private function that start with _, defaults to False
    :type private: bool
    :return: a dict of methods
    :rtype: DocstringsDict
    """
    source = inspect.getsource(getattr(import_module(mod), cls))
    _mod = ast.parse(source)
    _cls = _mod.body[0]
    if not isinstance(_cls, ast.ClassDef):
        raise ArgumentError("Node is not a class")
    return _parse_nodes(source, _cls.body, private=private, verbose=verbose)  # type: ignore


def parse_functions(mod: str, private=False, verbose=False) -> DocstringsDict:
    """Parse a module's functions to a methods dict

    All the functions in the file will be parsed
    except the ones that start with and underscore.
    The docstrings are returned in a dict

    .. code-block:: python

      from docdundee.docparser import parse_functions, parse_docstrings
      from docdundee.interfaces import DocstringsDict, ParsedDocstring

      parsed_funcs: DocstringsDict = parse_functions("mypackage.myfile")
      docs: Dict[str, ParsedDocstring] = parse_docstrings(parsed_funcs)

    :param mod: module import path
    :type mod: str
    :param private: parse private function starting with _, defaults to False
    :type private: bool
    :return: a dict of methods
    :rtype: DocstringsDict
    """
    source = inspect.getsource(import_module(mod))
    _mod = ast.parse(source)
    return _parse_nodes(source, _mod.body, private=private, verbose=verbose)  # type: ignore


def get_func_sources(file: str) -> FileSourcesDict:
    """Get source code of all functions in a file

    .. code-block:: python

      from docdundee.interfaces import FileSourcesDict

      sources: FileSourcesDict = get_func_sources("some/path/file.py")

    :param file: the file path
    :type file: str
    :raises ModuleNotFoundError: source not found
    :return: a dict of functions and sources
    :rtype: FileSourcesDict
    """
    ex: ExamplesDict = {}  # type: ignore
    with open(file, "r") as fileop:
        lines = fileop.readlines()
        source = "".join(lines)
        _mod = ast.parse(source)
        i = 0
        for node in _mod.body:
            if (
                isinstance(node, ast.FunctionDef)
                or isinstance(node, ast.AsyncFunctionDef)
                or isinstance(node, ast.ClassDef)
            ):
                rawsource = ast.get_source_segment(source, _mod.body[i])  # type: ignore
                if rawsource is None:
                    raise ModuleNotFoundError("Source not found")
                lines = rawsource.split("\n")
                lines.pop(0)
                nlines = []
                for line in lines:
                    nl = line.replace("\t", "", 1)
                    nl = nl.replace("    ", "", 1)
                    nlines.append(nl)
                end = "\n".join(nlines)
                ex[node.name] = end
            i += 1
    return ex


def parse_docstrings(
    methods: DocstringsDict, exec_examples=False, parse_rst=False
) -> Dict[str, ParsedDocstring]:
    """Parse a list of preprocessed DocstringsDict docstring

    .. code-block:: python

      from docdundee.docparser import parse_functions, parse_docstrings
      from docdundee.interfaces import DocstringsDict, ParsedDocstring

      parsed_ds: DocstringsDict = parse_functions("mypackage.myfile")
      docs: Dict[str, ParsedDocstring] = parse_docstrings(parsed_ds)

    :param methods: the parsed methods
    :type methods: DocstringsDict
    :param exec_examples: set the examples as executable by default, defaults to False
    :type exec_examples: bool
    :return: a dict of parsed docstrings
    :rtype: Dict[str, ParsedDocstring]
    """
    docs: Dict[str, ParsedDocstring] = {}
    for k in methods.keys():
        params = {}
        raises = []
        method = methods[k]
        for param in method["docstring"].params:
            pdesc = param.description
            ptype = param.type_name
            pdefault = param.default
            if pdesc is not None:
                pdesc = _to_html(pdesc, parse_rst)
            if ptype is not None:
                ptype = _to_html(ptype, parse_rst)
            if pdefault is not None:
                pdefault = _to_html(pdefault, parse_rst)
            params[param.arg_name] = {
                "description": pdesc,
                "type": ptype,
                # "is_optional": param.is_optional,
                "default": pdefault,
            }
        for ex in method["docstring"].raises:
            raises.append({"description": ex.description, "type": ex.type_name})
        r = None
        if method["docstring"].returns is not None:
            r = {"name": "", "type": ""}
            rn = method["docstring"].returns.return_name
            if rn is not None:
                rn = _to_html(rn, parse_rst)
            rt = method["docstring"].returns.type_name
            if rt is not None:
                rt = _to_html(rt, parse_rst)
            r["name"] = rn
            r["type"] = rt
        # print("EX", k, method["docstring"].examples)
        desc, example, is_executable = _parse_long_description(
            method["docstring"].long_description, exec_examples
        )
        if desc is not None:
            desc = _to_html(desc, parse_rst)
        shortdesc = method["docstring"].short_description
        if shortdesc is not None:
            shortdesc = _to_html(shortdesc, parse_rst)
        _example: ExampleParam | None = None
        if example is not None:
            _example = {
                "code": example,
                "is_executable": is_executable,
            }
        docs[k] = {
            "funcdef": method["funcdef"],
            "description": shortdesc,
            "long_description": desc,
            "example": _example,
            "params": params,
            "raises": raises,
            "returns": r,
        }
    return docs


def write_docstrings(
    filepath: str, docstrings: Dict[str, ParsedDocstring], indent: int | None = None
):
    """Write the docstrings json to a file

    .. code-block:: python

      from docdundee.docparser import (
        parse_functions,
        parse_docstrings,
        write_docstrings
      )
      from docdundee.interfaces import DocstringsDict, ParsedDocstring

      parsed_funcs: DocstringsDict = parse_functions("mypackage.myfile")
      docs: ParsedDocstring = parse_docstrings(parsed_funcs)
      write_docstrings("../../docsite/src/assets/doc/api/index.json", doc, 4)

    :param filepath: the file path
    :type filepath: str
    :param json_data: the json data
    :type json_data: Dict[str, Any] | Array[Any]
    :param indent: the indentation level, defaults to None
    :type: int | None
    """
    makedirs(path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as filetowrite:
        filetowrite.write(json.dumps(docstrings, indent=indent))


def _to_html(txt: str, parse_rst: bool) -> str:
    if not parse_rst:
        return txt.replace("\n", "<br />")
    return publish_parts(
        txt,
        settings_overrides={"output_encoding": "unicode"},
        writer_name="html",
    )["body"]


def _parse_nodes(
    source: str, nodes: List[ast.AST], private=False, verbose=False
) -> DocstringsDict:
    i = 0
    methods: DocstringsDict = {}  # type: ignore
    for node in nodes:
        if (
            isinstance(node, ast.FunctionDef)
            or isinstance(node, ast.AsyncFunctionDef)
            or isinstance(node, ast.ClassDef)
        ):
            if private is False:
                if node.name.startswith("_"):
                    continue
            nodedef = ""
            if not isinstance(node, ast.ClassDef):
                if isinstance(node, ast.AsyncFunctionDef):
                    nodedef = "async def"
                elif isinstance(node, ast.FunctionDef):
                    nodedef = "def"
                nodedef += f" {node.name}"
                args_li = []
                for arg in node.args.args:
                    args_li.append(ast.unparse(arg))
                if node.args.vararg:
                    args_li.append("*" + ast.unparse(node.args.vararg))
                if node.args.kwarg:
                    args_li.append("**" + ast.unparse(node.args.kwarg))
                args = ",\n\t".join(args_li)
                nodedef += f"(\n\t{args}\n)"
                if node.returns:
                    nodedef += f" -> {ast.unparse(node.returns)}"
                if verbose is True:
                    print(nodedef)
            methods[node.name] = {
                "funcdef": nodedef,
                "docstring": parse(ast.get_docstring(node) or ""),
            }
        i += 1
    return methods


def _parse_long_description(
    desc: str | None, exec_examples: bool
) -> Tuple[str | None, str | None, bool]:
    if desc is None:
        return (None, None, False)
    sl = desc.split(".. code-block:: python\n\n")
    if len(sl) < 2:
        return (desc, None, False)
    _desc = sl[0]
    _ex = sl[1].replace("  ", "")
    execute = exec_examples
    if _ex.startswith("# exec"):
        execute = True
        _ex = _ex.replace("# exec\n", "")
    elif _ex.startswith("# noexec"):
        execute = False
        _ex = _ex.replace("# noexec\n", "")
    return (_desc, _ex, execute)
