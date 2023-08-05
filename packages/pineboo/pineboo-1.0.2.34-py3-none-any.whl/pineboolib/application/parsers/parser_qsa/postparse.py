#!/usr/bin/python3
"""
Simplify AST-XML structures for later generation of Python files.
"""
from importlib.machinery import ModuleSpec
from optparse import OptionParser
import os
import sys
import importlib
from xml.etree import ElementTree as ET
from xml.dom import minidom  # type: ignore
from pineboolib import logging
from pineboolib.application.parsers.parser_qsa import pytnyzer, flscriptparse
from typing import List, Type, Optional, Dict, Tuple, Any, Callable, cast, Iterable

STRICT_MODE = pytnyzer.STRICT_MODE
importlib.reload(pytnyzer)
pytnyzer.STRICT_MODE = STRICT_MODE

TreeData = Dict[str, Any]

LOGGER = logging.get_logger(__name__)

USEFUL_TOKENS = "ID,ICONST,FCONST,SCONST,CCONST,RXCONST".split(",")

KNOWN_PARSERS: Dict[str, Type["TagObjectBase"]] = {}
UNKNOWN_PARSERS = {}


def parse_for(*tag_names: str) -> Callable:
    """Decorate functions for registering tags."""
    global KNOWN_PARSERS

    def decorator(func: Type["TagObjectBase"]) -> Type["TagObjectBase"]:
        for tag_name in tag_names:
            KNOWN_PARSERS[tag_name] = func
        return func

    return decorator


def parse(tag_name: str, tree_data: TreeData) -> "TagObject":
    """Excecute registered function for given tagname on treedata."""
    global KNOWN_PARSERS, UNKNOWN_PARSERS
    if tag_name not in KNOWN_PARSERS:
        UNKNOWN_PARSERS[tag_name] = 1
        func = parse_unknown
    else:
        func = KNOWN_PARSERS[tag_name]
    return func(tag_name, tree_data)


def getxmltagname(tag_name: str) -> str:
    """Transform tag names."""
    if tag_name == "source":
        return "Source"
    elif tag_name == "funcdeclaration":
        return "Function"
    elif tag_name == "classdeclaration":
        return "Class"
    elif tag_name == "vardeclaration":
        return "Variable"
    else:
        return "Unknown.%s" % tag_name


class TagObjectBase:
    """Base class for registering tag processors."""

    tags: List[str] = []

    @classmethod
    def can_process_tag(cls, tagname: str) -> bool:
        """Return if tagname is in class known tags."""
        return tagname in cls.tags

    def __init__(self, tagname: str) -> None:
        """Create base object for processing tags."""
        self.astname = tagname

    def add_subelem(self, argn: int, subelem: "TagObject") -> None:
        """Abstract function for adding sub elements."""

    def add_value(self, argn: int, vtype: str, value: str) -> None:
        """Abstract function for adding values."""

    def add_other(self, argn: int, vtype: str, data: str) -> None:
        """Abstract function for adding other types of data."""


XML_CLASS_TYPES: List[Type[TagObjectBase]] = []


class TagObjectFactory(type):
    """Metaclass for registering tag processors."""

    def __init__(cls, name: str, bases: Any, dct: Any) -> None:
        """Register a new class as tag processor."""
        global XML_CLASS_TYPES
        if issubclass(cls, TagObjectBase):
            XML_CLASS_TYPES.append(cast(Type[TagObjectBase], cls))
        else:
            raise Exception("This metaclass must be used as a subclass of TagObjectBase")
        super().__init__(name, bases, dct)


