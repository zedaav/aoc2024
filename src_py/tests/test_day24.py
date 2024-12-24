from aoc2024.day24 import D24Step1Puzzle, D24Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD24(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D24Step1Puzzle, "d24.sample.txt", 4)

    def test_step1_sample2(self):
        self.check_solution(D24Step1Puzzle, "d24.sample2.txt", 2024)

    def test_step1_input(self):
        self.check_solution(D24Step1Puzzle, "d24.input.txt", 59619940979346)

    def test_step2_sample(self):
        self.check_solution(D24Step2Puzzle, "d24.sample.txt", "co,de,ka,ta")

    def test_step2_input(self):
        self.check_solution(D24Step2Puzzle, "d24.input.txt", "az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy")
