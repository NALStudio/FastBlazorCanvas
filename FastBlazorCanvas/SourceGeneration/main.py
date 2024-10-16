import os
from typing import Final, Generic, TypeVar
import generate_bindings
from parse import *
from common import *
import constants

resolve_should_be_skipped: Final[frozenset[str]] = constants.do_not_resolve.union(constants.ts2cs_translationtable.keys())

T = TypeVar("T")

@dataclass(frozen=True)
class DependencyTracked(Generic[T]):
    value: T
    depended_by: list[str]

class MessageGeneratingError(Exception, ABC):
    @abstractmethod
    def generate_msg(self) -> str:
        pass

class ForbiddenTypeError(MessageGeneratingError):
    def __init__(self, type: str) -> None:
        self.type: Final[str] = type

    def generate_msg(self) -> str:
        return "Forbidden type: " + self.type

class UnknownTypesError(MessageGeneratingError):
    def __init__(self, types: Iterable[str]) -> None:
        self.types: Final[tuple[str, ...]] = tuple(types)

    def generate_msg(self) -> str:
        output: str = "Unknown types:"
        for missing_type in self.types:
            output += "\n- "
            output += missing_type
        return output

def resolve() -> SourceGenContext:
    with open("./dom.generated.d.ts", 'r', encoding="utf-8") as f:
        ts_source: Final[str] = f.read()

    interfaces: Final[dict[str, DependencyTracked[Interface]]] = {}
    typealiases: Final[dict[str, DependencyTracked[TypeDefinition]]] = {}

    unresolved_interfaces: Final[dict[str, list[str]]] = {constants.context_to_resolve: []}
    def add_unresolved_dependencies(dependee: str, dependencies: Iterable[str]):
        for dep in dependencies:
            if dep in constants.forbidden_type_in_parse:
                raise ForbiddenTypeError(dep)
            if dep in interfaces:
                continue

            if dep not in unresolved_interfaces:
                if dep not in resolve_should_be_skipped:
                    unresolved_interfaces[dep] = [dependee]
            else:
                unresolved_interfaces[dep].append(dependee)

    print("Constructing source parser...")
    parser: Final = SourceParser(ts_source)

    unknown_types: set[str] = set()

    print("Resolving interfaces...")
    while len(unresolved_interfaces) > 0:
        resolve: str
        depended_by: list[str]
        (resolve, depended_by) = unresolved_interfaces.popitem() # Take oldest element from dict

        print(f"Resolving '{resolve}'... Depended by: {', '.join(depended_by)}")

        if (interface := try_resolve_interface(parser, resolve)) is not None:
            # Interface resolved
            interfaces[interface.name] = DependencyTracked(interface, depended_by)
            add_unresolved_dependencies(interface.name, interface.extends)

            for member in interface.members:
                add_unresolved_dependencies(interface.name, all_types_of_member(member))
        elif (typealias := try_resolve_typealias(parser, resolve)) is not None:
            assert typealias.name == resolve
            typealiases[typealias.name] = DependencyTracked(typealias, depended_by)
        else:
            unknown_types.add(resolve)

    print()
    print("[ Resolved Interface <- Depended By ]")
    for resolved in interfaces.values():
        print(f"{resolved.value.name} <- {', '.join(resolved.depended_by)}")
    print()
    print("[ Resolved Type <- Depended By ]")
    for resolved in typealiases.values():
        print(f"{resolved.value.name} <- {', '.join(resolved.depended_by)}")
    print()
    print("    [ Member: (types) ]")
    for resolved in interfaces.values():
        print(resolved.value.name)
        for member in resolved.value.members:
            print(f"    {member.name}: {', '.join(all_types_of_member(member))}")
    print()

    if len(unknown_types) > 0:
        raise UnknownTypesError(unknown_types)

    return construct_context(interfaces, typealiases)

def _get_valid_members(interface: Interface) -> Iterable[Member]:
    for member in interface.members:
        if member.name not in constants.context_remove_members:
            yield member

