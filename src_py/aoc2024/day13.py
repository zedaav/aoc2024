import re
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/13
"""

BUTTON_PATTERN = re.compile(r"Button ([AB]): X\+([\d]+), Y\+([\d]+)")
PRIZE_PATTERN = re.compile(r"Prize: X=([\d]+), Y=([\d]+)")

"""
a * ax + b * bx = tx
a * ay + b * by = ty

equivalent to

a = (ty * bx - tx * by) / (ay * bx - ax * by)
b = -((ty * ax - tx * ay) / (ay * bx - ax * by))
"""


class ClawMachine:
    def __init__(self):
        self.a: tuple[int, int] | None = None
        self.b: tuple[int, int] | None = None
        self.target: tuple[int, int] | None = None

    def __repr__(self) -> str:
        return f"{self.a}/{self.b}/{self.target}"

    def cost(self, offset: int = 0) -> int:
        ax, ay = self.a
        bx, by = self.b
        tx, ty = self.target
        tx += offset
        ty += offset
        a = (ty * bx - tx * by) / (ay * bx - ax * by)
        b = -((ty * ax - tx * ay) / (ay * bx - ax * by))

        if a.is_integer() and b.is_integer():
            return int(a * 3 + b)
        return 0


class D13Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.machines: list[ClawMachine] = []
        self.pending_machine = None
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = BUTTON_PATTERN.match(line)
        if m is not None:
            if m.group(1) == "A":
                self.pending_machine = ClawMachine()
                self.pending_machine.a = (int(m.group(2)), int(m.group(3)))
            else:
                self.pending_machine.b = (int(m.group(2)), int(m.group(3)))
        else:
            m = PRIZE_PATTERN.match(line)
            if m is not None:
                self.pending_machine.target = (int(m.group(1)), int(m.group(2)))
                self.machines.append(self.pending_machine)
                self.pending_machine = None


class D13Step1Puzzle(D13Puzzle):
    def solve(self) -> int:
        return sum(m.cost(0) for m in self.machines)


class D13Step2Puzzle(D13Puzzle):
    def solve(self) -> int:
        return sum(m.cost(10000000000000) for m in self.machines)
