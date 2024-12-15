from aoc2024.day15 import D15Step1Puzzle, D15Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD15(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D15Step1Puzzle, "d15.sample.txt", 2028)

    def test_step1_sample2(self):
        self.check_solution(D15Step1Puzzle, "d15.sample2.txt", 10092)

    def test_step1_input(self):
        self.check_solution(D15Step1Puzzle, "d15.input.txt", 1383666)

    def test_step2_sample2(self):
        self.check_solution(D15Step2Puzzle, "d15.sample2.txt", 9021)

    def test_step2_sample3(self):
        self.check_solution(D15Step2Puzzle, "d15.sample3.txt", 105 + 207 + 306)

    def test_step2_input(self):
        self.check_solution(D15Step2Puzzle, "d15.input.txt", 1412866)
