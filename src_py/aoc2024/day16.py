import logging
import re
from pathlib import Path
from queue import PriorityQueue

from aoc2024.puzzle import OFFSETS, OPPOSITE, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2024/day/16
"""

EXTRA_COST = 1000
NO_COST = 1
MOVE_MAP = {
    Direction.N: [(Direction.N, NO_COST), (Direction.E, EXTRA_COST), (Direction.W, EXTRA_COST)],
    Direction.E: [(Direction.E, NO_COST), (Direction.S, EXTRA_COST), (Direction.N, EXTRA_COST)],
    Direction.S: [(Direction.S, NO_COST), (Direction.W, EXTRA_COST), (Direction.E, EXTRA_COST)],
    Direction.W: [(Direction.W, NO_COST), (Direction.N, EXTRA_COST), (Direction.S, EXTRA_COST)],
}


class D16Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.start: tuple[int, int] | None = None
        self.target: tuple[int, int] | None = None
        self.obstacles: set[tuple[int, int]] = set()
        self.width = 0
        self.height = 0
        super().__init__(input_file)
        logging.info(f"start: {self.start}")
        logging.info(f"target: {self.target}")
        logging.info(f"obstacles: {len(self.obstacles)}")

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

    def compute(self, forward: bool = True) -> tuple[int, dict[(int, int, Direction), int]]:
        # Iterate on priority queue until reaching target position

        # Items in queue: (cost, ((x,y),direction))
        q = PriorityQueue()
        winning_cost = None
        all_costs = {}
        seen_pos = set()
        dest = self.target if forward else self.start
        if forward:
            q.put((0, (self.start, Direction.E)))
        else:
            for d in MOVE_MAP:
                q.put((0, (self.target, d)))
        while not q.empty():
            # Pop next cheapest item
            cost, ((x, y), d) = q.get()

            # Remember cost with direction
            if (x, y, d) not in all_costs:
                all_costs[(x, y, d)] = cost

            # Already seen position?
            if (x, y, d) in seen_pos:
                continue
            seen_pos.add((x, y, d))

            # Reached target position?
            if (x, y) == dest:
                if winning_cost is None:
                    winning_cost = cost
                continue
            if winning_cost and cost > winning_cost:
                continue

            # Try possible moves
            for nd, nc in MOVE_MAP[d]:
                # Candidate position
                if nd == d:
                    dx, dy = OFFSETS[nd]
                    cx, cy = x + dx, y + dy
                else:
                    cx, cy = x, y

                # Possible move?
                if (cx, cy) in self.obstacles:
                    # No: obstacle
                    continue

                # Push one more possibility
                q.put((cost + nc, ((cx, cy), nd)))

        return winning_cost, all_costs


class D16Step1Puzzle(D16Puzzle):
    def solve(self) -> int:
        c, _ = self.compute()
        return c


class D16Step2Puzzle(D16Puzzle):
    def solve(self) -> int:
        # Go forward and reverse
        best, d1 = self.compute()
        _, d2 = self.compute(False)

        # Check all points with the correct cost
        all_good_pos = set()
        for x in range(self.width):
            for y in range(self.height):
                for d in MOVE_MAP:
                    if (x, y, d) in d1 and (x, y, OPPOSITE[d]) in d2 and d1[(x, y, d)] + d2[(x, y, OPPOSITE[d])] == best:
                        all_good_pos.add((x, y))
        return len(all_good_pos)
