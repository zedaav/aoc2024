import logging
from collections import defaultdict
from pathlib import Path
from queue import Queue

from aoc2024.puzzle import CARDINAL_DIRS, OFFSETS, AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/10
"""


class D10Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.map: list[list[int]] = []
        self.roots: set[tuple[int, int]] = set()
        self.targets: set[tuple[int, int]] = set()
        self.width = 0
        self.height = 0
        super().__init__(input_file)
        logging.debug(f"size: {self.width}x{self.height} ; roots: {self.roots}")

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        if line:
            self.height += 1
            new_line = [(-1 if d == "." else int(d)) for d in line]
            self.width = len(new_line)
            self.map.append(new_line)
            for x, p in enumerate(new_line):
                if p == 0:
                    self.roots.add((x, index - 1))
                elif p == 9:
                    self.targets.add((x, index - 1))


class D10Step1Puzzle(D10Puzzle):
    def solve(self) -> int:
        total = 0
        q = Queue()
        known_pos = defaultdict(set)
        for pos in self.roots:
            q.put((pos, pos))
            known_pos[pos].add(pos)

        while not q.empty():
            root, (x, y) = q.get()
            for d in CARDINAL_DIRS:
                dx, dy = OFFSETS[d]
                nx, ny = x - dx, y - dy
                if (nx < 0) or (nx >= self.width) or (ny < 0) or (ny >= self.height):
                    # Out of map
                    continue

                # Put in queue only if exactly one more than current position, and we didn't follow this path already
                if (self.map[ny][nx] == self.map[y][x] + 1) and ((nx, ny) not in known_pos[root]):
                    # Add to known pos for this root
                    known_pos[root].add((nx, ny))

                    # Got a 9?
                    if self.map[ny][nx] == 9:
                        total += 1
                    else:
                        q.put((root, (nx, ny)))

        return total


class D10Step2Puzzle(D10Puzzle):
    def solve(self) -> int:
        total = 0
        q = Queue()
        for pos in self.targets:
            path = set()
            path.add(pos)
            q.put((pos, path))

        while not q.empty():
            (x, y), path = q.get()
            for d in CARDINAL_DIRS:
                dx, dy = OFFSETS[d]
                nx, ny = x - dx, y - dy
                if (nx < 0) or (nx >= self.width) or (ny < 0) or (ny >= self.height):
                    # Out of map
                    continue

                # Put in queue only if exactly one less than current position, and we didn't follow this path already
                if (self.map[ny][nx] == self.map[y][x] - 1) and ((nx, ny) not in path):
                    # Add to path for this position
                    new_path = set(path)
                    new_path.add((nx, ny))

                    # Got a 0?
                    if self.map[ny][nx] == 0:
                        total += 1
                    else:
                        q.put(((nx, ny), new_path))

        return total
