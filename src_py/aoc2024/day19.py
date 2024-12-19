import logging
from functools import cache
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/19
"""


class D19Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.patterns: tuple[str] = None
        self.designs: list[str] = []
        super().__init__(input_file)
        logging.info(f"patterns: {self.patterns}")
        logging.info(f"designs: {len(self.designs)}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if "," in line:
            self.patterns = tuple(line.split(", "))
            assert len(self.patterns) == len(set(self.patterns))
        elif line:
            self.designs.append(line)


@cache
def design_ok(design: str, patterns: set[str]) -> bool:
    # Empty design --> ok
    if not design:
        return True

    # Iterate on patterns and go deeper if needed
    return any(design.startswith(p) and design_ok(design[len(p) :], patterns) for p in patterns)


@cache
def design_ways(design: str, patterns: tuple[str]) -> int:
    ways = 0

    # Empty design --> count 1
    if not design:
        ways = 1

    # Iterate on patterns to split
    for p in patterns:
        # Starts with pattern
        if design.startswith(p):
            ways += design_ways(design[len(p) :], patterns)

    # Patterns exhausted: return found ways
    return ways


class D19Step1Puzzle(D19Puzzle):
    def solve(self) -> int:
        # Count all "ok" designs
        total = 0
        for d in self.designs:
            ok = design_ok(d, self.patterns)
            logging.info(f"design '{d}' is {ok}")
            if ok:
                total += 1
        return total


class D19Step2Puzzle(D19Puzzle):
    def solve(self) -> int:
        # Count all "ok" designs
        total = 0
        for d in self.designs:
            ways = design_ways(d, self.patterns)
            logging.info(f"design '{d}' can be solved in {ways} ways")
            total += ways
        return total
