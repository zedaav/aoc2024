from aoc2024.day13 import D13Step1Puzzle, D13Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD13(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D13Step1Puzzle, "d13.sample.txt", 480)

    def test_step1_input(self):
        self.check_solution(D13Step1Puzzle, "d13.input.txt", 29522)

    def test_step2_sample(self):
        self.check_solution(D13Step2Puzzle, "d13.sample.txt", 875318608908)

    def test_step2_input(self):
        self.check_solution(D13Step2Puzzle, "d13.input.txt", 101214869433312)