def construct_context(interfaces: dict[str, DependencyTracked[Interface]], typealiases: dict[str, DependencyTracked[TypeDefinition]]) -> SourceGenContext:
    to_resolve: Final[str] = constants.context_to_resolve
    to_resolve_interface: Interface = interfaces[to_resolve].value
    assert to_resolve == to_resolve_interface.name

    members: list[Member] = list(_get_valid_members(to_resolve_interface))
    for extends in to_resolve_interface.extends:
        if extends not in interfaces:
            continue

        extends_inter: Interface = interfaces[extends].value
        members.extend(_get_valid_members(extends_inter))
    members.extend(constants.context_add_custom_members)

    generate_csharp: dict[str, Interface | StringEnum] = {}
    for gen_cs_class in constants.cs_generate_classes_for_interfaces:
        generate_csharp[gen_cs_class] = interfaces[gen_cs_class].value
    for gen_typealias in typealiases.values():
        gen_typealias_type = gen_typealias.value.type
        if isinstance(gen_typealias_type, StringEnum):
            generate_csharp[gen_typealias.value.name] = gen_typealias_type

    return SourceGenContext(
        interface_name=to_resolve_interface.name,
        members=tuple(members),
        generate_csharp=generate_csharp
    )

def generate(ctx: SourceGenContext):
    print("Generating code...")

    DIRECTORY: Final[str] = "./sourcegen"
    WWWROOT: Final[str] = os.path.join(DIRECTORY, "wwwroot")
    CONTEXTS: Final[str] = os.path.join(DIRECTORY, "Contexts")

    js_bindings: str = generate_bindings.generate(ctx, generate_bindings.JsBindingsWriter)

    cs_bindings: str = generate_bindings.generate(ctx, generate_bindings.CsBindingsWriter)

    print("Writing files...")

    os.makedirs(WWWROOT, exist_ok=True)
    os.makedirs(CONTEXTS, exist_ok=True)

    with open(f"{WWWROOT}/ndpcanvas_sourcegen.g.js", "w", encoding="utf-8") as f:
        f.write(js_bindings)

    with open(f"{CONTEXTS}/CanvasRenderingContext2D_BINDINGS_SOURCEGEN.g.cs", "w", encoding="utf-8") as f:
        f.write(cs_bindings)

    # with open(f"{CONTEXTS}/CanvasRenderingContext2D_SOURCEGEN.g.cs", "w", encoding="utf-8") as f:
    #     f.write(cs_class)

    print("!! FINISHED !!")


def try_resolve_interface(parser: SourceParser, name: str) -> Interface | None:
    source: str | None = parser.try_get_interface_source(name)
    if source is None:
        return None
    interface: Interface = InterfaceParser(source).parse_interface()
    assert name == interface.name

    return interface

def try_resolve_typealias(parser: SourceParser, name: str):
    source: str | None = parser.try_get_typealias_source(name)
    if source is None:
        return None

    typealias: TypeDefinition = TypeDefinitionParser(source).parse_type_definition()
    assert name == typealias.name

    return typealias

def all_types_of_member(member: Member) -> set[str]:
    data: set[str] = set()

    def add_types(type: Type):
        nonlocal data
        if isinstance(type, SingleType):
            data.add(type.type)
        elif isinstance(type, (StringConstant, NullType)):
            pass
        elif isinstance(type, UnionType):
            for union_type in type.types:
                add_types(union_type)
        elif isinstance(type, ArrayType):
            add_types(type.elements_type)

    add_types(member.type)
    if isinstance(member, Method):
        for arg in member.arguments:
            add_types(arg.type)

    return data

def main():
    parent_dir: str = os.path.dirname(__file__)

    parent_dir_name: str = os.path.basename(parent_dir)
    expected_parent_dir_name: Final[str] = "SourceGeneration"
    if parent_dir_name != expected_parent_dir_name:
        print(f"Unexpected parent directory: {parent_dir_name}")
        print(f"Expected to be inside {expected_parent_dir_name}")
        print("We will TERMINATE just in case so that we don't mess up your system.")
        exit(1)

    try:
        ctx: SourceGenContext = resolve()
    except Exception as e:
        if not isinstance(e, MessageGeneratingError):
            raise

        print()
        print("======= ERROR =======")
        print(e.generate_msg())
        print("======= ERROR =======")
        exit(1)

    generate(ctx)

if __name__ == "__main__":
    main()
