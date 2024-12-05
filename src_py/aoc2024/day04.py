import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from aoc2024.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2024/day/4
"""

LETTER_TO_DIGIT = {"X": 0, "M": 1, "A": 2, "S": 3}

CROSS_DIR = [Direction.NW, Direction.NE, Direction.SE, Direction.SW]


@dataclass
class Candidate:
    map: list[list[int]]
    x: int
    y: int
    width: int
    height: int

    def count_words(self) -> int:
        total = 0
        for d in Direction:
            nx, ny = self.x, self.y
            dx, dy = OFFSETS[d]
            v = self.map[ny][nx]
            while v < 3:
                nx, ny = nx + dx, ny + dy
                if (nx < 0) or (ny < 0) or (nx >= self.width) or (ny >= self.height):
                    # Out of map
                    break
                nv = self.map[ny][nx]
                if nv == v + 1:
                    v = nv
                else:
                    # Broken 0,1,2,3 chain
                    break
            else:
                # While loop exhausted, one more full word
                total += 1
        return total

    def count_x(self) -> int:
        vs = []
        vs_map = defaultdict(lambda: 0)
        for d in CROSS_DIR:
            dx, dy = OFFSETS[d]
            nx, ny = self.x + dx, self.y + dy
            if (nx < 0) or (ny < 0) or (nx >= self.width) or (ny >= self.height):
                # Missing one branch, give up
                return 0
            v = self.map[ny][nx]
            if v not in [1, 3]:
                # Neither M or S
                return 0
            vs_map[v] += 1
            vs.append(v)

        # This is a valid X-MAS if we get:
        # * 2 M and 2 S
        # * not that:
        #   M S      S M
        #    A   or   A
        #   S M      M S
        return 1 if ((vs_map == {1: 2, 3: 2}) and (tuple(vs) not in [(1, 3, 1, 3), (3, 1, 3, 1)])) else 0


class D04Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.map: list[list[int]] = []
        super().__init__(input_file)
        self.height = len(self.map)
        self.width = len(self.map[0])

    def parse_line(self, index: int, line: str):
        # Replace letters by digits
        self.map.append([LETTER_TO_DIGIT[x] for x in super().parse_line(index, line)])


class D04Step1Puzzle(D04Puzzle):
    def solve(self) -> int:
        total = 0

        # Browse the whole map
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 0:
                    # Only valid candidates start with 0 (= "X")
                    logging.debug(f"Check candidate in {x},{y}")
                    c = Candidate(self.map, x, y, self.width, self.height)
                    total += c.count_words()

        return total


class D04Step2Puzzle(D04Puzzle):
    def solve(self) -> int:
        total = 0

        # Browse the whole map
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 2:
                    # Only valid candidates start with 2 (= "A")
                    logging.debug(f"Check candidate in {x},{y}")
                    c = Candidate(self.map, x, y, self.width, self.height)
                    total += c.count_x()

        return total
