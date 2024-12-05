import re
from functools import cmp_to_key
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/5
"""

RULE_PATTERN = re.compile(r"(\d+)\|(\d+)")


class D05Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.rules: set[tuple[int, int]] = set()
        self.updates: list[dict[int, int]] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str):
        m = RULE_PATTERN.match(line)
        if m is not None:
            # Rule line
            self.rules.add((int(m.group(1)), int(m.group(2))))
        elif "," in line:
            # Updates list line
            self.updates.append({int(nb): off for off, nb in enumerate(line.split(",")) if nb not in [None, ""]})

    def validate(self, update: dict[int, int]) -> bool:
        # Iterate on rules
        return all(not ((x in update) and (y in update) and (update[x] > update[y])) for x, y in self.rules)


class D05Step1Puzzle(D05Puzzle):
    def solve(self) -> int:
        total = 0

        # Iterate on updates
        for update in self.updates:
            if self.validate(update):
                # All rules are passed, remember middle number
                total += list(update.keys())[len(update) // 2]

        return total


class D05Step2Puzzle(D05Puzzle):
    def custom_compare(self, x: int, y: int) -> int:
        if (x, y) in self.rules:
            return -1
        if (y, x) in self.rules:
            return 1
        return 0

    def solve(self) -> int:
        total = 0

        # Iterate on updates
        for update in self.updates:
            if not self.validate(update):
                # Invalid update: reorder pages
                sorted_update = sorted(list(update.keys()), key=cmp_to_key(self.custom_compare))

                # Once reordered, add middle page
                total += sorted_update[len(sorted_update) // 2]

        return total
