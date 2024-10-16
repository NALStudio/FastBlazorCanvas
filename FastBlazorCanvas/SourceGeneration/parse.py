# Type information fetched from: https://github.com/microsoft/TypeScript/blob/cd6c0a0b6b8659f49344951219c74a516fdec9a2/src/lib/dom.generated.d.ts

from abc import ABC
from dataclasses import dataclass
from typing import Final, Iterable, Self, Sequence, TypeAlias, cast

Strings: TypeAlias = tuple[str, ...]

class Type(ABC):
    pass

@dataclass(frozen=True)
class SingleType(Type):
    type: str

@dataclass(frozen=True)
class StringConstant(Type):
    value: str

@dataclass(frozen=True)
class NullType(Type): # Add a special null type that we can detect when generating C#
    pass              # as C# handles nullability very differently compared to TypeScript (TypeScript uses 'type | null' notation and C# uses 'Type?' notation)

@dataclass(frozen=True)
class UnionType(Type):
    types: tuple[Type, ...]

@dataclass(frozen=True)
class StringEnum(Type):
    values: tuple[StringConstant, ...]

@dataclass(frozen=True)
class ArrayType(Type):
    elements_type: Type

@dataclass(frozen=True)
class Member(ABC):
    name: str
    type: Type

@dataclass(frozen=True)
class MethodArgument:
    name: str
    type: Type
    optional: bool

@dataclass(frozen=True)
class Method(Member):
    arguments: tuple[MethodArgument, ...]

@dataclass(frozen=True)
class Field(Member):
    readonly: bool

@dataclass(frozen=True)
class Interface:
    name: str
    extends: tuple[str, ...]
    members: tuple[Member, ...]

@dataclass(frozen=True)
class TypeDefinition: # Use TypeDefinition as TypeAlias is already used by Python
    name: str
    type: Type

class SourceParser:
    def __init__(self, source: str) -> None:
        source = SourceParser.remove_comments(source)
        self.lines: tuple[str, ...] = tuple(source.splitlines())

    @staticmethod
    def remove_comments(source: str) -> str:
        def remove_comment(start: int, end: int):
            nonlocal source
            source = source[:start] + source[end:]

        multiline_start: int = 0
        while True:
            try:
                multiline_start = source.index("/*", multiline_start) # we can continue from the last index as we are completely sure that no comments occured before
            except ValueError:
                break

            multiline_end: int = source.index("*/", multiline_start)
            remove_comment(multiline_start, multiline_end + 2) # +2 since exclusive and token is 2 characters in size

        singleline_start: int = 0
        while True:
            try:
                singleline_start = source.index("//", singleline_start)
            except ValueError:
                break

            singleline_end: int = source.index('\n', singleline_start)
            remove_comment(singleline_start, singleline_end) # keep newline

        return source

    def try_get_interface_source(self, name: str) -> str | None:
        start_row: int | None = self.get_declaration_line("interface", name)
        if start_row is None:
            return None

        start_index: int = self.lines[start_row].find('{')
        if start_index == -1:
            raise ValueError("Could not find beginning '{'.") # We do assume it to be on the same line as the interface declaration, maybe this isn't the case after all?
        assert self.lines[start_row][start_index] == '{'

        row: int = start_row
        index: int = start_index
        parenthesis_count: int = 1
        while parenthesis_count > 0:
            index += 1
            if index >= len(self.lines[row]):
                index = 0
                row += 1

            row_text: str = self.lines[row]
            if row_text[index] == '{':
                parenthesis_count += 1
            elif row_text[index] == '}':
                parenthesis_count -= 1

        output: list[str] = []
        output.append(self.lines[start_row])
        output.extend(self.lines[(start_row + 1):row])
        output.append(self.lines[row][:(index + 1)]) # + 1 so that we include } in output

        return '\n'.join(output)

    def try_get_typealias_source(self, name: str) -> str | None:
        start_row: int | None = self.get_declaration_line("type", name)
        if start_row is None:
            return None

        end_row: int = start_row # inclusive
        while ';' not in self.lines[end_row]:
            end_row += 1

        end_index: int = self.lines[end_row].index(';') # inclusive

        output: list[str] = []
        output.extend(self.lines[start_row:end_row])
        output.append(self.lines[end_row][:(end_index + 1)])

        return '\n'.join(output)

    def get_declaration_line(self, declaration_type: str, declaration_name: str) -> int | None:
        should_start_with: str = declaration_type + " " + declaration_name + " " # require trailing space to differentiate CanvasRenderingContext2D from CanvasRenderingContext2DSettings
                                                                                 # this does break support of 'declare var' syntax which uses a trailing : character

        declarations: list[int] = []
        for i, line in enumerate(self.lines):
            if line.startswith(should_start_with):
                declarations.append(i)

        if len(declarations) > 1:
            raise LookupError("Multiple declarations found.")
        elif len(declarations) > 0:
            return declarations[0]
        else:
            return None

