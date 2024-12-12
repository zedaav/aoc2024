from collections import defaultdict
from pathlib import Path

from aoc2024.puzzle import CARDINAL_DIRS, OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2024/day/12
"""

PREVIOUS_OFFSETS = [OFFSETS[d] for d in [Direction.W, Direction.N]]


class Region:
    def __init__(self, type: str):
        self.type = type
        self.plots = set()
        self.edges = set()
        self._valid_edges = None

    def add(self, x: int, y: int):
        self.plots.add((x, y))
        self.edges |= set((x + dx, y + dy, d) for d, (dx, dy) in map(lambda e: (e, OFFSETS[e]), CARDINAL_DIRS))

    def merge(self, other: object):
        # Merge other region plots and edges into this one
        self.plots |= other.plots
        self.edges |= other.edges

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def valid_edges(self) -> set[tuple[int, int, Direction]]:
        if self._valid_edges is None:
            self._valid_edges = list(filter(lambda t: (t[0], t[1]) not in self.plots, self.edges))
        return self._valid_edges

    @property
    def perimeter(self) -> int:
        # Count all edges that are not plots
        return len(self.valid_edges)

    @property
    def sides_nb(self) -> int:
        # Map valid edges to count distinct sides
        sides: dict[Direction, dict[int, list[int]]] = defaultdict(lambda: defaultdict(list))
        for x, y, d in self.valid_edges:
            sides[d][x if d in [Direction.E, Direction.W] else y].append(y if d in [Direction.E, Direction.W] else x)
        count = 0
        for a in sides.values():
            for b in a.values():
                all_pos = sorted(b)
                count += 1
                for i in range(len(all_pos) - 1):
                    if abs(all_pos[i] - all_pos[i + 1]) != 1:
                        count += 1
        return count

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    @property
    def discount_price(self) -> int:
        return self.area * self.sides_nb


class D12Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.regions: dict[str, dict[tuple[int, int], Region]] = defaultdict(dict)
        self.all_regions: list[Region] = []
        super().__init__(input_file)

        # Iterate on lines to fill regions
        for y, line in enumerate(self.input_lines):
            for x, type in enumerate(line):
                # Find any previously defined region
                previous_region = None
                for dx, dy in PREVIOUS_OFFSETS:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in self.regions[type]:
                        if previous_region is None:
                            previous_region = self.regions[type][(nx, ny)]
                        else:
                            # 2 previous regions
                            candidate_region = self.regions[type][(nx, ny)]

                            # Not the same?
                            if previous_region != candidate_region:
                                # Merge them
                                previous_region.merge(candidate_region)

                                # All positions pointing to candidate region are relocated to the merged one
                                for plot in candidate_region.plots:
                                    self.regions[type][plot] = previous_region

                                # Forget candidate region
                                self.all_regions.remove(candidate_region)
                region = previous_region

                # ... or create a new one
                if region is None:
                    region = Region(type)
                    self.all_regions.append(region)

                # Remember it for this position
                self.regions[type][(x, y)] = region

                # Add plot
                region.add(x, y)


class D12Step1Puzzle(D12Puzzle):
    def solve(self) -> int:
        return sum(r.price for r in self.all_regions)


class D12Step2Puzzle(D12Puzzle):
    def solve(self) -> int:
        return sum(r.discount_price for r in self.all_regions)
