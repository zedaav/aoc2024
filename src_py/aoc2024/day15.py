import logging
import re
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from queue import Queue

from aoc2024.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2024/day/15
"""

DIRECTION_MAP = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}


@dataclass
class Box:
    plots: list[tuple[int, int]]
    all_boxes: dict[tuple[int, int], object]
    obstacles: set[tuple[int, int]]

    def __repr__(self) -> str:
        return f"{self.plots}"

    def __eq__(self, value):
        if isinstance(value, Box):
            return self.plots == value.plots
        return False

    def __ne__(self, value):
        if isinstance(value, Box):
            return not (self.plots == value.plots)
        return True

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def pos(self) -> int:
        x, y = self.plots[0]
        return 100 * y + x

    def can_move(self, offset: tuple[int, int], recursive: bool = True) -> set[object]:
        dx, dy = offset
        candidates = []
        for x, y in self.plots:
            cx, cy = x + dx, y + dy
            candidates.append((cx, cy))
        moveable_ones = set()

        # Iterate on candidates positions
        for cx, cy in candidates:
            # If there is an obstacle in candidate position: nothing to do
            if (cx, cy) in self.obstacles:
                return set()

            # If the candidate position is actually the other box part, just continue (the other part will tell if the move is possible)
            if (cx, cy) in self.plots:
                continue

            # If there is another box in candidate position: try to move it as well
            if (cx, cy) in self.all_boxes:
                # In non-recursive mode: just stop here
                if not recursive:
                    return set()

                # In recursive mode, check if other boxes can move as well
                to_move = self.all_boxes[(cx, cy)].can_move(offset)
                if to_move:
                    # Add to moveable boxes
                    moveable_ones |= to_move
                else:
                    # Can't move
                    return set()

        # If we get here, we can move this instance
        moveable_ones.add(self)
        return moveable_ones

    def move_all(self, offset: tuple[int, int]) -> bool:
        # Get moveable boxes, and move them
        q = Queue()
        for b in self.can_move(offset):
            q.put(b)
        has_moved = not q.empty()
        while not q.empty():
            b = q.get()
            if b.can_move(offset, recursive=False):
                # Yes, this one can move first
                b.move(offset)
            else:
                # Wait for other boxes to move first
                q.put(b)
        return has_moved

    def move(self, offset: tuple[int, int]):
        # Move this box
        dx, dy = offset
        to_move = self.plots
        self.plots = []

        for x, y in to_move:
            cx, cy = x + dx, y + dy
            self.plots.append((cx, cy))
            del self.all_boxes[(x, y)]
        for cx, cy in self.plots:
            self.all_boxes[(cx, cy)] = self


class D15Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.robot: tuple[int, int] = None
        self.boxes: dict[tuple[int, int], Box] = {}
        self.obstacles: set[tuple[int, int]] = set()
        self.moves: list[Direction] = []
        self.width = None
        self.height = 0
        super().__init__(input_file)
        logging.info(f"robot: {self.robot}")
        logging.info(f"boxes: {self.boxes}")
        logging.info(f"obstacles: {self.obstacles}")
        logging.info(f"map: {self.width}x{self.height}")
        logging.info(f"parsed {len(self.moves)} move instructions")

    @abstractmethod
    def is_wide(self) -> bool:
        pass

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        is_wide = self.is_wide()
        if line.startswith("#"):
            self.width = len(line) * (2 if is_wide else 1)
            self.height += 1
            if "@" in line:
                self.robot = (line.index("@") * (2 if is_wide else 1), index - 1)
            for x in re.finditer("O", line):
                b = (
                    Box([(x.start() * 2, index - 1), (x.start() * 2 + 1, index - 1)], self.boxes, self.obstacles)
                    if is_wide
                    else Box([(x.start(), index - 1)], self.boxes, self.obstacles)
                )
                for p in b.plots:
                    self.boxes[p] = b
            for x in re.finditer("#", line):
                self.obstacles.add((x.start() * (2 if is_wide else 1), index - 1))
                if is_wide:
                    self.obstacles.add((x.start() * 2 + 1, index - 1))
        elif line:
            self.moves.extend([DIRECTION_MAP[x] for x in line])

    def solve(self) -> int:
        # Iterate on moves

        for offset in map(lambda d: OFFSETS[d], self.moves):
            # Candidate new position for robot
            ox, oy = self.robot
            dx, dy = offset
            cx, cy = ox + dx, oy + dy

            # If there is an obstacle in candidate position: nothing to do
            if (cx, cy) in self.obstacles:
                continue

            # If there is a box in candidate position: check if it can be moved
            if (cx, cy) in self.boxes and not self.boxes[(cx, cy)].move_all(offset):
                # No, so nothing to do
                continue

            # Finally, if we get here, this is a valid move
            self.robot = (cx, cy)

        # Sum boxes positions
        all_boxes = set(self.boxes.values())
        logging.info(f"final robot position: {self.robot}")
        logging.info(f"final boxes positions: {all_boxes}")
        return sum(b.pos for b in all_boxes)


class D15Step1Puzzle(D15Puzzle):
    def is_wide(self) -> bool:
        return False


class D15Step2Puzzle(D15Puzzle):
    def is_wide(self) -> bool:
        return True