class TagObject(TagObjectBase, metaclass=TagObjectFactory):
    """Process XML tags for simplification. Main class with shared functionality."""

    set_child_argn = False
    name_is_first_id = False
    debug_other = True
    adopt_childs_tags: List[str] = []
    omit_tags = ["empty"]
    callback_subelem: Dict[Type["TagObject"], str] = {}
    promote_child_if_alone = False

    @classmethod
    def tagname(self, tagname: str) -> str:
        """Return processed target tag name."""
        return self.__name__

    def __init__(self, tagname: str) -> None:
        """Create new processor."""
        super().__init__(tagname)
        self.xml = ET.Element(self.tagname(tagname))
        self.xmlname: Optional[str] = None
        self.subelems: List[Any] = []
        self.values: List[Tuple[str, str]] = []
        if self.name_is_first_id:
            self.xml.set("name", "")

    def adopt_children(self, argn: int, subelem: "TagObject"):
        """Simplify tree by "merging" childs into itself."""
        for child in list(subelem.xml):
            if self.set_child_argn:
                child.set("argn", str(argn))
            else:
                if "argn" in child.attrib:
                    del child.attrib["argn"]
            self.xml.append(child)

    def omit_subelem(self, argn: int, subelem: "TagObject"):
        """Abstract function. Simplifies XML by removing unwanted terms."""
        return

    def is_in(self, listobj: Iterable) -> bool:
        """Return if the class type appears in any of the items."""
        return self.__class__ in listobj or self.astname in listobj

    def get(self, listobj: Dict[Any, str], default=None) -> Any:
        """Retrieve value from list based on this class type."""
        if self.__class__ in listobj:
            return listobj[self.__class__]
        if self.astname in listobj:
            return listobj[self.astname]
        return default

    def add_subelem(self, argn: int, subelem: "TagObject") -> None:
        """Add a new XML child."""
        if subelem.is_in(self.omit_tags):
            return self.omit_subelem(argn, subelem)
        if subelem.is_in(self.adopt_childs_tags):
            return self.adopt_children(argn, subelem)
        callback = subelem.get(self.callback_subelem)
        if callback:
            return getattr(self, callback)(argn, subelem)

        if self.set_child_argn:
            subelem.xml.set("argn", str(argn))
        self.xml.append(subelem.xml)
        self.subelems.append(subelem)

    def add_value(self, argn: int, vtype: str, value: str) -> None:
        """Add a new XML value."""
        self.values.append((vtype, value))
        if vtype == "ID" and self.name_is_first_id and self.xmlname is None:
            self.xmlname = value
            self.xml.set("name", value)
            return

        self.xml.set("arg%02d" % argn, vtype + ":" + repr(value))

    def add_other(self, argn: int, vtype: str, data: str) -> None:
        """Add extra data to XML."""
        if self.debug_other:
            self.xml.set("arg%02d" % argn, vtype)

    def polish(self) -> "TagObject":
        """Clean up the structure by removing or merging some data."""
        if self.promote_child_if_alone:
            if len(self.values) == 0 and len(self.subelems) == 1:
                return self.subelems[0]
        return self


class ListObject(TagObject):
    """Base class for list objects."""

    set_child_argn = False
    debug_other = False


class NamedObject(TagObject):
    """Base class for objects with names."""

    name_is_first_id = True
    debug_other = False


class ListNamedObject(TagObject):
    """Base class for list objects with names."""

    name_is_first_id = True
    set_child_argn = False
    debug_other = False


class TypedObject(ListObject):
    """Base class for typed objects."""

    type_arg = 0

    def add_other(self, argn, vtype, value):
        """Add extra data to XML."""
        if argn == self.type_arg:
            self.xml.set("type", vtype)


class Source(ListObject):
    """Process Source tags."""

    tags = ["source", "basicsource", "classdeclarationsource", "statement_list", "statement_block"]
    adopt_childs_tags = ["source_element", "statement_list", "statement", "statement_block"]


class Identifier(NamedObject):
    """Process Identifier tags."""

    tags = ["identifier", "optid"]

    def polish(self):
        """Fix astname attribute."""
        if self.xmlname is None:
            self.astname = "empty"
        return self


class Arguments(ListObject):
    """Process Argument tags."""

    tags = ["arglist"]
    adopt_childs_tags = ["vardecl_list"]


class VariableType(NamedObject):
    """Process VariableType tags."""

    tags = ["optvartype"]

    def polish(self):
        """Fix astname attribute."""
        if self.xmlname is None:
            self.astname = "empty"
        return self


class ExtendsType(NamedObject):
    """Process ExtendsType tags."""

    tags = ["optextends"]

    def polish(self):
        """Fix astname attribute."""
        if self.xmlname is None:
            self.astname = "empty"
        return self


class Function(ListNamedObject):
    """Process Function tags."""

    tags = ["funcdeclaration"]
    callback_subelem = ListNamedObject.callback_subelem.copy()
    callback_subelem[VariableType] = "add_vartype"

    def add_vartype(self, argn, subelem):
        """Add returns notation."""
        self.xml.set("returns", str(subelem.xmlname))


class FunctionAnon(ListObject):
    """Process FunctionAnon tags."""

    tags = ["funcdeclaration_anon"]


class FunctionAnonExec(ListObject):
    """Process FunctionAnonExec tags."""

    tags = ["funcdeclaration_anon_exec"]


