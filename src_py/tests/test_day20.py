from aoc2024.day20 import D20Step1Puzzle, D20Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD20(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D20Step1Puzzle, "d20.sample.txt", 16, solve_arg=6)

    def test_step1_input(self):
        self.check_solution(D20Step1Puzzle, "d20.input.txt", 1530, solve_arg=100)

    def test_step2_sample(self):
        self.check_solution(D20Step2Puzzle, "d20.sample.txt", 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3, solve_arg=50)

    def test_step2_input(self):
        self.check_solution(D20Step2Puzzle, "d20.input.txt", 1033983, solve_arg=100)
