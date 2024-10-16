from abc import ABC, abstractmethod

from common import Field, Method, SourceGenContext
import constants
from parse import *
from common import *
from parse import Field, Method

class JsBindingsWriter(HighLevelCodeWriter):
    #region Metadata
    def write_start(self):
        self.writer.write("/* AUTO GENERATED CODE */")
        self.writer.writeline().writeline()

    def write_end(self):
        pass
    #endregion

    #region Methods
    def write_method(self, method: Method, arguments: tuple[MethodArgument, ...], *, optionals_included: bool):
        method_name: str = js_method_name(self.ctx, method, optionals_included=optionals_included)

        self.writer.write(f"export function {method_name}(obj")
        for arg in arguments:
            self.writer.write(', ').write(arg.name)
        self.writer.write(") {")

        self.writer.writeline()
        self.writer.indent += 1

        self.writer.write("obj.").write(method.name).write('(')
        self.writer.write(", ".join(a.name for a in arguments))
        self.writer.write(");")

        self.writer.writeline()
        self.writer.indent -= 1
        self.writer.writeline('}')

        self.writer.writeline()
    #endregion

    #region Properties
    def write_property_start(self, property: Field):
        pass

    def write_getter(self, property: Field):
        self.writer.write(f"export function {js_getter_name(self.ctx, property)}(obj) {{")

        self.writer.writeline()
        self.writer.indent += 1

        self.writer.write(f"return obj.{property.name};")

        self.writer.writeline()
        self.writer.indent -= 1
        self.writer.writeline('}')

    def write_setter(self, property: Field):
        self.writer.write(f"export function {js_setter_name(self.ctx, property)}(obj, value) {{")

        self.writer.writeline()
        self.writer.indent += 1

        self.writer.write(f"obj.{property.name} = value;")

        self.writer.writeline()
        self.writer.indent -= 1
        self.writer.writeline('}')

    def write_property_end(self):
        self.writer.writeline()
    #endregion

class CsBindingsWriter(HighLevelCodeWriter):
    #region Metadata
    def write_start(self):
        self.writer.write("/* AUTO GENERATED CODE */")
        self.writer.writeline().writeline()

        self.writer.writeline("using System.Runtime.InteropServices.JavaScript;")
        self.writer.writeline()

        self.writer.writeline(f"namespace {constants.CS_NAMESPACE};")
        self.writer.writeline()

        self.writer.writeline("[System.Runtime.Versioning.SupportedOSPlatform(\"browser\")]")
        self.writer.writeline(f"internal partial class {self.ctx.interface_name}Bindings")
        self.writer.writeline("{")

        self.writer.indent += 1

    def write_end(self):
        self.writer.indent -= 1
        self.writer.writeline("}")
    #endregion

    #region Methods
    def write_method(self, method: Method, arguments: tuple[MethodArgument, ...], *, optionals_included: bool):
        cs_name: str = cs_method_name(method)
        js_name: str = js_method_name(self.ctx, method, optionals_included=optionals_included)

        self._write_method(cs_name=cs_name, js_name=js_name, arguments=arguments, returns=method.type)
        self.writer.writeline()
    #endregion

    #region Properties
    def write_property_start(self, property: Field):
        pass

    def write_getter(self, property: Field):
        cs_name: str = cs_property_name(property, getter=True)
        js_name: str = js_getter_name(self.ctx, property)

        self._write_method(cs_name=cs_name, js_name=js_name, arguments=(), returns=property.type)

    def write_setter(self, property: Field):
        cs_name: str = cs_property_name(property, setter=True)
        js_name: str = js_setter_name(self.ctx, property)
        arg: MethodArgument = MethodArgument("value", property.type, optional=False)

        self._write_method(cs_name=cs_name, js_name=js_name, arguments=(arg,), returns=SingleType("void"))

    def _write_method(self, *, cs_name: str, js_name: str, arguments: tuple[MethodArgument, ...], returns: Type):
        self.writer.writeline(f"[JSImport(\"{js_name}\", \"{constants.JS_MODULE_NAME}\")]")
        self.writer.write(f"public static partial {cs_marshaled_type(self.ctx, returns)} {cs_name}(JSObject obj")

        for arg in arguments:
            self.writer.write(", ") # we have obj as the first argument so we can just start passing the rest with a comma

            self.writer.write(cs_marshaled_type(self.ctx, arg.type))
            self.writer.write(' ')
            self.writer.write(arg.name)

        self.writer.writeline(");")

    def write_property_end(self):
        self.writer.writeline()
    #endregion

