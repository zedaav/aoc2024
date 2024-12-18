import logging
import re
from collections import deque
from pathlib import Path

from aoc2024.puzzle import CARDINAL_DIRS, OFFSETS, AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/18
"""

BYTE_PATTERN = re.compile(r"([\d]+),([\d]+)")


class D18Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path, target: tuple[int, int]):
        self.bytes: list[tuple[int, int]] = []
        self.start = (0, 0)
        self.target = target
        self.width = target[0] + 1
        self.height = target[1] + 1
        super().__init__(input_file)
        logging.info(f"start: {self.start}")
        logging.info(f"target: {self.target}")
        logging.info(f"bytes: {len(self.bytes)}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = BYTE_PATTERN.match(line)
        if m:
            self.bytes.append((int(m.group(1)), int(m.group(2))))

    def find_path(self, bytes_nb: int) -> int:
        # Obstables are the N first bytes
        obstacles = set(self.bytes[:bytes_nb])
        valid = set((x, y) for x in range(self.width) for y in range(self.height) if (x, y) not in obstacles)

        # Iterate on priority queue until reaching target position
        # Items in queue: (cost, (x,y))
        paths = {}
        q = deque([(0, self.start)])
        while q:
            # Pop next cheapest item
            cost, (x, y) = q.popleft()

            # Already got the cost for this path?
            if (x, y) in paths:
                continue
            paths[(x, y)] = cost

            # Try possible moves
            for d in CARDINAL_DIRS:
                # Candidate position
                dx, dy = OFFSETS[d]
                cx, cy = x + dx, y + dy

                # Possible move?
                if ((cx, cy) not in valid) or ((cx, cy) in paths):
                    # No: invalid position, or already seen
                    continue

                # Push one more possibility
                q.append((cost + 1, (cx, cy)))
        return paths.get(self.target, None)


class D18Step1Puzzle(D18Puzzle):
    def solve(self, bytes_nb: int) -> int:
        return self.find_path(bytes_nb)


class D18Step2Puzzle(D18Puzzle):
    def solve(self, bytes_nb: int) -> str:
        # Bisection between bytes_nb and length of all bytes
        a, b = bytes_nb, len(self.bytes)
        while a < b:
            # Try with the middle
            n = (a + b) // 2 + 1
            if self.find_path(n) is None:
                # Can't find path: retry on left side
                b = n - 1
            else:
                # Path is still valid: retry on right side
                a = n

        guilty_byte = self.bytes[a]
        return str(guilty_byte)[1:-1].replace(" ", "")
