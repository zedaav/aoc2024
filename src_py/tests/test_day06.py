from aoc2024.day06 import D06Step1Puzzle, D06Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD06(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D06Step1Puzzle, "d06.sample.txt", 41)

    def test_step1_input(self):
        self.check_solution(D06Step1Puzzle, "d06.input.txt", 5199)

    def test_step2_sample(self):
        self.check_solution(D06Step2Puzzle, "d06.sample.txt", 6)

    def test_step2_input(self):
        self.check_solution(D06Step2Puzzle, "d06.input.txt", 1915)
