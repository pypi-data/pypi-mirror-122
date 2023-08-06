from dataclasses import dataclass, field
from typing import IO, List


@dataclass
class Block:
    lang: str
    lines: List[str] = field(default_factory=list)
    complete: bool = False

    @property
    def script(self) -> str:
        """Joins `lines` into a single script."""
        return "".join(self.lines)

    def write(self, writer: IO[str]) -> None:
        """Writes a Markdown code block."""

        writer.write(f"```{self.lang}\n")
        for line in self.lines:
            writer.write(line)
        writer.write("```\n")
