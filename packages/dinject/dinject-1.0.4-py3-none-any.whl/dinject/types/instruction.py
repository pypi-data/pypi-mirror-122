from dataclasses import dataclass
from re import match
from typing import IO, Dict, Optional

from dinject.enums import Content, Host, Range
from dinject.exceptions import InstructionParseError


@dataclass
class Instruction:
    """Document injection instruction"""

    content: Content = Content.MARKDOWN
    """Content type to inject the result as."""

    range: Range = Range.NONE
    """Injection site demarcation."""

    host: Host = Host.SHELL
    """Execution host."""

    @staticmethod
    def parse(line: str) -> Optional["Instruction"]:
        """Parses `line` as an Instruction`."""

        m = match("^<!--dinject(.*)-->$", line)
        if not m:
            return None

        wip: Dict[str, str] = {}

        for pair in m.group(1).split(" "):
            if not pair:
                continue
            if m := match("([a-z]+)=([a-z]+)", pair):
                wip[m.group(1)] = m.group(2)
            else:
                raise InstructionParseError(pair, line)

        return Instruction(
            content=Content[wip.get("as", Content.MARKDOWN.name).upper()],
            range=Range[wip.get("range", Range.NONE.name).upper()],
            host=Host[wip.get("host", Host.SHELL.name).upper()],
        )

    @staticmethod
    def write_range_end(writer: IO[str]) -> None:
        """Writes an instruction to mark the end of an injection."""

        writer.write("<!--dinject")
        writer.write(f" range={Range.END.name.lower()}")
        writer.write("-->\n")

    def write_range_start(self, writer: IO[str]) -> None:
        """Writes an instruction to mark the start of an injection."""

        writer.write("<!--dinject")
        writer.write(f" as={self.content.name.lower()}")
        writer.write(f" host={self.host.name.lower()}")
        writer.write(f" range={Range.START.name.lower()}")
        writer.write("-->\n")