def generate(ctx: SourceGenContext, writer_type: type[HighLevelCodeWriter]) -> str:
    writer: Final[HighLevelCodeWriter] = writer_type(ctx)

    writer.write_start()
    for member in ctx.members:
        if isinstance(member, Method):
            _generate_method(writer, member)
        elif isinstance(member, Field):
            _generate_property(writer, member)
    writer.write_end()

    return writer.tostring()

def _generate_method(writer: HighLevelCodeWriter, method: Method):
    no_optional_arguments: tuple[MethodArgument, ...] = tuple(
        arg for arg in method.arguments if (not arg.optional)
    )
    writer.write_method(method, no_optional_arguments, optionals_included=False)
    if len(no_optional_arguments) != len(method.arguments):
        writer.write_method(method, method.arguments, optionals_included=True)

def _generate_property(writer: HighLevelCodeWriter, property: Field):
    writer.write_property_start(property)

    writer.write_getter(property)
    if not property.readonly:
        writer.write_setter(property)

    writer.write_property_end()

def js_method_name(ctx: SourceGenContext, method: Method, *, optionals_included: bool):
    opt: str = "_opt" if optionals_included else ""
    return f"{ctx.interface_name}_method_{method.name}{opt}"

def js_getter_name(ctx: SourceGenContext, property: Field) -> str:
    return f"{ctx.interface_name}_property_get_{property.name}"

def js_setter_name(ctx: SourceGenContext, property: Field) -> str:
    return f"{ctx.interface_name}_property_set_{property.name}"

def _capitalize_first_letter(input: str) -> str:
    return input[0].upper() + input[1:]

def cs_method_name(method: Method):
    return _capitalize_first_letter(method.name)

def cs_property_name(property: Field, *, getter: bool = False, setter: bool = False):
    if getter and setter:
        raise ValueError("Property cannot be both getter and setter.")

    parts: list[str] = property.name.split('_')
    name: str = ''.join(_capitalize_first_letter(part) for part in parts)

    if getter:
        name = "Get" + name
    if setter:
        name = "Set" + name

    return name

def cs_marshaled_type(ctx: SourceGenContext, type: Type) -> str:
    return _cs_type(ctx, type, marshaled=True)

def cs_converted_type(ctx: SourceGenContext, type: Type) -> str:
    return _cs_type(ctx, type, marshaled=False)

def _cs_type(ctx: SourceGenContext, type: Type, *, marshaled: bool) -> str:
    if isinstance(type, SingleType):
        return _cs_type_rune(ctx, type.type, marshaled=marshaled)
    elif isinstance(type, UnionType):
        raise ValueError(f"Unions are not supported by neither C# nor C#/JS marshaling. Tried to resolve type for: {type}")
    elif isinstance(type, StringEnum):
        raise ValueError("Cannot fetch StringEnum name using type.\nPlease resolve the type earlier in the source generation phase when the enum name is also known.")
    elif isinstance(type, ArrayType):
        return _cs_type(ctx, type.elements_type, marshaled=marshaled) + "[]"
    else: # StringConstant and NullType shouldn't exist without a parent type....... ?
        raise NotImplementedError(type)

def _csgen_type(name: str, value: Interface | StringEnum, *, marshaled: bool) -> str:
    if not marshaled:
        return name
    else:
        if isinstance(value, StringEnum):
            return "string"
        else:
            assert isinstance(value, Interface)
            return "JSObject"

def _cs_type_rune(ctx: SourceGenContext, typename: str, *, marshaled: bool) -> str:
    if typename in constants.ts2cs_translationtable:
        return constants.ts2cs_translationtable[typename]
    elif typename in ctx.generate_csharp:
        return _csgen_type(typename, ctx.generate_csharp[typename], marshaled=marshaled)
    else:
        print(f"No known C# type for: '{typename}'")
        return typename
