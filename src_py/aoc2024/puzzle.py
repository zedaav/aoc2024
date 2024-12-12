from abc import ABC, abstractmethod
from enum import IntEnum, auto
from pathlib import Path


# Directions
class Direction(IntEnum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()
    NE = auto()
    SE = auto()
    SW = auto()
    NW = auto()


# Cardinal directions
CARDINAL_DIRS = [Direction.N, Direction.E, Direction.S, Direction.W]

# Opposite directions
OPPOSITE = {
    Direction.N: Direction.S,
    Direction.S: Direction.N,
    Direction.W: Direction.E,
    Direction.E: Direction.W,
}

# Offsets
OFFSETS = {
    Direction.N: (0, -1),
    Direction.NE: (1, -1),
    Direction.E: (1, 0),
    Direction.SE: (1, 1),
    Direction.S: (0, 1),
    Direction.SW: (-1, 1),
    Direction.W: (-1, 0),
    Direction.NW: (-1, -1),
}


# Base class for puzzle solutions
class AOCPuzzle(ABC):
    def __init__(self, input_file: Path):
        # Parse input file
        self.input_file = input_file
        self.input_lines = []
        self.parse_file()

    def parse_file(self):
        # Check file existence
        assert self.input_file.is_file(), f"File not found: {self.input_file}"

        # Browse input lines
        with self.input_file.open() as f:
            for index, line in enumerate(f.readlines(), start=1):
                # Remember parsed line
                self.input_lines.append(self.parse_line(index, line))

    def parse_line(self, index: int, line: str) -> str:
        # Default implementation: just strip meaningless characters at end of line
        return line.strip("\r\n ")

    @abstractmethod
    def solve(self) -> int | str | list[str]:  # pragma: no cover
        pass
