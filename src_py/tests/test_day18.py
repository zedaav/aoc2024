from aoc2024.day18 import D18Step1Puzzle, D18Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD18(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D18Step1Puzzle, "d18.sample.txt", 22, puzzle_kwargs={"target": (6, 6)}, solve_arg=12)

    def test_step1_input(self):
        self.check_solution(D18Step1Puzzle, "d18.input.txt", 312, puzzle_kwargs={"target": (70, 70)}, solve_arg=1024)

    def test_step2_sample(self):
        self.check_solution(D18Step2Puzzle, "d18.sample.txt", "6,1", puzzle_kwargs={"target": (6, 6)}, solve_arg=12)

    def test_step2_input(self):
        self.check_solution(D18Step2Puzzle, "d18.input.txt", "28,26", puzzle_kwargs={"target": (70, 70)}, solve_arg=1024)
