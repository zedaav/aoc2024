from dataclasses import dataclass
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/9
"""

# https://www.reddit.com/r/adventofcode/comments/1ha27bo/comment/m15wwre/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button


@dataclass
class File:
    ident: int
    pos: int
    size: int

    def __repr__(self) -> str:
        return f"{{ {self.ident}: pos={self.pos} size={self.size} }}"

    def checksum(self) -> int:
        # Sum all successive positions:
        # pos + (pos + 1) + ... + (pos + len - 1)
        # = pos*len + (len * (len - 1))//2
        return self.ident * ((self.pos * self.size) + (self.size * (self.size - 1)) // 2)


class D09Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.used: list[File] = []
        self.free: list[File] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        if line:
            pos = 0
            for ident, size in enumerate(map(int, line)):
                if ident % 2:
                    self.free.append(File(0, pos, size))
                else:
                    self.used.append(File(ident // 2, pos, size))
                pos += size


class D09Step1Puzzle(D09Puzzle):
    def solve(self) -> int:
        new_used = []

        # Iterate on used slots (reverse)
        for used in self.used[::-1]:
            # Iterate on free slots
            for free in self.free:
                if used.pos < free.pos:
                    break
                if free.size >= used.size:
                    # Fit entirely
                    used.pos = free.pos
                    free.size -= used.size
                    free.pos += used.size
                    break
                elif free.size:
                    # Need to split: create a new used file
                    new_file = File(used.ident, free.pos, free.size)
                    new_used.append(new_file)

                    # Update remaining chunk
                    used.size -= free.size

                    # Disqualify this free block for next search
                    free.size = 0

        self.used.extend(new_used)

        # Sum on used slots
        return sum(f.checksum() for f in self.used)


class D09Step2Puzzle(D09Puzzle):
    def solve(self) -> int:
        # Iterate on used slots (reverse)
        for used in self.used[::-1]:
            # Iterate on free slots
            for free in self.free:
                if (free.pos <= used.pos) and (free.size >= used.size):
                    # Fit entirely
                    used.pos = free.pos
                    free.size -= used.size
                    free.pos += used.size
                    break

        # Sum on used slots
        return sum(f.checksum() for f in self.used)
