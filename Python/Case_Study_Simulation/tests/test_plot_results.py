"""Check that comparison plots export only the three-strategy table."""

import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from plot_results import plot_simulation_results


class PlotResultsTests(unittest.TestCase):
    def test_only_three_strategy_table_is_exported(self):
        time = np.array([0.0, 60.0, 120.0])
        states = {0: np.array([0.8, 0.75, 0.7])}
        currents = {0: np.array([1.0, 2.0, -1.0])}
        duties = {0: np.full(3, 0.5)}
        mpc = {"time": time, "I_cat": np.zeros(3),
               "total_MPC_solve_time": 1.0, "average_MPC_solve_time": 0.5}
        lpf = {"time_lpf": time, "I_cat_lpf": np.zeros(3)}
        dp = {"time_dp": time, "total_DP_solve_time": 2.0,
              "average_DP_solve_time": 2.0}
        for name in ("LoH", "SoCb", "SoCsc"):
            mpc[name], lpf[name + "_lpf"], dp[name + "_dp"] = states, states, states
        for name in ("I_fc", "I_b", "I_sc"):
            mpc[name], lpf[name + "_lpf"], dp[name + "_dp"] = currents, currents, currents
        for name in ("duty_fc", "duty_b", "duty_sc"):
            mpc[name], lpf[name + "_lpf"], dp[name + "_dp"] = duties, duties, duties

        with matplotlib.rc_context({"text.usetex": False}), \
             patch("plot_results._save_figures", return_value=[]) as save:
            try:
                plot_simulation_results(
                    mpc_results=mpc, lpf_ems_results=lpf, dp_results=dp,
                    I_t_ref_nominal=np.ones((1, 3)),
                    I_t_ref_plant=np.ones((1, 3)), I_a_ref=np.zeros((1, 3)),
                    tau_s=60.0, tau_s_MPC=60.0, t_end=120.0, traction_idx=[0],
                    lpf_ems_losses_kWh=3.0, mpc_losses_kWh=1.0,
                    dp_losses_kWh=2.0, converter_efficiency=0.97,
                )
                save.assert_called_once()
                figures = save.call_args.args[0]
                self.assertEqual(set(figures), {
                    "LoH.pdf", "SoCb.pdf", "SoCsc.pdf", "IDCfc.pdf",
                    "IDCb.pdf", "IDCsc.pdf", "It.pdf",
                    "Performance_Table_LPF-EMS_vs_DP_vs_MPC.pdf",
                })
                table_figure = figures["Performance_Table_LPF-EMS_vs_DP_vs_MPC.pdf"]
                table = table_figure.axes[0].tables[0]
                headers = [table[0, col].get_text().get_text() for col in range(7)]
                self.assertEqual(headers[1:4], ["LPF-EMS", "DP", "MPC"])
            finally:
                plt.close("all")


if __name__ == "__main__":
    unittest.main()
