import logging
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/8
"""

ANTENNA_PATTERN = re.compile(r"([a-zA-Z0-9])")


class D08Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.antennas: dict[str, set[tuple[int, int]]] = defaultdict(set)
        self.height = 0
        self.width = 0
        super().__init__(input_file)
        logging.info(f"width={self.width} height={self.height} antennas={self.antennas}")

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        if line:
            self.width = len(line)
            self.height += 1
            for m in ANTENNA_PATTERN.finditer(line):
                self.antennas[m.group(1)].add((m.start(1), index - 1))

    def solve(self, greedy: bool = False) -> int:
        # Iterate on antennas
        antinodes = set()
        for type, locs in self.antennas.items():
            # Iterate on all combinations of locations
            logging.info(f"> combinations for {type} antennas")
            for (xa, ya), (xb, yb) in combinations(locs, 2):
                # All antennas are also antinodes
                if greedy:
                    antinodes.add((xa, ya))
                    antinodes.add((xb, yb))

                # Reckon and apply delta
                logging.info(f">> {(xa, ya)} vs {(xb, yb)}")
                dx, dy = abs(xa - xb), abs(ya - yb)

                # Check order
                wx = xa > xb
                wy = ya > yb

                # Compute anti-nodes
                for cx, cy, d in (xa, ya, -1), (xb, yb, 1):
                    index = 1
                    while True:
                        nx, ny = cx + (dx * d * (-1 if wx else 1) * index), cy + (dy * d * (-1 if wy else 1) * index)
                        # logging.info(f">>>> {(nx, ny)} ({(cx, cy, dx, dy, d, wx, wy)})")
                        if (nx < 0) or (ny < 0) or (nx >= self.width) or (ny >= self.height):
                            break

                        # Still valid, remember
                        antinodes.add((nx, ny))

                        if not greedy:
                            # Not greedy: only one occurrence
                            break
                        else:
                            # Greedy: continue to add more antinodes
                            index += 1

        return len(antinodes)


class D08Step1Puzzle(D08Puzzle):
    def solve(self) -> int:
        return super().solve()


class D08Step2Puzzle(D08Puzzle):
    def solve(self) -> int:
        return super().solve(True)
