import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
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
    _a_pin_name: str
    _b_pin_name: str
    _all_pins: dict[str, Pin]
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


class D24Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.all_pins: dict[str, Pin] = {}
        super().__init__(input_file)
        logging.info(f"pins: {len(self.all_pins)}")

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
                    self.all_pins[output_pin_name] = AndGateOutputPin(a_pin_name, b_pin_name, self.all_pins)
                elif operation == "OR":
                    self.all_pins[output_pin_name] = OrGateOutputPin(a_pin_name, b_pin_name, self.all_pins)
                elif operation == "XOR":
                    self.all_pins[output_pin_name] = XorGateOutputPin(a_pin_name, b_pin_name, self.all_pins)
                else:
                    raise ValueError(f"Unknown operation: {operation}")


class D24Step1Puzzle(D24Puzzle):
    def solve(self) -> int:
        # Iterate on pin names starting with "z"
        result = 0
        for z_pin in filter(lambda x: x.startswith("z"), self.all_pins.keys()):
            result |= self.all_pins[z_pin].value << int(z_pin[1:])
        return result


class D24Step2Puzzle(D24Puzzle):
    def solve(self) -> int:
        return 0
