from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/7
"""


class D07Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.input = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str):
        line = super().parse_line(index, line)
        test_value, numbers = line.split(":")
        self.input.append((int(test_value), tuple(int(num) for num in numbers.split())))

    def test(self, target_value: int, numbers: list[int], with_or: bool = False) -> bool:
        if len(numbers) == 0:
            return target_value == 0

        # Can the last operator be *
        candidate_number = numbers[-1]
        if (target_value % candidate_number == 0) and self.test(target_value // candidate_number, numbers[:-1], with_or):
            return True

        # Can the last operator be ||
        if with_or:
            right_operand_size = 10 ** len(str(candidate_number))
            if (target_value % right_operand_size == candidate_number) and self.test(target_value // right_operand_size, numbers[:-1], with_or):
                return True

        # Can the last operator be +
        if target_value >= candidate_number:
            return self.test(target_value - candidate_number, numbers[:-1], with_or)

        # None of the allowed operators work
        return False


class D07Step1Puzzle(D07Puzzle):
    def solve(self) -> int:
        # Go through operators
        total = 0
        for res, numbers in self.input:
            if self.test(res, numbers):
                total += res
        return total


class D07Step2Puzzle(D07Puzzle):
    def solve(self) -> int:
        # Go through operators
        total = 0
        for res, numbers in self.input:
            if self.test(res, numbers, True):
                total += res
        return total
