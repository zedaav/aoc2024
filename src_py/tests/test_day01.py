from aoc2024.day01 import D01Step1Puzzle, D01Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD01(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D01Step1Puzzle, "d01.sample.txt", 11)

    def test_step1_input(self):
        self.check_solution(D01Step1Puzzle, "d01.input.txt", 1882714)

    def test_step2_sample(self):
        self.check_solution(D01Step2Puzzle, "d01.sample.txt", 31)

    def test_step2_input(self):
        self.check_solution(D01Step2Puzzle, "d01.input.txt", 19437052)
