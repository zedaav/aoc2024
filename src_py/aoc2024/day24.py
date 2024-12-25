import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
    _x: int | None = None
    _y: int | None = None
    _z: int | None = None
    _cached_pins_per_op: dict[tuple[str, str, type[GateOutputPin]], str] = field(default_factory=dict)

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
        if self._z is None:
            self._z = self._int("z")
        return self._z

    @property
    def x(self) -> int:
        if self._x is None:
            self._x = self._int("x")
        return self._x

    @property
    def y(self) -> int:
        if self._y is None:
            self._y = self._int("y")
        return self._y

    def find_gate(self, a_pin_name: str, b_pin_name: str, gate_type: type[GateOutputPin]) -> str:
        for pin in self.gates:
            if isinstance(pin, gate_type) and (
                (pin._a_pin_name == a_pin_name and pin._b_pin_name == b_pin_name) or (pin._a_pin_name == b_pin_name and pin._b_pin_name == a_pin_name)
            ):
                return pin.name

        return None

    def swap(self, a_pin_name: str, b_pin_name: str):
        a_pin = self._all_pins[a_pin_name]
        b_pin = self._all_pins[b_pin_name]
        self._all_pins[a_pin_name] = b_pin
        self._all_pins[b_pin_name] = a_pin
        a_pin.name = b_pin_name
        b_pin.name = a_pin_name
        self._z = None


class D24Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.all_pins: dict[str, Pin] = {}
        super().__init__(input_file)
        self.computer = Computer(self.all_pins)
        logging.info(f"default: {self.computer}")

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
        return self.computer.compute()


class D24Step2Puzzle(D24Puzzle):
    def solve(self) -> str:
        # Expected result
        expected_result = self.computer.x + self.computer.y
        current_result = self.computer.compute()
        logging.info(f"expected: {expected_result} ({bin(expected_result)}), current: {current_result} ({bin(current_result)})")

        # Iterate on all bits
        wrong_gates = set()
        carry = None
        for i in range(self.computer.z_width):
            # Main inputs and output for this iteration
            x = f"x{i:02}"
            y = f"y{i:02}"
            z = f"z{i:02}"

            # Find base gates for inputs
            x_xor_y = self.computer.find_gate(x, y, XorGateOutputPin)
            x_and_y = self.computer.find_gate(x, y, AndGateOutputPin)

            # Check if carry is known at this level
            if not carry:
                # Not yet (first level); nothing more to do
                carry = x_and_y
                continue

            # Check for a XOR gate between carry and x_xor_y
            candidate_xor = self.computer.find_gate(carry, x_xor_y, XorGateOutputPin)
            if candidate_xor is None:
                # Not found: check missing wires
                z_gate = self.computer._all_pins[z]
                bad_wires = list(set([carry, x_xor_y]) ^ set([z_gate._a_pin_name, z_gate._b_pin_name]))
                if len(bad_wires) == 2:
                    a, b = bad_wires
                    logging.info(f"bit {i}: wrong pins: {a} and {b}")
                    wrong_gates.add(a)
                    wrong_gates.add(b)
                    self.computer.swap(a, b)
            elif candidate_xor != z:
                # Not correctly wired
                logging.info(f"bit {i}: wrong pins: {z} and {candidate_xor}")
                wrong_gates.add(z)
                wrong_gates.add(candidate_xor)
                self.computer.swap(z, candidate_xor)

            # Update base gates for inputs
            x_xor_y = self.computer.find_gate(x, y, XorGateOutputPin)
            x_and_y = self.computer.find_gate(x, y, AndGateOutputPin)

            # Update carry
            carry = self.computer.find_gate(carry, x_xor_y, AndGateOutputPin)
            carry = self.computer.find_gate(carry, x_and_y, OrGateOutputPin)

        # Just print wrong gates
        return ",".join(sorted(wrong_gates))
