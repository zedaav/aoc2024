from aoc2024.day22 import D22Step1Puzzle, D22Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD22(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D22Step1Puzzle, "d22.sample.txt", 37327623)

    def test_step1_input(self):
        self.check_solution(D22Step1Puzzle, "d22.input.txt", 20068964552)

    def test_step2_sample2(self):
        self.check_solution(D22Step2Puzzle, "d22.sample2.txt", 23)

    def test_step2_input(self):
        self.check_solution(D22Step2Puzzle, "d22.input.txt", 2246)
