import logging
import re
from collections import defaultdict
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2024/day/6
"""

MAP_PATTERN = re.compile(r"(#)|(\^)")


class D06Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.obstructions_per_line: dict[int, list[int]] = defaultdict(list)
        self.obstructions_per_col: dict[int, list[int]] = defaultdict(list)
        self.width = 0
        self.height = 0
        self.guardian: tuple[int, int] | None = None
        super().__init__(input_file)
        logging.debug(f"map size: {self.width}x{self.height}")
        logging.debug(f"original guardian position: {self.guardian}")
        assert self.width == self.height
        self.size = self.width

        # Process obstructions per column
        for y, cols in self.obstructions_per_line.items():
            for x in cols:
                self.obstructions_per_col[x].append(y)

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        if len(line):
            self.height += 1
            self.width = len(line)
            for m in MAP_PATTERN.finditer(line):
                if m.group(1):
                    self.obstructions_per_line[index - 1].append(m.start(1))
                elif m.group(2) and (self.guardian is None):
                    self.guardian = (m.start(2), index - 1)

    def all_guard_pos(self, obs_per_col: dict | None = None, obs_per_line: dict | None = None) -> tuple[int, int, Direction]:
        # Initial position
        x, y = self.guardian
        direction = Direction.N
        all_positions = set()
        all_positions.add((x, y, direction))

        # Default to contained dict
        if obs_per_col is None:
            obs_per_col = self.obstructions_per_col
        if obs_per_line is None:
            obs_per_line = self.obstructions_per_line

        # Iterate while not getting out of the map
        while True:
            # Compute obstruction list regarding current direction
            new_direction = direction
            if direction == Direction.N:
                obs = obs_per_col[x]
                to_compare = y
                reverse_compare = True
                vertical = True
            elif direction == Direction.E:
                obs = obs_per_line[y]
                to_compare = x
                reverse_compare = False
                vertical = False
            elif direction == Direction.S:
                obs = obs_per_col[x]
                to_compare = y
                reverse_compare = False
                vertical = True
            elif direction == Direction.W:
                obs = obs_per_line[y]
                to_compare = x
                reverse_compare = True
                vertical = False

            # Iterate on obstructions
            obs = [-1] + obs + [self.size]
            for obs_index in range(len(obs) - 1):
                obs_a, obs_b = obs[obs_index], obs[obs_index + 1]
                if obs_a < to_compare < obs_b:
                    # Reaching next position
                    offset = abs(to_compare - (obs_a if reverse_compare else obs_b)) - 1
                    len_before = len(all_positions)
                    set_before = set(all_positions)
                    if vertical:
                        if reverse_compare:
                            new_set = {(x, y - o, direction) for o in range(1, offset + 1)}
                            all_positions |= {(x, y - o, direction) for o in range(1, offset + 1)}
                            y -= offset
                            if y > 0:
                                new_direction = Direction.E
                        else:
                            new_set = {(x, y + o, direction) for o in range(1, offset + 1)}
                            all_positions |= {(x, y + o, direction) for o in range(1, offset + 1)}
                            y += offset
                            if y < (self.size - 1):
                                new_direction = Direction.W
                    else:
                        if reverse_compare:
                            new_set = {(x - o, y, direction) for o in range(1, offset + 1)}
                            all_positions |= {(x - o, y, direction) for o in range(1, offset + 1)}
                            x -= offset
                            if x > 0:
                                new_direction = Direction.N
                        else:
                            new_set = {(x + o, y, direction) for o in range(1, offset + 1)}
                            all_positions |= {(x + o, y, direction) for o in range(1, offset + 1)}
                            x += offset
                            if x < (self.size - 1):
                                new_direction = Direction.S
                    assert len_before + offset == len(
                        all_positions
                    ), f"loop detected! ({len_before}({set_before}) + ({new_set}) != {len(all_positions)}({all_positions}))"

                    # We're done on this direction
                    break

            # Ready to go out?
            if direction == new_direction:
                # Yes!
                break
            else:
                # Heading to the new direction
                direction = new_direction

        return all_positions


class D06Step1Puzzle(D06Puzzle):
    def solve(self) -> int:
        return len(set([(x, y) for x, y, _ in self.all_guard_pos()]))


class D06Step2Puzzle(D06Puzzle):
    def solve(self) -> int:
        # Get all positions, and build a set of candidate positions for additional obstruction
        candidate_obs = set()
        for x, y, _ in self.all_guard_pos():
            if (x, y) != self.guardian:
                candidate_obs.add((x, y))

        # Iterate on candidates
        loops = 0
        for new_obs_x, new_obs_y in candidate_obs:
            # Add obstruction
            obs_per_col = defaultdict(list)
            for a, b in self.obstructions_per_col.items():
                obs_per_col[a].extend(b)
            obs_per_col[new_obs_x].append(new_obs_y)
            obs_per_col[new_obs_x].sort()
            obs_per_line = defaultdict(list)
            for a, b in self.obstructions_per_line.items():
                obs_per_line[a].extend(b)
            obs_per_line[new_obs_y].append(new_obs_x)
            obs_per_line[new_obs_y].sort()

            # Compute all guards positions
            try:
                self.all_guard_pos(obs_per_col, obs_per_line)
            except AssertionError:
                # If getting here, we've got into a loop
                loops += 1

        return loops
