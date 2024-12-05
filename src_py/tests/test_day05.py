from aoc2024.day05 import D05Step1Puzzle, D05Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD05(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D05Step1Puzzle, "d05.sample.txt", 143)

    def test_step1_input(self):
        self.check_solution(D05Step1Puzzle, "d05.input.txt", 5651)

    def test_step2_sample(self):
        self.check_solution(D05Step2Puzzle, "d05.sample.txt", 123)

    def test_step2_input(self):
        self.check_solution(D05Step2Puzzle, "d05.input.txt", 4743)
