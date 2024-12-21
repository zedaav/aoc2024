import logging
import re
from itertools import combinations
from pathlib import Path
from queue import PriorityQueue

from aoc2024.puzzle import CARDINAL_DIRS, OFFSETS, AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/20
"""


def taxi_cab_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    # Compute the taxi-cab distance between two positions
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


class D20Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.start: tuple[int, int] | None = None
        self.target: tuple[int, int] | None = None
        self.obstacles: set[tuple[int, int]] = set()
        self.width = 0
        self.height = 0
        self.positions: dict[tuple[int, int], int] = {}
        self.initial_score = 0
        super().__init__(input_file)
        logging.info(f"start: {self.start}")
        logging.info(f"target: {self.target}")
        logging.info(f"obstacles: {len(self.obstacles)}")
        logging.info(f"map: {self.width}x{self.height}")

        # Browse possible positions
        self.prepare()
        logging.info(f"positions: {len(self.positions)}")
        self.initial_score = self.positions[self.target]
        logging.info(f"initial score: {self.initial_score}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line.startswith("#"):
            self.width = len(line)
            self.height += 1
            if "S" in line:
                self.start = (line.index("S"), index - 1)
            if "E" in line:
                self.target = (line.index("E"), index - 1)
            for x in re.finditer("#", line):
                self.obstacles.add((x.start(), index - 1))

    def is_in_map(self, pos: tuple[int, int]) -> bool:
        # Check if position is in map:
        x, y = pos
        return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)

    def prepare(self):
        # Browse the full path to:
        # - make sure that all free cells are on one single path
        # - remember the cost for each free cell
        # - identify all possible walls for cheating

        # Items in queue: (cost, (x,y))
        q = PriorityQueue()
        q.put((0, self.start))
        while not q.empty():
            # Pop next cheapest item
            cost, (x, y) = q.get()

            # Remember cost for this position
            assert (x, y) not in self.positions
            self.positions[(x, y)] = cost

            # Try possible moves
            next_pos = set()
            for nd in CARDINAL_DIRS:
                # Candidate position
                dx, dy = OFFSETS[nd]
                cx, cy = x + dx, y + dy

                # Possible move?
                if ((cx, cy) in self.positions) or ((cx, cy) in self.obstacles):
                    # No: already seen or obstacle
                    continue

                next_pos.add((cx, cy))

            # Make sure there is only one possible next position (or 0, if we reached target position)
            assert len(next_pos) in (0, 1), f"possible next moves for {(x,y)}: {next_pos}"

            # Push one more possibility
            if len(next_pos):
                q.put((cost + 1, next_pos.pop()))

        # Make sure we covered all positions
        assert self.width * self.height == len(self.obstacles) + len(self.positions)

    def solve(self, cheat_len_range: tuple[int, int], saved_min_cost: int) -> int:
        total = 0
        cheat_len_min, cheat_len_max = cheat_len_range

        # Iterate on possible combinations of two points
        for ((x1, y1), c1), ((x2, y2), c2) in combinations(self.positions.items(), 2):
            # Reckon the distance between the two points (= the cheat length)
            d = taxi_cab_distance((x1, y1), (x2, y2))
            if not (cheat_len_min <= d <= cheat_len_max):
                # Only keep cheats with a length in the expected range
                continue
            if abs(c2 - c1) - d >= saved_min_cost:
                # Only count cheats that save at least the expected amount of steps
                total += 1
        return total


class D20Step1Puzzle(D20Puzzle):
    def solve(self, saved_min_cost: int) -> int:
        return super().solve((2, 2), saved_min_cost)


class D20Step2Puzzle(D20Puzzle):
    def solve(self, saved_min_cost: int) -> int:
        return super().solve((2, 20), saved_min_cost)
