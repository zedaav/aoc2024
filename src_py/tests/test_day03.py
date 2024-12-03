from aoc2024.day03 import D03Step1Puzzle, D03Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD03(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D03Step1Puzzle, "d03.sample.txt", 161)

    def test_step1_input(self):
        self.check_solution(D03Step1Puzzle, "d03.input.txt", 189527826)

    def test_step2_sample(self):
        self.check_solution(D03Step2Puzzle, "d03.sample2.txt", 48)

    def test_step2_input(self):
        self.check_solution(D03Step2Puzzle, "d03.input.txt", 63013756)
