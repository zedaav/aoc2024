import logging
from collections import defaultdict
from functools import cache
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/22
"""

MODULO = 16777216


@cache
def next_secret(number: int) -> int:
    number = ((number * 64) ^ number) % MODULO
    number = ((number // 32) ^ number) % MODULO
    number = ((number * 2048) ^ number) % MODULO
    return number


class D22Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.numbers: list[int] = []
        super().__init__(input_file)
        logging.info(f"numbers: {self.numbers}")
        self.secrets: dict[int, list[int | tuple[int, int]]] = defaultdict(list)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line:
            self.numbers.append(int(line))

    def build_secrets(self, changes: bool = True):
        for n in self.numbers:
            initial = n
            self.secrets[initial].append((n % 10, 0) if changes else n)
            for _ in range(2000):
                s = next_secret(n)
                c = (s % 10) - (n % 10)
                n = s
                self.secrets[initial].append((n % 10, c) if changes else n)


class D22Step1Puzzle(D22Puzzle):
    def solve(self) -> int:
        # Build secret numbers
        self.build_secrets(changes=False)

        # Sum all the last occurrences
        total = 0
        for n in self.numbers:
            secret = self.secrets[n][-1]
            logging.info(f"n: {n} -- secret: {secret}")
            total += secret
        return total


class D22Step2Puzzle(D22Puzzle):
    def solve(self) -> int:
        # Build secret numbers
        self.build_secrets(changes=True)

        # Bananas per pattern map
        bananas: dict[tuple[int, int, int, int], int] = defaultdict(lambda: 0)

        # Iterate over all the numbers
        for n in self.numbers:
            s = self.secrets[n]

            # Build obtained bananas per pattern for this number
            first_seqs = {}
            for i in range(len(s) - 3):
                t = tuple(map(lambda x: x[1], s[i : i + 4]))
                if t not in first_seqs:
                    first_seqs[t] = s[i + 3][0]

            # Merge into the main bananas map
            for k, v in first_seqs.items():
                bananas[k] += v

        return max(bananas.values())
