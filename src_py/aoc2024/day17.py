import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/17
"""

REGISTER_PATTERN = re.compile(r"Register ([ABC]): ([\d]+)")
PROGRAM_PATTERN = re.compile(r"Program: ([\d,]+)")
OPERAND_MAP = {4: "A", 5: "B", 6: "C"}


@dataclass
class Computer:
    registers: dict[str, int] = field(default_factory=dict)
    instructions: list[int] = field(default_factory=list)
    outputs: list[int] = field(default_factory=list)
    inst_pointer: int = 0

    def __repr__(self) -> str:
        return f"{self.inst_pointer}/{self.registers}/{self.outputs}"

    def __post_init__(self):
        # Build instructions map
        self.inst_map = {0: self._adv, 1: self._bxl, 2: self._bst, 3: self._jnz, 4: self._bxc, 5: self._out, 6: self._bdv, 7: self._cdv}

    def _combo(self, operand: int) -> int:
        return self.registers[OPERAND_MAP[operand]] if operand in OPERAND_MAP else operand

    def _adv(self, operand: int):
        self.registers["A"] = self.registers["A"] // 2 ** self._combo(operand)

    def _bxl(self, operand: int):
        self.registers["B"] = self.registers["B"] ^ operand

    def _bst(self, operand: int):
        self.registers["B"] = self._combo(operand) % 8

    def _jnz(self, operand: int) -> int | None:
        if self.registers["A"]:
            return operand

    def _bxc(self, operand: int):
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def _out(self, operand: int):
        self.outputs.append(self._combo(operand) % 8)

    def _bdv(self, operand: int):
        self.registers["B"] = self.registers["A"] // 2 ** self._combo(operand)

    def _cdv(self, operand: int):
        self.registers["C"] = self.registers["A"] // 2 ** self._combo(operand)

    def loop(self) -> bool:
        # If instruction pointer overflows, stop here
        if not (0 <= self.inst_pointer < len(self.instructions)):
            return False

        # Exhaust instructions until jumping back to 0
        go_on = True
        while go_on and (0 <= self.inst_pointer < len(self.instructions)):
            # Run pointed instruction
            inst = self.instructions[self.inst_pointer]
            oper = self.instructions[self.inst_pointer + 1]
            next_ptr = self.inst_map[inst](oper)
            if next_ptr is not None:
                self.inst_pointer = next_ptr
                go_on = False
            else:
                self.inst_pointer += 2
        return True

    def process(self):
        while self.loop():
            # Run all loops until program halts
            pass


class D17Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.computer = Computer()
        super().__init__(input_file)
        logging.info(f"init: {self.computer}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = REGISTER_PATTERN.match(line)
        if m is not None:
            self.computer.registers[m.group(1)] = int(m.group(2))
        m = PROGRAM_PATTERN.match(line)
        if m is not None:
            self.computer.instructions.extend([int(n) for n in m.group(1).split(",")])


class D17Step1Puzzle(D17Puzzle):
    def solve(self) -> str:
        self.computer.process()
        return ",".join(map(str, self.computer.outputs))


class D17Step2Puzzle(D17Puzzle):
    def find(self, a: int, solutions: list[int], pos: int = 0):
        computer = Computer({"A": a, "B": 0, "C": 0}, self.computer.instructions)
        computer.loop()
        if computer.outputs[0] != computer.instructions[-(pos + 1)]:
            # mitmatch
            return

        if pos == len(self.computer.instructions) - 1:
            # Ok we're done
            solutions.append(a)
        else:
            for b in range(8):
                # First number ok, find next position
                self.find(a * 8 + b, solutions, pos + 1)

    def solve(self) -> int:
        solutions = []
        for a in range(8):
            self.find(a, solutions)
        return solutions[0]
