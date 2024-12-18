from pathlib import Path

from aoc2024.puzzle import AOCPuzzle
from pytest_multilog import TestHelper


# Base class for AOC puzzles tests
class AOCPuzzleTester(TestHelper):
    INPUTS_ROOT = Path(__file__).parent.parent.parent / "inputs"

    # Access to input file
    def get_input(self, name: str) -> Path:
        return self.INPUTS_ROOT / name

    # Test puzzle solution
    def check_solution(self, puzzle: type[AOCPuzzle], input_name: str, expected_solution: int, solve_arg=None, puzzle_kwargs: dict = None):
        # Solve puzzle
        p = puzzle(self.get_input(input_name)) if puzzle_kwargs is None else puzzle(self.get_input(input_name), **puzzle_kwargs)
        solution = p.solve() if solve_arg is None else p.solve(solve_arg)

        # Verify solution
        assert solution == expected_solution, f"Solution not found (expected: {expected_solution} / found: {solution})"
