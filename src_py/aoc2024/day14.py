import logging
import re
from dataclasses import dataclass
from math import prod
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/14
"""

ROBOT_PATTERN = re.compile(r"p=([-\d]+),([-\d]+) +v=([-\d]+),([-\d]+)")


@dataclass
class Robot:
    p: tuple[int, int]
    v: tuple[int, int]

    def __repr__(self) -> str:
        return f"{self.p}/{self.v}"

    def move(self, iter: int, dims: tuple[int, int]) -> tuple[int, int]:
        x, y = self.p
        dx, dy = self.v
        w, h = dims

        # Move with modulo
        x += dx * iter
        x %= w
        if x < 0:
            x += w
        y += dy * iter
        y %= h
        if y < 0:
            y += h
        return (x, y)


class D14Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.robots: list[Robot] = []
        super().__init__(input_file)
        logging.info(f"robots: {self.robots}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = ROBOT_PATTERN.match(line)
        if m is not None:
            self.robots.append(Robot((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))))


class D14Step1Puzzle(D14Puzzle):
    def solve(self, dims: tuple[int, int]) -> int:
        # Iterate on robots
        w, h = dims
        qw, qh = (w // 2), (h // 2)
        logging.info(f"qw,qh : {(qw,qh)}")
        quarters = {(x, y): [] for x in range(2) for y in range(2)}
        for r in self.robots:
            # Move it
            x, y = r.move(100, dims)

            if (x == qw) or (y == qh):
                # Just in the middle, not in any quarter
                continue

            # Put in in the right quarter
            qx, qy = int(x > qw), int(y > qh)
            quarters[(qx, qy)].append((x, y))

        return prod(len(q) for q in quarters.values())


class D14Step2Puzzle(D14Puzzle):
    def solve(self, out_folder: Path) -> int:
        w, h = 101, 103
        expected_len = len(self.robots)
        i = 0
        while True:
            i += 1
            plots = set(r.move(i, (w, h)) for r in self.robots)
            if len(plots) == expected_len:
                # Each robot is on a unique plot; draw picture
                map = [["."] * w for _ in range(h)]
                for x, y in plots:
                    map[y][x] = "x"
                with (out_folder / "picture.txt").open("w") as f:
                    f.writelines(("".join(line) + "\n") for line in map)
                break
        return i
