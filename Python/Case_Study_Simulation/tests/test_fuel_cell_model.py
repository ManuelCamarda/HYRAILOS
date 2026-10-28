"""Run with: python -m unittest discover -s tests -v (from the case directory)."""

import unittest
from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from pyomo.environ import ConcreteModel, Var, value

from data_carriage import load_carriage_data_1
from fuel_cell_model import (
    FLOW_BRIDGE_COEFFICIENTS, LOW_LOAD_EFFICIENCY,
    TRANSITION_LOW_PLR, TRANSITION_HIGH_PLR,
    fuel_cell_efficiency, hydrogen_mass_flow, normalized_hydrogen_flow,
    polynomial_efficiency, pyomo_hydrogen_mass_flow,
    validate_fuel_cell_parameters,
)


class FuelCellModelTests(unittest.TestCase):
    def test_zero_and_negative_measurement(self):
        self.assertEqual(hydrogen_mass_flow(0.0, 100e3, 120e6), 0.0)
        self.assertEqual(hydrogen_mass_flow(-1e-6, 100e3, 120e6), 0.0)
        self.assertEqual(fuel_cell_efficiency(0.0), LOW_LOAD_EFFICIENCY)

    def test_published_branches(self):
        low = np.array([0.0, 0.01, 0.03])
        np.testing.assert_allclose(fuel_cell_efficiency(low), LOW_LOAD_EFFICIENCY)
        high = np.array([0.07, 0.1, 0.2, 0.5, 1.0])
        np.testing.assert_allclose(fuel_cell_efficiency(high), polynomial_efficiency(high))

    def test_curve_envelope_and_monotone_flow(self):
        plr = np.linspace(0.0, 1.0, 100001)
        eta = fuel_cell_efficiency(plr)
        flow = normalized_hydrogen_flow(plr)
        self.assertTrue(np.isfinite(eta).all())
        self.assertTrue(np.all((eta > 0.0) & (eta <= 1.0)))
        self.assertTrue(np.all(np.diff(flow) >= 0.0))

    def test_c2_matching(self):
        polynomial = np.polynomial.Polynomial([.3747, .4623, -2.0704, 3.6503, -2.996, .9033])
        bridge = np.polynomial.Polynomial(FLOW_BRIDGE_COEFFICIENTS)
        a, b = TRANSITION_LOW_PLR, TRANSITION_HIGH_PLR
        width = b - a
        np.testing.assert_allclose(
            [bridge(0.0), bridge.deriv()(0.0)/width, bridge.deriv(2)(0.0)/width**2],
            [a/LOW_LOAD_EFFICIENCY, 1.0/LOW_LOAD_EFFICIENCY, 0.0], atol=1e-12,
        )
        eta, d, dd = polynomial(b), polynomial.deriv()(b), polynomial.deriv(2)(b)
        expected = [b/eta, 1.0/eta-b*d/eta**2,
                    -2*d/eta**2-b*dd/eta**2+2*b*d*d/eta**3]
        np.testing.assert_allclose(
            [bridge(1.0), bridge.deriv()(1.0)/width, bridge.deriv(2)(1.0)/width**2],
            expected, atol=2e-12,
        )

    def test_pyomo_matches_numerical(self):
        model = ConcreteModel()
        model.power = Var(bounds=(0, 100e3), initialize=0.0)
        expression = pyomo_hydrogen_mass_flow(model.power, 100e3, 120e6)
        for power in [0.0, 500.0, 2999.99, 3000.0, 5000.0, 7000.0, 7000.01, 20000.0, 100e3]:
            model.power.set_value(power)
            self.assertAlmostEqual(value(expression), hydrogen_mass_flow(power, 100e3, 120e6), places=14)

    def test_units_and_capacity(self):
        data = load_carriage_data_1()
        validate_fuel_cell_parameters(data)
        self.assertEqual(data.mH2_max, 15.4)
        self.assertAlmostEqual(data.mH2_max * data.LoH_initial, 12.32)
        power = 20e3
        flow = hydrogen_mass_flow(power, data.Pfc_rated, data.LHV)
        eta = fuel_cell_efficiency(power/data.Pfc_rated)
        self.assertAlmostEqual(flow * eta * data.LHV, power)
        # A 60-s update is in seconds, not 60/3600 or another Wh scaling.
        next_loh = data.LoH_initial - flow / data.mH2_max * 60.0
        self.assertAlmostEqual((data.LoH_initial-next_loh)*data.mH2_max, flow*60.0)

    def test_invalid_parameters(self):
        for name in ("mH2_max", "LHV", "Pfc_rated", "V_nom_fc"):
            for invalid in (0.0, -1.0, float("nan"), float("inf")):
                with self.subTest(name=name, invalid=invalid), self.assertRaises(ValueError):
                    validate_fuel_cell_parameters(replace(load_carriage_data_1(), **{name: invalid}))

    def test_old_fmu_rejected_before_instantiation(self):
        from fmu_initialization import initialize_fmu
        with patch("fmu_initialization.read_model_description", return_value=SimpleNamespace(modelVariables=[])), \
             patch("fmu_initialization.extract") as extract:
            with self.assertRaisesRegex(ValueError, "Regenerate the FMU"):
                initialize_fmu("old.fmu", 0.0, ["t"], [load_carriage_data_1()], [0], 0.97)
            extract.assert_not_called()


if __name__ == "__main__":
    unittest.main()
