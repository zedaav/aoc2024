from aoc2024.day19 import D19Step1Puzzle, D19Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD19(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D19Step1Puzzle, "d19.sample.txt", 6)

    def test_step1_input(self):
        self.check_solution(D19Step1Puzzle, "d19.input.txt", 216)

    def test_step2_sample(self):
        self.check_solution(D19Step2Puzzle, "d19.sample.txt", 16)

    def test_step2_input(self):
        self.check_solution(D19Step2Puzzle, "d19.input.txt", 603191454138773)
