import logging
import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

from aoc2024.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2024/day/24
"""

PIN_PATTERN = re.compile(r"([a-z\d]+): ([\d]+)")
GATE_PATTERN = re.compile(r"([a-z\d]+) (AND|OR|XOR) ([a-z\d]+) -> ([a-z\d]+)")


# Pin interface
class Pin(ABC):
    @property
    @abstractmethod
    def value(self) -> bool:  # pragma: no cover
        pass


# Input pin
@dataclass
class InputPin(Pin):
    _value: bool

    @property
    def value(self) -> bool:
        return self._value


# Gate output pin
@dataclass
class GateOutputPin(Pin, ABC):
    name: str
    _a_pin_name: str
    _b_pin_name: str
    _all_pins: dict[str, Pin] = field(default_factory=dict)
    _a_pin: Pin | None = None
    _b_pin: Pin | None = None

    @property
    def a(self) -> Pin:
        if self._a_pin is None:
            self._a_pin = self._all_pins[self._a_pin_name]
        return self._a_pin

    @property
    def b(self) -> Pin:
        if self._b_pin is None:
            self._b_pin = self._all_pins[self._b_pin_name]
        return self._b_pin

    @abstractmethod
    def operate(self) -> bool:  # pragma: no cover
        pass

    @property
    def value(self) -> bool:
        return self.operate()


# AND Gate
class AndGateOutputPin(GateOutputPin):
    def operate(self) -> bool:
        return self.a.value & self.b.value


# OR Gate
class OrGateOutputPin(GateOutputPin):
    def operate(self) -> bool:
        return self.a.value | self.b.value


# XOR Gate
class XorGateOutputPin(GateOutputPin):
    def operate(self) -> bool:
        return self.a.value ^ self.b.value


# Computer system, holding all pins
@dataclass
class Computer:
    _all_pins: dict[str, Pin]

    def __post_init__(self):
        # Inject the pins map in all gate output pins
        for pin in self._all_pins.values():
            if isinstance(pin, GateOutputPin):
                pin._all_pins = self._all_pins

    def _width(self, prefix: str) -> int:
        return max(map(lambda x: int(x[1:]), filter(lambda x: x.startswith(prefix), self._all_pins.keys()))) + 1

    def __repr__(self) -> str:
        return f"computer with {len(self._all_pins)} pins ({len(self.gates)} gates), {self.x_width} bits x {self.y_width} bits inputs, and {self.z_width} bits output"

    @property
    def x_width(self) -> int:
        return self._width("x")

    @property
    def y_width(self) -> int:
        return self._width("y")

    @property
    def z_width(self) -> int:
        return self._width("z")

    @property
    def gates(self) -> list[GateOutputPin]:
        return [pin for pin in self._all_pins.values() if isinstance(pin, GateOutputPin)]

    def _int(self, prefix: str) -> int:
        result = 0
        for x_name, x_pin in filter(lambda x: x[0].startswith(prefix), self._all_pins.items()):
            result |= int(x_pin.value) << int(x_name[1:])
        return result

    def compute(self):
        return self._int("z")

    @property
    def x(self) -> int:
        return self._int("x")

    @property
    def y(self) -> int:
        return self._int("y")


class D24Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.all_pins: dict[str, Pin] = {}
        super().__init__(input_file)
        self.default_computer = Computer(self.all_pins.copy())
        logging.info(f"default: {self.default_computer}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = PIN_PATTERN.match(line)
        if m:
            pin_name, value = m.groups()
            self.all_pins[pin_name] = InputPin(value == "1")
        else:
            m = GATE_PATTERN.match(line)
            if m:
                a_pin_name, operation, b_pin_name, output_pin_name = m.groups()
                if operation == "AND":
                    self.all_pins[output_pin_name] = AndGateOutputPin(output_pin_name, a_pin_name, b_pin_name)
                elif operation == "OR":
                    self.all_pins[output_pin_name] = OrGateOutputPin(output_pin_name, a_pin_name, b_pin_name)
                elif operation == "XOR":
                    self.all_pins[output_pin_name] = XorGateOutputPin(output_pin_name, a_pin_name, b_pin_name)
                else:
                    raise ValueError(f"Unknown operation: {operation}")


class D24Step1Puzzle(D24Puzzle):
    def solve(self) -> int:
        # Run the default computer
        return self.default_computer.compute()


class D24Step2Puzzle(D24Puzzle):
    def solve(self, args: tuple[int, Callable]) -> str:
        n, check = args

        # Iterate on all gates combinations of N pairs (with no duplicates)
        gates_names = [g.name for g in self.default_computer.gates]
        pairs = list(combinations(gates_names, 2))
        for combo in filter(lambda c: len([a for b in c for a in b]) == len(set(a for b in c for a in b)), combinations(pairs, n)):
            # Build a new computer with swapped gates
            logging.debug(f"Trying {combo}")

            # Copy the default computer, and swap gates
            computer_candidate = Computer(self.all_pins.copy())
            for a, b in combo:
                computer_candidate._all_pins[a], computer_candidate._all_pins[b] = computer_candidate._all_pins[b], computer_candidate._all_pins[a]

            # Check if the new computer is valid, by testing the output
            if computer_candidate.compute() == check(computer_candidate.x, computer_candidate.y):
                return ",".join(sorted([a for b in combo for a in b]))