class InterfaceParser:
    def __init__(self, source: str) -> None:
        self.tokens: Final[Strings] = (
            Tokenizer(source)
                .with_token_char(',')
                .with_token_char(';')
                .build_tokens()
        )

    def parse_interface(self) -> Interface:
        tokens: Strings = self.tokens

        assert tokens[0] == "interface"
        assert tokens[-1] == '}'

        name: str = tokens[1]
        extends: Strings | None = None

        body_start: int = 2
        if tokens[body_start] == "extends":
            (move_next, extends) = self._parse_extends(2)
            body_start += move_next

        members: tuple[Member, ...] = self._parse_body(body_start)

        if extends is None:
            extends = ()
        return Interface(name, extends, members)

    def _parse_extends(self, start: int) -> tuple[int, Strings]: # returns move next amount
        assert self.tokens[start] == "extends"

        extends: list[str] = []
        length: int = 1 # 1 so that we don't include extends in the tokens
        while True:
            token: str = self.tokens[start + length]
            if token == '{':
                break

            if token != ',':
                extends.append(token)
            length += 1

        return (length, tuple(extends))

    def _parse_body(self, start: int) -> tuple[Member, ...]:
        assert self.tokens[start] == '{'
        assert self.tokens[-1] == '}'

        tokens: list[str] = list(self.tokens[(start + 1):-1])
        member_tokens: list[Strings] = group_tokens_by_delimeter(tokens, ';')

        members: list[Member] = []
        for memtokens in member_tokens:
            member: Member | None = MethodParser(memtokens).try_parse_method()
            if member is None:
                member = FieldParser(memtokens).parse_field()
            members.append(member)

        return tuple(members)

class MethodParser:
    def __init__(self, tokens: Strings) -> None:
        self.tokens: Final[Strings] = (
            Tokenizer(tokens)
                .with_token_char('(')
                .with_token_char(')')
                .with_token_char(',')
                .build_tokens()
                # we don't tokenize : so that we don't mess with argument parsing
        )

    def try_parse_method(self) -> Method | None:
        tokens: Strings = self.tokens

        name: str = tokens[0]

        if tokens[1] != '(':
            return None
        arguments_start: int = 1
        arguments_end: int = find_pair(tokens, arguments_start, '(', ')')

        arguments: Final = self._parse_arguments(arguments_start, arguments_end)

        assert tokens[arguments_end + 1] == ':' # We don't tokenize : but since it is followed by a whitespace, this assert should go through

        return_type_start: int = arguments_end + 2
        return_type: Type = TypeParser(tokens[return_type_start:]).parse_type()

        return Method(
            name=name,
            type=return_type,
            arguments=arguments
        )

    def _parse_arguments(self, start: int, end: int) -> tuple[MethodArgument, ...]:
        assert self.tokens[start] == '('
        assert self.tokens[end] == ')'

        tokens: tuple[str, ...] = self.tokens[(start + 1):end]
        argument_expressions: list[Strings] = group_tokens_by_delimeter(tokens, ',')

        arguments: list[MethodArgument] = []
        for arg in argument_expressions:
            arg_parser = ArgumentParser(arg)
            parsed_arg: MethodArgument = arg_parser.parse_argument()
            arguments.append(parsed_arg)

        return tuple(arguments)

class ArgumentParser:
    def __init__(self, tokens: Strings) -> None:
        self.tokens: Final[Strings] = (
            Tokenizer(tokens)
                .with_token_char(':')
                .with_token_char('?')
                .build_tokens()
        )

    def parse_argument(self) -> MethodArgument:
        tokens: list[str] = list(self.tokens)

        name: str = tokens.pop(0)

        optional: bool = False
        if tokens[0] == '?':
            optional = True
            tokens.pop(0)

        colon: str = tokens.pop(0)
        assert colon == ':'
        argument_type: Type = TypeParser(tokens).parse_type() # rest of the tokens are type information

        return MethodArgument(
            name=name,
            type=argument_type,
            optional=optional
        )

class FieldParser:
    def __init__(self, tokens: Strings) -> None:
        self.tokens: Final[Strings] = (
            Tokenizer(tokens)
                .with_token_char(':')
                .build_tokens()
        )

    def parse_field(self) -> Field:
        tokens: list[str] = list(self.tokens)

        readonly: bool = False
        if tokens[0] == "readonly":
            readonly = True
            tokens.pop(0)

        name: str = tokens.pop(0)
        colon: str = tokens.pop(0)
        assert colon == ':'
        field_type: Type = TypeParser(tokens).parse_type()

        return Field(
            name=name,
            type=field_type,
            readonly=readonly
        )