class Variable(NamedObject):
    """Process Variable tags."""

    tags = ["vardecl"]
    callback_subelem = NamedObject.callback_subelem.copy()
    callback_subelem[VariableType] = "add_vartype"

    def add_vartype(self, argn, subelem):
        """Add type notation."""
        self.xml.set("type", str(subelem.xmlname))


class DeclarationBlock(ListObject):
    """Process DeclarationBlock tags."""

    tags = ["vardeclaration"]
    adopt_childs_tags = ["vardecl_list"]

    def add_other(self, argn, vtype, value):
        """Add debug info."""
        if argn == 0:
            self.xml.set("mode", vtype)

    def polish(self):
        """Cleanup."""
        # if len(self.values) == 0 and len(self.subelems) == 1:
        #    self.subelems[0].xml.set("mode",self.xml.get("mode"))
        #    return self.subelems[0]
        return self


class Class(ListNamedObject):
    """Process Class tags."""

    tags = ["classdeclaration"]
    callback_subelem = ListNamedObject.callback_subelem.copy()
    callback_subelem[ExtendsType] = "add_exttype"

    def add_exttype(self, argn, subelem):
        """Add extends notation."""
        self.xml.set("extends", str(subelem.xmlname))


class Member(TagObject):
    """Process Member tags."""

    debug_other = False
    set_child_argn = False
    tags = ["member_var", "member_call"]
    adopt_childs_tags = ["varmemcall", "member_var", "member_call"]


class ArrayMember(TagObject):
    """Process ArrayMember tags."""

    debug_other = False
    set_child_argn = False
    tags = ["array_member"]
    adopt_childs_tags = ["variable_1", "func_call"]


class InstructionCall(TagObject):
    """Process InstructionCall tags."""

    debug_other = False
    tags = ["callinstruction"]


class InstructionStore(TagObject):
    """Process InstructionStore tags."""

    promote_child_if_alone = True
    debug_other = False
    tags = ["storeinstruction"]


class InstructionFlow(TypedObject):
    """Process InstructionFlow tags."""

    debug_other = True
    tags = ["flowinstruction"]


class Instruction(TagObject):
    """Process Instruction tags."""

    promote_child_if_alone = True
    debug_other = False
    tags = ["instruction"]


class OpMath(TypedObject):
    """Process OpMath tags."""

    debug_other = True
    tags = ["mathoperator"]


class Compare(TypedObject):
    """Process Compare tags."""

    debug_other = True
    tags = ["cmp_symbol", "boolcmp_symbol"]


class FunctionCall(NamedObject):
    """Process FunctionCall tags."""

    tags = ["funccall_1"]


class CallArguments(ListObject):
    """Process CallArguments tags."""

    tags = ["callargs"]


class Constant(ListObject):
    """Process Constant tags."""

    tags = ["constant"]

    def add_value(self, argn: int, vtype: str, value: str) -> None:
        """Add value notation."""
        value = str(value)  # str(value,"ISO-8859-15","replace")
        if vtype == "SCONST":
            vtype = "String"
            value = value[1:-1]
            self.xml.set("delim", '"')
        if vtype == "CCONST":
            vtype = "String"
            value = value[1:-1]
            self.xml.set("delim", "'")
        if vtype == "RCONST":
            vtype = "Regex"
        if vtype == "ICONST":
            vtype = "Number"
        if vtype == "FCONST":
            vtype = "Number"
        self.const_value = value
        self.const_type = vtype
        self.xml.set("type", vtype)
        self.xml.set("value", value)


class InlineUpdate(ListObject):
    """Process InlineUpdate tags."""

    tags = ["inlinestoreinstruction"]

    def add_other(self, argn, vtype, value):
        """Add debug info."""
        self.xml.set("type", vtype)
        if argn == 0:
            self.xml.set("mode", "update-read")
        if argn == 1:
            self.xml.set("mode", "read-update")


class If(ListObject):
    """Process If tags."""

    tags = ["ifstatement"]


class Condition(ListObject):
    """Process Condition tags."""

    tags = ["condition"]


class TypeOf(ListObject):
    """Process Typeof_operator tags."""

    tags = ["typeof_operator"]


class Else(ListObject):
    """Process Else tags."""

    tags = ["optelse"]

    def polish(self):
        """Fix astname."""
        if len(self.subelems) == 0:
            self.astname = "empty"
        return self


class DictObject(ListObject):
    """Process DictObject tags."""

    tags = ["dictobject_value_elemlist", "dictobject_value"]
    adopt_childs_tags = ["dictobject_value_elemlist", "dictobject_value"]


