import re
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/3
"""

PATTERN1 = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
PATTERN2 = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))")
INST_MUL = "mul"
INST_DO = "do("
INST_DONT = "don"


class D03Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.mul_instructions: list[tuple[int, int]] = []
        self.enabled = True
        super().__init__(input_file)

    def solve(self) -> int:
        # Multiplications result
        return sum(x * y for x, y in self.mul_instructions)


class D03Step1Puzzle(D03Puzzle):
    def parse_line(self, index: int, line: str):
        # Parse instruction line
        self.mul_instructions.extend([(int(m.group(1)), int(m.group(2))) for m in PATTERN1.finditer(line)])


class D03Step2Puzzle(D03Puzzle):
    def parse_line(self, index: int, line: str):
        # Iterate on instructions
        for m in PATTERN2.finditer(line):
            prefix = m.group()[0:3]
            if prefix == INST_MUL and self.enabled:
                self.mul_instructions.append((int(m.group(2)), int(m.group(3))))
            elif prefix == INST_DO:
                self.enabled = True
            elif prefix == INST_DONT:
                self.enabled = False
