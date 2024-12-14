from aoc2024.day14 import D14Step1Puzzle, D14Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD14(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D14Step1Puzzle, "d14.sample.txt", 12, solve_arg=(11, 7))

    def test_step1_input(self):
        self.check_solution(D14Step1Puzzle, "d14.input.txt", 214109808, solve_arg=(101, 103))

    def test_step2_input(self):
        self.check_solution(D14Step2Puzzle, "d14.input.txt", 7687, solve_arg=self.test_folder)
