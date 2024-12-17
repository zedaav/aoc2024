from aoc2024.day17 import D17Step1Puzzle, D17Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD17(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D17Step1Puzzle, "d17.sample.txt", "4,6,3,5,6,3,5,2,1,0")

    def test_step1_sample2(self):
        self.check_solution(D17Step1Puzzle, "d17.sample2.txt", "4,2,5,6,7,7,7,7,3,1,0")

    def test_step1_input(self):
        self.check_solution(D17Step1Puzzle, "d17.input.txt", "7,6,5,3,6,5,7,0,4")

    def test_step2_sample3(self):
        self.check_solution(D17Step2Puzzle, "d17.sample3.txt", 117440)

    def test_step2_input(self):
        self.check_solution(D17Step2Puzzle, "d17.input.txt", 190615597431823)
