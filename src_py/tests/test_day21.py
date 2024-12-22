from aoc2024.day21 import D21Step1Puzzle, D21Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD21(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D21Step1Puzzle, "d21.sample.txt", 126384)

    def test_step1_input(self):
        self.check_solution(D21Step1Puzzle, "d21.input.txt", 136780)

    def test_step2_sample(self):
        self.check_solution(D21Step2Puzzle, "d21.sample.txt", 154115708116294)

    def test_step2_input(self):
        self.check_solution(D21Step2Puzzle, "d21.input.txt", 167538833832712)