class DictElem(ListObject):
    """Process DictElem tags."""

    tags = ["dictobject_value_elem"]


class ExpressionContainer(ListObject):
    """Process ExpressionContainer tags."""

    tags = ["expression"]
    # adopt_childs_tags = ['base_expression']

    def polish(self):
        """Fix internal expressions."""
        if len(self.values) == 0 and len(self.subelems) == 1:
            # if isinstance(self.subelems[0], Constant):
            if self.subelems[0].xml.tag == "base_expression":
                self.subelems[0].xml.tag = "Expression"
                return self.subelems[0]
            else:
                self.xml.tag = "Value"

        return self


class InstructionUpdate(ListObject):
    """Process InstructionUpdate tags."""

    tags = ["updateinstruction"]


class Switch(ListObject):
    """Process Switch tags."""

    tags = ["switch"]
    adopt_childs_tags = ["case_cblock_list", "case_block_list"]


class CaseList(ListObject):
    """Process CaseList tags."""

    tags = ["case_block_list"]
    adopt_childs_tags = ["case_cblock_list", "case_block_list"]


class Case(ListObject):
    """Process ExtendsType tags."""

    tags = ["case_block"]


class CaseDefault(ListObject):
    """Process CaseDefault tags."""

    tags = ["case_default"]


class While(ListObject):
    """Process While tags."""

    tags = ["whilestatement"]


class For(ListObject):
    """Process For tags."""

    tags = ["forstatement"]


class ForInitialize(ListObject):
    """Process ForInitialize tags."""

    tags = ["for_initialize"]


class ForCompare(ListObject):
    """Process ExtendsType tags."""

    tags = ["for_compare"]


class ForIncrement(ListObject):
    """Process ExtendsType tags."""

    tags = ["for_increment"]


class DoWhile(ListObject):
    """Process DoWhile tags."""

    tags = ["dowhilestatement"]


class ForIn(ListObject):
    """Process ExtendsType tags."""

    tags = ["forinstatement"]


class With(ListObject):
    """Process ExtendsType tags."""

    tags = ["withstatement"]


class TryCatch(ListObject):
    """Process TryCatch tags."""

    tags = ["trycatch"]


class New(ListObject):
    """Process New tags."""

    tags = ["new_operator"]


class Delete(ListObject):
    """Process Delete tags."""

    tags = ["deleteinstruction"]


class Parentheses(ListObject):
    """Process ExtendsType tags."""

    tags = ["parentheses"]
    adopt_childs_tags = ["base_expression"]


class OpUnary(TypedObject):
    """Process OpUnary tags."""

    tags = ["unary_operator"]


class OpTernary(ListObject):
    """Process OpTernary tags."""

    tags = ["ternary_operator"]


class OpUpdate(TypedObject):
    """Process OpUpdate tags."""

    tags = ["updateoperator"]


# ----- keep this one at the end.
class Unknown(TagObject):
    """Process Unknown tags."""

    promote_child_if_alone = True
    set_child_argn = False

    @classmethod
    def tagname(self, tagname):
        """Just return tagname."""
        return tagname

    @classmethod
    def can_process_tag(self, tagname):
        """Just return true."""
        return True


# -----------------


def create_xml(tagname) -> Optional[TagObject]:
    """Create processor for tagname by inspecting first known processor that fits."""
    classobj = None
    for cls in XML_CLASS_TYPES:
        if cls.can_process_tag(tagname):
            classobj = cls
            break
    if classobj is None:
        return None
    if issubclass(classobj, TagObject):
        return classobj(tagname)
    else:
        raise ValueError("Unexpected class %s" % classobj)


def parse_unknown(tagname, treedata):
    """Parse anything and error handling."""
    xmlelem = create_xml(tagname)
    if xmlelem is None:
        raise Exception("No class for parsing tagname %s" % tagname)

    position = 0
    for key, value in treedata["content"]:
        if type(value) is dict:
            instruction = parse(key, value)
            xmlelem.add_subelem(position, instruction)
        elif key in USEFUL_TOKENS:
            xmlelem.add_value(position, key, value)
        else:
            xmlelem.add_other(position, key, value)
        position += 1

    return xmlelem.polish()


def post_parse(treedata: TreeData):
    """Parse a xml. Convenience function."""
    source = parse("source", treedata)
    # print UNKNOWN_PARSERS.keys()
    return source.xml


