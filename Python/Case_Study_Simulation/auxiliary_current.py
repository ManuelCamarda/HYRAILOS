"""
Generates the auxiliary services current demand for each carriage.

The current implementation creates a bounded random current between 0 and a maximum value.
"""

import numpy as np

def auxiliary_current_generation(t_start, t_end, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, car_types, N):
    n_car = len(car_types)
    rng = np.random.default_rng(2)

    start_idx = int(round(t_start / tau_s_MPC))
    end_idx = start_idx + sim_steps_MPC
    total_steps = int(round(t_end / tau_s_MPC)) + 1

    I_a_points_full = rng.uniform(0, 15, size=(n_car, total_steps))
    I_a_points = I_a_points_full[:, start_idx:end_idx]

    I_a_ref = np.repeat(I_a_points, int(tau_s_MPC / tau_s), axis=1)

    I_a_ref=I_a_ref[:, :sim_steps]

    I_a_points = np.concatenate((I_a_points, np.zeros((n_car, N + 1))), axis=1)
    I_a_ref = np.concatenate((I_a_ref, I_a_ref[:, -1][:, None]), axis=1)

    return (I_a_ref, I_a_points)
