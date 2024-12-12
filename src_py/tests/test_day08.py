from aoc2024.day08 import D08Step1Puzzle, D08Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD08(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D08Step1Puzzle, "d08.sample.txt", 14)

    def test_step1_input(self):
        self.check_solution(D08Step1Puzzle, "d08.input.txt", 280)

    def test_step2_sample(self):
        self.check_solution(D08Step2Puzzle, "d08.sample.txt", 34)

    def test_step2_input(self):
        self.check_solution(D08Step2Puzzle, "d08.input.txt", 958)