class Module(object):
    """Python code tester for pineboo-parse."""

    def __init__(self, name: str, path: str) -> None:
        """Create Module."""
        self.name = name
        self.path = path

    def loadModule(self):
        """Import and return Python file."""
        try:
            from importlib import util

            module_name = self.name[: self.name.find(".")]
            script_name = os.path.join(self.path, self.name)
            spec: Optional["ModuleSpec"] = util.spec_from_file_location(module_name, script_name)
            if spec and spec.loader is not None:
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)  # type: ignore [attr-defined]
                self.module = module
            else:
                raise Exception(
                    "Module named %s can't be loaded from %s" % (module_name, script_name)
                )

            result = True

        except FileNotFoundError:
            LOGGER.error("Fichero %r no encontrado" % self.name)
            result = False
        except Exception:
            LOGGER.exception("Unexpected exception on loadModule")
            result = False

        return result


def parse_args(argv: List[str]) -> Tuple[Any, List[str]]:
    """Define parsing arguments for the program."""
    parser = OptionParser()
    parser.add_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        default=True,
        help="don't print status messages to stdout",
    )

    parser.add_option(
        "--optdebug",
        action="store_true",
        dest="optdebug",
        default=False,
        help="debug optparse module",
    )

    parser.add_option(
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="prints lots of useless messages",
    )

    parser.add_option("--path", dest="storepath", default=None, help="store XML results in PATH")

    parser.add_option(
        "--topython",
        action="store_true",
        dest="topython",
        default=False,
        help="write python file from xml",
    )

    parser.add_option(
        "--exec-py",
        action="store_true",
        dest="exec_python",
        default=False,
        help="try to execute python file",
    )

    parser.add_option(
        "--toxml", action="store_true", dest="toxml", default=False, help="write xml file from qs"
    )

    parser.add_option(
        "--full", action="store_true", dest="full", default=False, help="write xml file from qs"
    )

    parser.add_option(
        "--cache",
        action="store_true",
        dest="cache",
        default=False,
        help="If dest file exists, don't regenerate it",
    )

    parser.add_option(
        "--strict",
        action="store_true",
        dest="strict",
        default=False,
        help="Enable STRICT_MODE on pytnyzer",
    )

    parser.add_option(
        "--python-ext",
        dest="python_ext",
        default=".qs.py",
        help="Change Python file extension (default: '.qs.py')",
    )

    (options, args) = parser.parse_args(argv)
    return (options, args)


def main() -> None:
    """Run the program from command line."""
    pytnyzer.STRICT_MODE = True
    log_format = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"
    logging.basicConfig(format=log_format, level=0)
    blib_logger = logging.get_logger("blib2to3.pgen2.driver")
    blib_logger.setLevel(logging.WARNING)

    options, args = parse_args(sys.argv[1:])
    execute(options, args)


def pythonify(filelist: List[str], arguments: List[str] = []) -> None:
    """Convert to python the files included in the list."""
    if not isinstance(filelist, list):
        raise ValueError("First argument must be a list")
    options, args = parse_args(arguments)
    options.full = True
    execute(options, filelist)


def pythonify2(filename: str, known_refs: Dict[str, Tuple[str, str]] = {}) -> str:
    """Convert File to Python. Faster version as does not write to disk. Avoids re-parsing XML."""
    file_ = open(filename, "r", encoding="latin-1")
    filecontent = file_.read()
    file_.close()
    ast = common_parse(filecontent)
    return pytnyzer.pythonize2(ast, known_refs)


def pythonify_string(
    qs_code: str,
    known_refs: Dict[str, Tuple[str, str]] = {},
    parser_template: str = "expression_template",
) -> str:
    """Convert QS string to Python. For unit-testing, only evaluates expressions."""

    ast = common_parse(qs_code)
    ast.set("parser-template", parser_template)  # type: ignore [attr-defined] # noqa: F821
    return pytnyzer.pythonize2(ast, known_refs)


def common_parse(data: str):
    """Run common parse code."""

    prog = flscriptparse.parse(data)
    if not prog:
        raise Exception("Parse failed")
    if prog["error_count"] > 0:
        raise Exception("Found %d errors parsing string" % (prog["error_count"]))

    tree_data: TreeData = flscriptparse.calctree(prog, alias_mode=0)
    return post_parse(tree_data)


