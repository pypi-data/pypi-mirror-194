import pytest as pt
import numpy as np
import numpy.testing as npt

from circuitsim_janq0 import (
    Circuit,
    Resistor,
    Element,
    Equation,
    VoltageSource,
    Solution,
    CurrentSource,
    Capacitor,
)


@pt.fixture
def singleton_element():
    class E(Element):
        def __init__(self, node: str, branch: str):
            self.node = node
            self.branch = branch

        def stamp(self, equation: Equation, nodes, branches, freq=0):
            node = nodes[self.node]
            branch = branches[self.branch]
            equation.stamp_node_voltage(1, node, node)
            equation.stamp_node_current(-1, node, branch)
            equation.stamp_branch_voltage(-1, branch, node)
            equation.stamp_branch_current(1, branch, branch)
            equation.stamp_node_consts(1, node)
            equation.stamp_branch_consts(-1, branch)

        @property
        def nodes(self):
            return [self.node]

        @property
        def branches(self):
            return [self.branch]

    return E


@pt.fixture
def circuit1(singleton_element):
    circuit = Circuit()
    circuit.add_element(singleton_element("0", "a"))
    circuit.add_element(singleton_element("0", "b"))
    circuit.add_element(singleton_element("B", "b"))
    return circuit


@pt.fixture
def voltage_source_resistor_circuit():
    circuit = Circuit()
    circuit.add_element(VoltageSource(10, "A", "0", "I"))
    circuit.add_element(Resistor(100, "A", "0"))
    return circuit


class TestResistor:
    def test_negative_resistance_raises_value_error(self):
        with pt.raises(ValueError):
            resistor = Resistor(-100, "A", "B")

    def test_zero_resistance_raises_value_error(self):
        with pt.raises(ValueError):
            resistor = Resistor(0, "A", "B")

    def test_stamp_with_current(self):
        equation = Equation(2, 1)
        Resistor(99, "A", "R", "I").stamp(equation, {"R": 0, "A": 1}, {"I": 0})
        npt.assert_array_equal(
            equation.coeffs, [[0, 0, -1], [0, 0, 1], [-1, 1, -99]]
        )

    def test_stamp_without_current(self):
        equation = Equation(2, 1)
        Resistor(99, "A", "R").stamp(equation, {"R": 0, "A": 1}, {"I": 0})
        npt.assert_array_equal(
            equation.coeffs,
            [[1 / 99, -1 / 99, 0], [-1 / 99, 1 / 99, 0], [0, 0, 0]],
        )


class TestCurrentSource:
    def test_init_without_current(self):
        i = CurrentSource(0.13, "A", "B")
        assert i.current == 0.13
        assert i.pos_node == "A"
        assert i.neg_node == "B"

    def test_stamp_without_current(self):
        i = CurrentSource(10, "A", "0")
        eq = Equation(2, 0)
        i.stamp(eq, {"A": 1, "0": 0}, {})
        npt.assert_array_equal(eq.consts, [10, -10])

    def test_stamp_with_current(self):
        i = CurrentSource(10, "A", "0", "I")
        eq = Equation(2, 1)
        i.stamp(eq, {"A": 1, "0": 0}, {"I": 0})
        npt.assert_array_equal(eq.consts, [0, 0, 10])
        npt.assert_array_equal(eq.coeffs, [[0, 0, -1], [0, 0, 1], [0, 0, 1]])


class TestVoltageSource:
    def test_stamp(self):
        equation = Equation(2, 1)
        VoltageSource(12, "A", "R", "I").stamp(
            equation, {"R": 0, "A": 1}, {"I": 0}
        )
        npt.assert_array_equal(
            equation.coeffs, [[0, 0, -1], [0, 0, 1], [-1, 1, 0]]
        )
        npt.assert_array_equal(equation.consts, [0, 0, 12])


class TestCapacitor:
    def test_stamp_without_current(self):
        equation = Equation(2, 0)
        Capacitor(1.5915494e-3, "A", "R").stamp(
            equation, {"R": 0, "A": 1}, {}, freq=100.0
        )
        npt.assert_array_almost_equal(equation.coeffs, [[1j, -1j], [-1j, 1j]])


class TestCircuit:
    def test_adding_existent_node_wont_do_anything(self, singleton_element):
        element1 = singleton_element("A", "a")
        element2 = singleton_element("A", "b")
        circuit1 = Circuit()
        circuit1.add_element(element1)
        circuit2 = Circuit()
        circuit2.add_element(element1)
        circuit2.add_element(element2)
        assert circuit1.nodes == circuit2.nodes

    def test_adding_existent_branch_wont_do_anything(self, singleton_element):
        element1 = singleton_element("A", "a")
        element2 = singleton_element("B", "a")
        circuit1 = Circuit()
        circuit1.add_element(element1)
        circuit2 = Circuit()
        circuit2.add_element(element1)
        circuit2.add_element(element2)
        assert circuit1.branches == circuit2.branches

    def test_new_node_will_have_incremented_value(self, singleton_element):
        element1 = singleton_element("0", "a")
        element2 = singleton_element("A", "b")
        circuit = Circuit()
        circuit.add_element(element1)
        circuit.add_element(element2)
        assert circuit.nodes == {"0": 0, "A": 1}

    def test_new_branch_will_have_incremented_value(self, singleton_element):
        element1 = singleton_element("A", "a")
        element2 = singleton_element("B", "b")
        circuit = Circuit()
        circuit.add_element(element1)
        circuit.add_element(element2)
        assert circuit.branches == {"a": 0, "b": 1}

    def test_add_element_will_add_it(self, singleton_element):
        element1 = singleton_element("A", "a")
        circuit = Circuit()
        circuit.add_element(element1)
        assert circuit.elements == [element1]

    def test_form_equation_gives_good_coeffs(self, circuit1):
        equation = circuit1.form_equation()
        npt.assert_array_equal(
            np.array(equation.coeffs),
            np.array(
                [
                    [2.0, 0.0, -1.0, -1.0],
                    [0.0, 1.0, 0.0, -1.0],
                    [-1.0, 0.0, 1.0, 0.0],
                    [-1.0, -1.0, 0.0, 2.0],
                ]
            ),
        )

    def test_form_equation_gives_good_coeffs(self, circuit1):
        equation = circuit1.form_equation()
        npt.assert_array_equal(
            np.array(equation.consts),
            np.array([2, 1, -1, -2]),
        )


class TestEquation:
    def test_solve_circuit1(self, circuit1):
        equation = circuit1.form_equation()
        npt.assert_array_equal(equation.solve(), [[0, 0], [-1, -1]])

    def test_solve_voltage_source_resistor_circuit(
        self, voltage_source_resistor_circuit
    ):
        eq = voltage_source_resistor_circuit.form_equation()
        voltages, currents = eq.solve()
        npt.assert_array_equal(voltages, np.array([0, 10]))
        npt.assert_array_equal(currents, np.array([-0.1]))
