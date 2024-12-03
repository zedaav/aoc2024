import re
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/2
"""

PATTERN = re.compile(r"(\d+)")


class D02Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.safe_count = 0
        self.still_unsafe = []
        super().__init__(input_file)

    def solve(self) -> int:
        # Simply get count
        return self.safe_count

    def is_safe(self, levels: list[int]) -> bool:
        is_raising = None
        previous_nb = None
        for nb in levels:
            if previous_nb is not None:
                if is_raising is None:
                    if nb > previous_nb:
                        is_raising = True
                    elif nb < previous_nb:
                        is_raising = False
                    else:
                        return False

                if ((nb > previous_nb) and (not is_raising)) or ((nb < previous_nb) and (is_raising)) or (nb == previous_nb):
                    return False
                if abs(nb - previous_nb) > 3:
                    return False
            previous_nb = nb
        return True

    def parse_line(self, index: int, line: str):
        levels = list(map(lambda p: int(p.group(1)), PATTERN.finditer(line)))
        if self.is_safe(levels):
            self.safe_count += 1
        else:
            self.still_unsafe.append(levels)


class D02Step1Puzzle(D02Puzzle):
    pass


class D02Step2Puzzle(D02Puzzle):
    def solve(self) -> int:
        # 2nd run to tentatively the ones that are still unsafe
        for levels in self.still_unsafe:
            # Try to remove one level, one at a time
            for candidate_index in range(len(levels)):
                updated_levels = levels[0:candidate_index] + levels[candidate_index + 1 :]
                if self.is_safe(updated_levels):
                    # Safe by removing only one level: ok, that's safe as well
                    self.safe_count += 1
                    break

        return super().solve()
