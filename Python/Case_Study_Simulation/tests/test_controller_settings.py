"""Check module-local disturbance and LPF-EMS configuration."""

import ast
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

import lpf_ems_simulation
import traction_current
from data_carriage import load_carriage_data_1
from lpf_ems_simulation import LPFEMSController


class ControllerSettingsTests(unittest.TestCase):
    def setUp(self):
        self.nominal_points = np.array([
            [100.0, -50.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [100.0, -50.0, 0.0, 0.0],
        ])
        self.nominal_ref = np.repeat(self.nominal_points[:, :3], 120, axis=1)

    def disturbance(self, **kwargs):
        return traction_current.traction_current_disturbance(
            self.nominal_ref, self.nominal_points,
            tau_s=0.5, tau_s_MPC=60.0, sim_steps_MPC=3,
            car_types=["t", "a", "t"], **kwargs,
        )

    def controller(self, **kwargs):
        return LPFEMSController(
            tau_s=0.5, traction_idx=[0], data=[load_carriage_data_1()],
            converter_efficiency=0.97, **kwargs,
        )

    def test_main_settings_excludes_controller_tuning(self):
        source = Path(__file__).resolve().parents[1] / "User_Settings.py"
        tree = ast.parse(source.read_text(encoding="utf-8-sig"))
        settings = next(
            node.value for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "settings"
                    for target in node.targets)
        )
        keys = [ast.literal_eval(key) for key in settings.keys]
        self.assertFalse(any(key.startswith("lpf_ems_") for key in keys))
        self.assertNotIn("traction_disturbance_fraction", keys)
        self.assertNotIn("traction_disturbance_seed", keys)

    def test_disturbance_defaults_match_explicit_module_values(self):
        automatic = self.disturbance()
        explicit = self.disturbance(
            disturbance_fraction=traction_current.TRACTION_DISTURBANCE_FRACTION,
            disturbance_seed=traction_current.TRACTION_DISTURBANCE_SEED,
        )
        for actual, expected in zip(automatic, explicit):
            self.assertEqual(actual.dtype, expected.dtype)
            self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_disturbance_reads_edited_module_values(self):
        with patch.object(traction_current, "TRACTION_DISTURBANCE_FRACTION", 0.12), \
             patch.object(traction_current, "TRACTION_DISTURBANCE_SEED", 123):
            automatic = self.disturbance()
        explicit = self.disturbance(disturbance_fraction=0.12, disturbance_seed=123)
        for actual, expected in zip(automatic, explicit):
            np.testing.assert_array_equal(actual, expected)

    def test_zero_fraction_restores_nominal_profiles(self):
        with patch.object(traction_current, "TRACTION_DISTURBANCE_FRACTION", 0.0):
            ref, points, error_ref, error_points = self.disturbance()
        np.testing.assert_array_equal(ref, self.nominal_ref)
        np.testing.assert_array_equal(points, self.nominal_points)
        self.assertTrue(np.all(error_ref == 0.0))
        self.assertTrue(np.all(error_points == 0.0))

    def test_lpf_controller_uses_module_settings(self):
        controller = self.controller()
        for key, expected in lpf_ems_simulation.LPF_EMS_SETTINGS.items():
            with self.subTest(setting=key):
                self.assertEqual(getattr(controller, key), expected)

    def test_lpf_controller_reads_edited_module_values(self):
        with patch.dict(lpf_ems_simulation.LPF_EMS_SETTINGS,
                        {"tau_fast": 90.0, "sc_target": 0.55}):
            controller = self.controller()
        self.assertEqual(controller.tau_fast, 90.0)
        self.assertEqual(controller.sc_target, 0.55)
        self.assertAlmostEqual(controller.alpha_fast, np.exp(-0.5 / 90.0))

    def test_explicit_lpf_configuration_does_not_mutate_module_settings(self):
        original = dict(lpf_ems_simulation.LPF_EMS_SETTINGS)
        controller = self.controller(config={"tau_fast": 100.0})
        self.assertEqual(controller.tau_fast, 100.0)
        self.assertEqual(lpf_ems_simulation.LPF_EMS_SETTINGS, original)


if __name__ == "__main__":
    unittest.main()