class Tokenizer:
    def __init__(self, source: str | Iterable[str]) -> None:
        if isinstance(source, str):
            source = (source,)

        tokens: list[str] = []
        for token_or_source in source:
            tokens.extend(token_or_source.split())

        self._tokens: list[str] = tokens

    def with_token_char(self, char: str) -> Self:
        assert len(char) == 1

        def char_should_be_extracted(token: str) -> bool:
            assert len(char) == 1
            return len(token) > 1 and char in token

        tokens: list[str] = self._tokens

        while any(char_should_be_extracted(token) for token in tokens):
            for i, token in enumerate(tokens):
                if not char_should_be_extracted(token):
                    continue

                start_index: int = token.index(char)
                end_index: int = start_index + len(char)

                left: str = token[:start_index]
                extracted: str = token[start_index:end_index]
                right: str = token[end_index:]

                tokens.pop(i)

                if len(right) > 0:
                    tokens.insert(i, right)

                assert len(extracted) > 0
                tokens.insert(i, extracted)

                if len(left) > 0:
                    tokens.insert(i, left)

                break # BREAK OUT OF FOR-LOOP because we have just modified the tokens list
                # we will stay in the while loop until all tokens have been extracted

        return self

    def build_tokens(self) -> Strings:
        return tuple(self._tokens)

class TypeParser:
    def __init__(self, tokens: Iterable[str]) -> None:
        self.tokens: Strings = (
            Tokenizer(tokens)
                .with_token_char('|')
                .with_token_char('(')
                .with_token_char(')')
                .with_token_char('[')
                .with_token_char(']')
                .build_tokens()
        )

    def parse_type(self) -> Type:
        types: list[Type] = []

        tokens: list[str] = list(self.tokens)
        while len(tokens) > 0:
            if tokens[0] == '(':
                types.append(self._handle_parenthesis(tokens))
            elif tokens[0] == '[':
                left: str = tokens.pop(0)
                right: str = tokens.pop(0)
                assert left == '['
                assert right == ']'
                types[-1] = ArrayType(types[-1])
            elif tokens[0] == '|':
                tokens.pop(0)
            else:
                single: str = tokens.pop(0)
                types.append(self._resolve_single_type(single))

        assert len(types) > 0
        if len(types) == 1:
            return types[0]
        else:
            if all(isinstance(t, StringConstant) for t in types):
                return StringEnum(cast(tuple[StringConstant], tuple(types)))
            else:
                return UnionType(tuple(types))

    @staticmethod
    def _resolve_single_type(single: str) -> Type:
        if single.startswith("\"") and single.endswith("\""):
            return StringConstant(single[1:-1])
        elif single == "null":
            return NullType()
        else:
            return SingleType(single)

    @staticmethod
    def _handle_parenthesis(tokens: list[str]) -> Type:
        end_parenthesis: int = find_pair(tokens, 0, '(', ')')

        left: str = tokens.pop(0)

        parenthesis_tokens: list[str] = []
        for _ in range(end_parenthesis - 1):
            parenthesis_tokens.append(tokens.pop(0))

        right: str = tokens.pop(0)
        assert left == '(', "Unexpected token: " + left
        assert len(parenthesis_tokens) > 0
        assert right == ')', "Unexpected token: " + right

        return TypeParser(parenthesis_tokens).parse_type()

class TypeDefinitionParser:
    def __init__(self, source: str) -> None:
        self.tokens: Final[Strings] = (
            Tokenizer(source)
                .with_token_char('=')
                .with_token_char(';')
                .build_tokens()
        )

    def parse_type_definition(self) -> TypeDefinition:
        tokens: list[str] = list(self.tokens)

        type_def: str = tokens.pop(0)
        name: str = tokens.pop(0)
        equals: str = tokens.pop(0)
        semicolon: str = tokens.pop(-1)

        assert type_def == "type"
        assert equals == '='
        assert semicolon == ';'

        type: Type = TypeParser(tokens).parse_type()

        return TypeDefinition(name=name, type=type)

def group_tokens_by_delimeter(tokens: Iterable[str], delimeter: str) -> list[Strings]:
    assert len(delimeter) == 1

    output: list[list[str]] = [[]]
    for t in tokens:
        if t == delimeter:
            output.append([])
        else:
            output[-1].append(t)

    if len(output[-1]) < 1:
        output.pop(-1)

    return [tuple(group) for group in output]

def find_pair(tokens: Sequence[str], left_index: int, left: str, right: str) -> int:
    assert len(left) == 1
    assert len(right) == 1
    assert tokens[left_index] == left

    count: int = 1
    index: int = left_index
    while count > 0:
        index += 1
        tok: str = tokens[index]
        if tok == left:
            count += 1
        elif tok == right:
            count -= 1

    return index
