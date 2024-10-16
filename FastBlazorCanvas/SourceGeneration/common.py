from abc import ABC, abstractmethod
from dataclasses import dataclass

from parse import *


@dataclass(frozen=True)
class SourceGenContext:
    interface_name: str

    members: tuple[Member, ...]

    generate_csharp: dict[str, Interface | StringEnum]

class CodeWriter:
    def __init__(self, initial_value: str = "") -> None:
        self._content: list[str] = [initial_value]
        self._written_after_newline: bool = False
        self.indent: int = 0

    def write(self, value: str) -> Self:
        if not self._written_after_newline:
            self._content.append(' ' * (4 * self.indent)) # indent content
            self._written_after_newline = True

        self._content.append(value)
        return self

    def writeline(self, value: str = "") -> Self:
        if len(value) > 0: # if check so that we don't just indent unnecessarily
            self.write(value)

        self._content.append('\n')
        self._written_after_newline = False
        return self

    def tostring(self) -> str:
        return ''.join(self._content)

class HighLevelCodeWriter(ABC):
    def __init__(self, ctx: SourceGenContext) -> None:
        super().__init__()

        self.writer: CodeWriter = CodeWriter()
        self.ctx: Final[SourceGenContext] = ctx

    @abstractmethod
    def write_start(self):
        pass

    @abstractmethod
    def write_method(self, method: Method, arguments: tuple[MethodArgument, ...], *, optionals_included: bool):
        pass

    @abstractmethod
    def write_property_start(self, property: Field):
        pass

    @abstractmethod
    def write_getter(self, property: Field):
        pass

    @abstractmethod
    def write_setter(self, property: Field):
        pass

    @abstractmethod
    def write_property_end(self):
        pass

    @abstractmethod
    def write_end(self):
        pass

    def tostring(self) -> str:
        return self.writer.tostring()
