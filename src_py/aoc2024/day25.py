import logging
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/25
"""


class D25Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.locks: list[list[int]] = []
        self.keys: list[list[int]] = []
        self.pending_lock: list[int] | None = None
        self.pending_key: list[int] | None = None
        super().__init__(input_file)
        logging.info(f"{len(self.locks)} locks:\n" + "\n".join(map(str, self.locks)))
        logging.info(f"{len(self.keys)} keys:\n" + "\n".join(map(str, self.keys)))

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line:
            if self.pending_lock is not None:
                # Update heights of pending lock
                for i, c in enumerate(line):
                    if c == "#":
                        self.pending_lock[i] += 1
            elif self.pending_key is not None:
                # Update heights of pending key
                for i, c in enumerate(line):
                    if c == "#":
                        self.pending_key[i] += 1
            else:
                # New lock or key
                if line.startswith("#"):
                    self.pending_lock = [1] * len(line)
                elif line.startswith("."):
                    self.pending_key = [0] * len(line)
        else:
            if self.pending_lock is not None:
                # Pending lock is over, remember it
                self.locks.append(self.pending_lock)
                self.pending_lock = None
            elif self.pending_key is not None:
                # Pending key is over, remember it
                self.keys.append(self.pending_key)
                self.pending_key = None


class D25Step1Puzzle(D25Puzzle):
    def solve(self) -> int:
        # Iterate on locks and keys
        total = 0
        for lock in self.locks:
            for key in self.keys:
                # Check if any column exceeds the max
                if not any(lk + k > 7 for lk, k in zip(lock, key, strict=True)):
                    total += 1
        return total
