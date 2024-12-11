from aoc2024.day10 import D10Step1Puzzle, D10Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD10(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D10Step1Puzzle, "d10.sample.txt", 36)

    def test_step1_input(self):
        self.check_solution(D10Step1Puzzle, "d10.input.txt", 667)

    def test_step2_sample(self):
        self.check_solution(D10Step2Puzzle, "d10.sample.txt", 81)

    def test_step2_input(self):
        self.check_solution(D10Step2Puzzle, "d10.input.txt", 1344)
