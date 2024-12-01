import logging
import re
from abc import abstractmethod
from collections import defaultdict
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/1
"""

PATTERN = re.compile(r"(\d+)\s+(\d+)")


class D01Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.list1 = []
        super().__init__(input_file)
        logging.debug(f"list 1: {self.list1}")

    @abstractmethod
    def handle_number(self, nb: int):
        pass

    def parse_line(self, index: int, line: str) -> str:
        m = PATTERN.match(line)
        if m is not None:
            self.list1.append(int(m.group(1)))
            self.handle_number(int(m.group(2)))


class D01Step1Puzzle(D01Puzzle):
    def __init__(self, input_file: Path):
        self.list2 = []
        super().__init__(input_file)
        logging.debug(f"list 2: {self.list2}")

    def handle_number(self, nb: int):
        self.list2.append(nb)

    def solve(self) -> int:
        # Sum distances between numbers
        total = 0
        for a, b in zip(sorted(self.list1), sorted(self.list2), strict=True):
            total += abs(a - b)
        return total


class D01Step2Puzzle(D01Puzzle):
    def __init__(self, input_file: Path):
        self.line2_counts = defaultdict(lambda: 0)
        super().__init__(input_file)

    def handle_number(self, nb: int):
        self.line2_counts[nb] += 1

    def solve(self) -> int:
        total = 0
        for nb in self.list1:
            total += nb * self.line2_counts[nb]
        return total
