import logging
from functools import cache
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/21
"""

NUMPAD = ["789", "456", "123", " 0A"]
DIRPAD = [" ^A", "<v>"]


def path(pad: list[str], key1: str, key2: str) -> str:
    # Get positions of both keys on the pad
    x1, y1 = next((x, y) for y, row in enumerate(pad) for x, col in enumerate(row) if col == key1)
    x2, y2 = next((x, y) for y, row in enumerate(pad) for x, col in enumerate(row) if col == key2)

    def g(x: int, y: int, seq: str):
        if (x, y) == (x2, y2):
            yield seq + "A"
        if x2 < x and pad[y][x - 1] != " ":
            yield from g(x - 1, y, seq + "<")
        if y2 < y and pad[y - 1][x] != " ":
            yield from g(x, y - 1, seq + "^")
        if y2 > y and pad[y + 1][x] != " ":
            yield from g(x, y + 1, seq + "v")
        if x2 > x and pad[y][x + 1] != " ":
            yield from g(x + 1, y, seq + ">")

    return min(g(x1, y1, ""), key=lambda p: sum(a != b for a, b in zip(p, p[1:], strict=False)))


@cache
def solve(seq: str, level: int, level_max: int) -> int:
    if level > level_max:
        # Reached the maximum level: just return the sequence length
        return len(seq)

    # Iterate on pairs of keys (n, n+1), and recursively build the path between these two keys, to finally sum the lengths of all the paths
    return sum(solve(path(DIRPAD if level else NUMPAD, key1, key2), level + 1, level_max) for key1, key2 in zip("A" + seq, seq, strict=False))


class D21Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.codes: list[str] = []
        super().__init__(input_file)
        logging.info(f"codes: {self.codes}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line:
            self.codes.append(line)

    def solve(self, level_max: int) -> int:
        # Iterate on codes
        total = 0
        for code in self.codes:
            # Solve sequence length and reckon complexity
            seq_len = solve(code, 0, level_max)
            complexity = seq_len * int(code.replace("A", ""))
            logging.info(f"code: {code}; seq len: {seq_len}, complexity: {complexity}")
            total += complexity
        return total


class D21Step1Puzzle(D21Puzzle):
    def solve(self) -> int:
        return super().solve(2)


class D21Step2Puzzle(D21Puzzle):
    def solve(self) -> int:
        return super().solve(25)