def execute(options: Any, args: List[str]) -> None:
    """Execute conversion orders given by options and args. Can be used to emulate program calls."""

    pytnyzer.STRICT_MODE = options.strict

    if options.full:
        execpython = options.exec_python
        options.exec_python = False
        options.full = False
        options.toxml = True
        LOGGER.info("Pass 1 - Parse and write XML file . . .")
        try:
            execute(options, args)
        except Exception:
            LOGGER.exception("Error parseando:")

        options.toxml = False
        options.topython = True
        LOGGER.info("Pass 2 - Pythonize and write PY file . . .")
        try:
            execute(options, [arg + ".xml" for arg in args])
        except Exception:
            LOGGER.exception("Error convirtiendo:")

        if execpython:
            options.exec_python = execpython
            LOGGER.info("Pass 3 - Test PY file load . . .")
            options.topython = False
            try:
                execute(
                    options,
                    [(arg + ".xml.py").replace(".qs.xml.py", options.python_ext) for arg in args],
                )
            except Exception:
                LOGGER.exception("Error al ejecutar Python:")
        LOGGER.debug("Done.")

    elif options.exec_python:
        # import qsatype
        for filename in args:
            realpath = os.path.realpath(filename)
            path, name = os.path.split(realpath)
            if not os.path.exists(realpath):
                LOGGER.error("Fichero no existe: %s" % name)
                continue

            mod = Module(name, path)
            if not mod.loadModule():
                LOGGER.error("Error cargando modulo %s" % name)

    elif options.topython:
        import io

        if options.cache:
            args = [
                x
                for x in args
                if not os.path.exists((x + ".py").replace(".qs.xml.py", options.python_ext))
                or os.path.getmtime(x)
                > os.path.getctime((x + ".py").replace(".qs.xml.py", options.python_ext))
            ]

        nfs = len(args)
        for nf_, filename in enumerate(args):
            bname = os.path.basename(filename)
            if options.storepath:
                destname = os.path.join(options.storepath, bname + ".py")
            else:
                destname = filename + ".py"
            destname = destname.replace(".qs.xml.py", options.python_ext)
            if not os.path.exists(filename):
                LOGGER.error("Fichero %r no encontrado" % filename)
                continue
            LOGGER.debug(
                "Pythonizing File: %-35s . . . .        (%.1f%%)"
                % (bname, 100.0 * (nf_ + 1.0) / nfs)
            )
            old_stderr = sys.stdout
            stream = io.StringIO()
            sys.stdout = stream
            try:
                pytnyzer.pythonize(filename, destname, destname + ".debug")
            except Exception:
                LOGGER.exception("Error al pythonificar %r:" % filename)
            sys.stdout = old_stderr
            text = stream.getvalue()
            if len(text) > 2:
                LOGGER.info("%s: " % bname + ("\n%s: " % bname).join(text.splitlines()))

    else:
        if options.cache:
            args = [
                x
                for x in args
                if not os.path.exists(x + ".xml")
                or os.path.getmtime(x) > os.path.getctime(x + ".xml")
            ]
        nfs = len(args)
        for nf_, filename in enumerate(args):
            bname = os.path.basename(filename)
            LOGGER.debug(
                "Parsing File: %-35s . . . .        (%.1f%%)" % (bname, 100.0 * (nf_ + 1.0) / nfs)
            )
            try:
                file_ = open(filename, "r", encoding="latin-1")
                filecontent = file_.read()
                file_.close()
            except Exception:
                LOGGER.exception("Error: No se pudo abrir fichero %s", filename)
                continue
            prog = flscriptparse.parse(filecontent)
            if not prog:
                LOGGER.error("Error: No se pudo abrir %s" % (repr(filename)))
                continue
            if prog["error_count"] > 0:
                LOGGER.error(
                    "Encontramos %d errores parseando: %-35s"
                    % (prog["error_count"], repr(filename))
                )
                continue
            if not options.toxml:
                # Si no se quiere guardar resultado, no hace falta calcular mas
                continue

            tree_data = None
            try:
                tree_data = flscriptparse.calctree(prog, alias_mode=0)
            except Exception:
                LOGGER.exception("Error al convertir a XML %r:" % bname)

            if not tree_data:
                LOGGER.error("No se pudo parsear %s" % (repr(filename)))
                continue
            ast = post_parse(tree_data)
            if ast is None:
                LOGGER.error("No se pudo analizar %s" % (repr(filename)))
                continue
            if options.storepath:
                destname = os.path.join(options.storepath, bname + ".xml")
            else:
                destname = filename + ".xml"

            xml_str = minidom.parseString(ET.tostring(ast)).toprettyxml(indent="   ")
            file_ = open(destname, "w", encoding="UTF-8")
            file_.write(xml_str)
            file_.close()


if __name__ == "__main__":
    main()
