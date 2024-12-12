from aoc2024.day12 import D12Step1Puzzle, D12Step2Puzzle

from tests.base import AOCPuzzleTester


class TestD12(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D12Step1Puzzle, "d12.sample.txt", 140)

    def test_step1_sample2(self):
        self.check_solution(D12Step1Puzzle, "d12.sample2.txt", 772)

    def test_step1_sample3(self):
        self.check_solution(D12Step1Puzzle, "d12.sample3.txt", 1930)

    def test_step1_input(self):
        self.check_solution(D12Step1Puzzle, "d12.input.txt", 1377008)

    def test_step2_sample(self):
        self.check_solution(D12Step2Puzzle, "d12.sample.txt", 80)

    def test_step2_sample2(self):
        self.check_solution(D12Step2Puzzle, "d12.sample2.txt", 436)

    def test_step2_sample3(self):
        self.check_solution(D12Step2Puzzle, "d12.sample3.txt", 1206)

    def test_step2_sample4(self):
        self.check_solution(D12Step2Puzzle, "d12.sample4.txt", 236)

    def test_step2_sample5(self):
        self.check_solution(D12Step2Puzzle, "d12.sample5.txt", 368)

    def test_step2_input(self):
        self.check_solution(D12Step2Puzzle, "d12.input.txt", 815788)
