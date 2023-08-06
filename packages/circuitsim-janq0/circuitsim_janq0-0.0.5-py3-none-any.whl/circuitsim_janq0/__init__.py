from __future__ import annotations
from abc import ABC, abstractmethod
import argparse
from bidict import bidict
from collections.abc import Mapping
from dataclasses import dataclass, field
import gettext
import logging
import numpy as np
from si_prefix import si_parse, si_format
import si_prefix  # To be able to change the module's constants
from sys import stdin
from tabulate import tabulate


si_prefix.SI_PREFIX_UNITS = "yzafpnum kMGTPEZY"


class Element(ABC):
    """Abstract base class for circuit elements"""

    @abstractmethod
    def stamp(
        self,
        equation: Equation,
        nodes: Mapping,
        branches: Mapping,
    ) -> None:
        """A stamp is the element contribution to the circuit equation

        It also needs to take nodes and branches as arguments, which
        map the circuit nodes and branches to their equation indices.
        """
        pass

    @property
    @abstractmethod
    def nodes(self) -> list:
        """Returns all node connections of the element"""
        pass

    @property
    @abstractmethod
    def branches(self) -> list:
        """Returns all branches of the element"""
        pass


class Resistor(Element):
    def __init__(
        self,
        resistance: float,
        pos_node: str,
        neg_node: str,
        branch: str | None = None,
    ) -> None:
        if resistance < 0:
            raise ValueError("Resistance can't be negative.")
        if resistance == 0:
            raise ValueError(
                "Resistance can't be 0. If you wish to connect two nodes, "
                "merge them into one."
            )

        self.resistance = resistance
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.branch = branch

    def stamp(
        self,
        equation: Equation,
        nodes: Mapping,
        branches: Mapping,
        freq: float = 0,
    ) -> None:
        if self.branch:
            self._stamp_with_current(equation, nodes, branches)
        else:
            self._stamp_without_current(equation, nodes, branches)

    @property
    def nodes(self) -> list:
        return [self.pos_node, self.neg_node]

    @property
    def branches(self) -> list:
        return [self.branch] if self.branch else []

    def _stamp_with_current(
        self, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        branch = branches[self.branch]
        equation.stamp_node_current(1, pos_node, branch)
        equation.stamp_node_current(-1, neg_node, branch)
        equation.stamp_branch_voltage(1, branch, pos_node)
        equation.stamp_branch_voltage(-1, branch, neg_node)
        equation.stamp_branch_current(-self.resistance, branch, branch)

    def _stamp_without_current(
        self, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        conductance = 1 / self.resistance
        equation.stamp_node_voltage(conductance, pos_node, pos_node)
        equation.stamp_node_voltage(-conductance, pos_node, neg_node)
        equation.stamp_node_voltage(-conductance, neg_node, pos_node)
        equation.stamp_node_voltage(conductance, neg_node, neg_node)


class Capacitor(Element):
    def __init__(
        self,
        capacitance: float,
        pos_node: str,
        neg_node: str,
        branch: str | None = None,
    ) -> None:
        if capacitance < 0:
            raise ValueError("Capacitance can't be negative.")
        if capacitance == 0:
            raise ValueError("Capacitance can't be 0")

        self.capacitance = capacitance
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.branch = branch

    def stamp(
        self,
        equation: Equation,
        nodes: Mapping,
        branches: Mapping,
        freq: float = 0,
    ) -> None:
        if self.branch:
            self._stamp_with_current(freq, equation, nodes, branches)
        else:
            self._stamp_without_current(freq, equation, nodes, branches)

    @property
    def nodes(self) -> list:
        return [self.pos_node, self.neg_node]

    @property
    def branches(self) -> list:
        return [self.branch] if self.branch else []

    def _stamp_with_current(
        self, freq, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        branch = branches[self.branch]
        reactance = complex(0, -1 / (2 * np.pi * freq * self.capacitance))
        equation.stamp_node_current(1, pos_node, branch)
        equation.stamp_node_current(-1, neg_node, branch)
        equation.stamp_branch_voltage(1, branch, pos_node)
        equation.stamp_branch_voltage(-1, branch, neg_node)
        equation.stamp_branch_current(-reactance, branch, branch)

    def _stamp_without_current(
        self, freq, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        admittance = complex(0, 2 * np.pi * freq * self.capacitance)
        equation.stamp_node_voltage(admittance, pos_node, pos_node)
        equation.stamp_node_voltage(-admittance, pos_node, neg_node)
        equation.stamp_node_voltage(-admittance, neg_node, pos_node)
        equation.stamp_node_voltage(admittance, neg_node, neg_node)


class Inductor(Element):
    def __init__(
        self,
        inductance: float,
        pos_node: str,
        neg_node: str,
        branch: str | None = None,
    ) -> None:
        if inductance < 0:
            raise ValueError("Inductance can't be negative.")
        if inductance == 0:
            raise ValueError("Inductance can't be 0")

        self.inductance = inductance
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.branch = branch

    def stamp(
        self,
        equation: Equation,
        nodes: Mapping,
        branches: Mapping,
        freq: float = 0,
    ) -> None:
        if freq == 0:
            return

        if self.branch:
            self._stamp_with_current(freq, equation, nodes, branches)
        else:
            self._stamp_without_current(freq, equation, nodes, branches)

    @property
    def nodes(self) -> list:
        return [self.pos_node, self.neg_node]

    @property
    def branches(self) -> list:
        return [self.branch] if self.branch else []

    def _stamp_with_current(
        self, freq, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        branch = branches[self.branch]
        reactance = complex(0, -2 * np.pi * freq * self.inductance)
        equation.stamp_node_current(1, pos_node, branch)
        equation.stamp_node_current(-1, neg_node, branch)
        equation.stamp_branch_voltage(1, branch, pos_node)
        equation.stamp_branch_voltage(-1, branch, neg_node)
        equation.stamp_branch_current(-reactance, branch, branch)

    def _stamp_without_current(
        self, freq, equation: Equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        admittance = complex(0, 1 / (2 * np.pi * freq * self.inductance))
        equation.stamp_node_voltage(admittance, pos_node, pos_node)
        equation.stamp_node_voltage(-admittance, pos_node, neg_node)
        equation.stamp_node_voltage(-admittance, neg_node, pos_node)
        equation.stamp_node_voltage(admittance, neg_node, neg_node)


class VoltageSource(Element):
    def __init__(
        self, voltage: float, pos_node: str, neg_node: str, branch: str
    ):
        self.voltage = voltage
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.branch = branch

    def stamp(
        self,
        equation: Equation,
        nodes: Mapping,
        branches: Mapping,
        freq: float = 0,
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        branch = branches[self.branch]
        equation.stamp_node_current(1, pos_node, branch)
        equation.stamp_node_current(-1, neg_node, branch)
        equation.stamp_branch_voltage(+1, branch, pos_node)
        equation.stamp_branch_voltage(-1, branch, neg_node)
        equation.stamp_branch_consts(self.voltage, branch)

    @property
    def nodes(self) -> list:
        return [self.pos_node, self.neg_node]

    @property
    def branches(self) -> list:
        return [self.branch]


class CurrentSource(Element):
    def __init__(self, current, pos_node, neg_node, branch=None):
        self.current = current
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.branch = branch

    def stamp(
        self, equation, nodes: Mapping, branches: Mapping, freq: float = 0
    ):
        if self.branch:
            self._stamp_with_current(equation, nodes, branches)
        else:
            self._stamp_without_current(equation, nodes, branches)

    @property
    def nodes(self):
        return [self.pos_node, self.neg_node]

    @property
    def branches(self):
        return [self.branch] if self.branch else []

    def _stamp_with_current(
        self, equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        branch = branches[self.branch]
        equation.stamp_node_current(1, pos_node, branch)
        equation.stamp_node_current(-1, neg_node, branch)
        equation.stamp_branch_current(1, branch, branch)
        equation.stamp_branch_consts(self.current, branch)

    def _stamp_without_current(
        self, equation, nodes: Mapping, branches: Mapping
    ) -> None:
        pos_node = nodes[self.pos_node]
        neg_node = nodes[self.neg_node]
        equation.stamp_node_consts(-self.current, pos_node)
        equation.stamp_node_consts(self.current, neg_node)


class Circuit:
    """Representation of the circuit

    Stores all the circuit elements and assigns each node and branch
    an index, that can be used for indexing the rows and columns of
    the Equation matrices. Index of reference_node will always be 0.
    """

    def __init__(self, reference_node: str = "0", freq=0):
        """Creates an empty circuit"""
        if freq < 0:
            raise ValueError("Frequency can't be negative")
        self.freq = freq
        self.elements = []
        self.branches = bidict()
        self.nodes = bidict()
        self.node_count = 0
        self.branch_count = 0
        self._add_node(reference_node)

    def solve(self) -> tuple[str, float]:
        node_voltages, branch_currents = self.form_equation().solve()
        return Solution(
            dict(zip(self.nodes, node_voltages)),
            dict(zip(self.branches, branch_currents)),
            complex=bool(self.freq),
        )

    def add_element(self, element: Element):
        """Adds an element to the circuit

        If the element is connected to now nodes or branches, they
        get a new Equation index in self.nodes or self.branches
        """
        self.elements.append(element)
        for node in element.nodes:
            self._add_node(node)
        for branch in element.branches:
            self._add_branch(branch)

    def form_equation(self) -> Equation:
        """Forms an Equation based on the circuit"""
        equation = Equation(
            self.node_count, self.branch_count, complex_=bool(self.freq)
        )
        for element in self.elements:
            element.stamp(equation, self.nodes, self.branches, freq=self.freq)
        return equation

    def _add_node(self, node: str):
        if node not in self.nodes:
            self.nodes[node] = self.node_count
            self.node_count += 1

    def _add_branch(self, branch: str):
        if branch not in self.branches:
            self.branches[branch] = self.branch_count
            self.branch_count += 1


class Equation:
    """Modified nodal analysis equation"""

    def __init__(self, node_count, branch_count, complex_=False):
        dtype = complex if complex_ else float
        self.node_count = node_count
        self.branch_count = branch_count
        self.size = node_count + branch_count
        self.coeffs = np.zeros((self.size, self.size), dtype="complex_")
        self.consts = np.zeros((self.size))

    def solve(self):
        coeffs0 = np.delete(np.delete(self.coeffs, 0, 0), 0, 1)
        consts0 = np.delete(self.consts, 0, 0)
        return np.split(
            np.insert(np.linalg.solve(coeffs0, consts0), 0, 0, axis=0),
            [self.node_count],
        )

    def stamp_node_voltage(self, value: float, node: int, voltage: int):
        self.coeffs[node, voltage] += value

    def stamp_node_current(self, value: float, node: int, current: int):
        self.coeffs[node, current + self.node_count] += value

    def stamp_branch_voltage(self, value: float, branch: int, voltage: int):
        self.coeffs[self.node_count + branch, voltage] += value

    def stamp_branch_current(self, value: float, branch: int, current: int):
        self.coeffs[
            self.node_count + branch, self.node_count + current
        ] += value

    def stamp_node_consts(self, value: float, node: int):
        self.consts[node] += value

    def stamp_branch_consts(self, value: float, branch: int):
        self.consts[self.node_count + branch] += value


@dataclass
class Solution:
    nodes: dict[str, int] = field(default_factory=dict)
    branches: dict[str, int] = field(default_factory=dict)
    complex: bool = False

    def __str__(self):
        nodes = tabulate(
            self._table_array(self.nodes.items(), "V"),
            headers=["Uzel", "Napětí", "Fáze"],
        )
        branches = tabulate(
            self._table_array(self.branches.items(), "A"),
            headers=["Větev", "Proud", "Fáze"],
        )
        return f"{nodes}\n\n{branches}"

    def _table_array(self, items, unit):
        return (
            [
                (
                    name,
                    Solution._format_value(abs(v), unit),
                    Solution._format_phase(v),
                )
                for name, v in items
            ]
            if self.complex
            else [
                (name, Solution._format_value(v.real, unit))
                for name, v in items
            ]
        )

    @classmethod
    def _format_value(cls, value: float, unit):
        return f"{si_format(value, precision=2)}{unit}"

    @classmethod
    def _format_phase(cls, value: complex):
        return f"{si_format(np.angle(value, deg=True), precision=2)}°"


class IO:
    elements = {
        "R": lambda r, p_n, n_n, br=None: Resistor(
            IO._parse_num(r), p_n, n_n, br
        ),
        "U": lambda v, p_n, n_n, br: VoltageSource(
            IO._parse_num(v), p_n, n_n, br
        ),
        "I": lambda i, p_n, n_n, br=None: CurrentSource(
            IO._parse_num(i), p_n, n_n, br
        ),
        "C": lambda c, p_n, n_n, br=None: Capacitor(
            IO._parse_num(c), p_n, n_n, br
        ),
        "L": lambda l, p_n, n_n, br=None: Inductor(
            IO._parse_num(l), p_n, n_n, br
        ),
    }

    def __init__(self, args: argparse.Namespace):
        self.circuit = Circuit(
            freq=args.frequency, reference_node=args.reference_node
        )
        self._add_elems_from_netlist(args.netlist)

    def print_solution(self):
        print(self.circuit.solve())

    def _add_elems_from_netlist(self, netlist):
        with netlist as f:
            for line in f:
                self._parse_line(line)

    def _parse_line(self, line):
        element, *args = line.split()
        self.circuit.add_element(self.elements[element](*args))

    @classmethod
    def _parse_num(cls, number: str) -> int:
        return si_parse(number)


def main():
    parser = argparse.ArgumentParser(
        description="simulates a linear AC or DC circuit and prints out the output values",
        epilog="If the netlist filename isn't given, the standard input is read.",
    )
    parser.add_argument(
        "netlist",
        type=argparse.FileType(),
        default=stdin,
        nargs="?",
        help="filename of the netlist file",
    )
    parser.add_argument(
        "-r",
        "--reference-node",
        type=str,
        default="0",
        help="the label that will be used as the reference node (0 V) in the netlist",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        type=float,
        default=0,
        help="set the circuit to AC with the given frequency in hertz",
    )
    IO(parser.parse_args()).print_solution()


if __name__ == "__main__":
    main()
