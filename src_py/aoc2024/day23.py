import logging
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/23
"""

LINK_PATTERN = re.compile(r"([a-z]{2})-([a-z]{2})")


class D23Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.computers: dict[str, set[str]] = defaultdict(set)
        super().__init__(input_file)
        logging.info(f"computers: {len(self.computers)}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = LINK_PATTERN.match(line)
        if m:
            # Fill computers map
            a, b = m.groups()
            self.computers[a].add(b)
            self.computers[b].add(a)


class D23Step1Puzzle(D23Puzzle):
    def solve(self) -> int:
        # Filter computers not linked to a "t" one
        for a, linked_ones in self.computers.copy().items():
            if not a.startswith("t") and not any(c.startswith("t") for c in linked_ones):
                del self.computers[a]
        logging.info(f"computers with t: {len(self.computers)}")

        # Filter triplets of interconnected computers
        triplets: set[set[str]] = set()
        for a, linked_ones in self.computers.copy().items():
            for b, c in combinations(linked_ones, 2):
                if c in self.computers[b]:
                    # a, b, c are interconnected
                    triplets.add(frozenset([a, b, c]))
        logging.info(f"triplets: {len(triplets)}")
        return sum(any(c.startswith("t") for c in t) for t in triplets)


class D23Step2Puzzle(D23Puzzle):
    def solve(self) -> int:
        # Iterate to find all sets of interconnected computers
        all_sets: set[frozenset[str]] = set()
        for a, linked_ones in self.computers.items():
            logging.debug(f"a: {a}, linked ones: {linked_ones}")
            candidates = linked_ones.copy()
            for b in linked_ones:
                if b not in candidates:
                    # Already removed
                    continue
                for c in filter(lambda x: x != b and x in candidates, linked_ones):
                    if c not in self.computers[b]:
                        candidates.remove(c)
            candidates.add(a)
            all_sets.add(frozenset(candidates))

        # Sort all sets by length
        longest = sorted(all_sets, key=lambda s: len(s), reverse=True)[0]
        return ",".join(sorted(longest))
