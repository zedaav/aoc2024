import logging
import re
from functools import cache
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/11
"""

PATTERN = re.compile(r"(\d+)")


@cache
def stones_count(stone: str, iterations: int) -> int:
    # One remaining iteration: 1
    if iterations == 0:
        return 1

    # Go to next level, depending on stone type

    # Rule 1: 0 --> 1
    if stone == "0":
        ret = stones_count("1", iterations - 1)
        return ret

    # Rule 2: even length --> split in 2
    if (len(stone) % 2) == 0:
        stone_len = len(stone)
        sum = 0
        for new_stone in map(lambda x: x.lstrip("0"), [stone[0 : stone_len // 2], stone[stone_len // 2 :]]):
            sum += stones_count(new_stone if new_stone else "0", iterations - 1)
        return sum

    # Rule 3: just multiply by 1024
    ret = stones_count(str(int(stone) * 2024), iterations - 1)
    return ret


class D11Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.stones: list[str] = []
        super().__init__(input_file)
        logging.debug(f"stones count: {len(self.stones)}")

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        for s in PATTERN.finditer(line):
            self.stones.append(s.group(1))

    def run(self, iterations: int) -> int:
        return sum(stones_count(s, iterations) for s in self.stones)


class D11Step1Puzzle(D11Puzzle):
    def solve(self) -> int:
        return self.run(25)


class D11Step2Puzzle(D11Puzzle):
    def solve(self) -> int:
        return self.run(75)
