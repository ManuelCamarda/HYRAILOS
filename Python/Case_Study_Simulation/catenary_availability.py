"""
Generates the catenary availability profile for the selected route time window.

The user-provided catenary availability intervals expressed in minutes are converted by this module 
into boolean profiles.
"""

import numpy as np

def catenary_availability_generation(t_start, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, car_types, intervals, N):

    # catenary availability
    t_MPC = (t_start + np.arange(0, sim_steps_MPC) * tau_s_MPC) / 60
    t_FMU = (t_start + np.arange(0, sim_steps) * tau_s) / 60

    bool_cat_points = np.zeros(sim_steps_MPC, dtype=int)
    bool_cat_ref = np.zeros(sim_steps, dtype=int)

    for t_start, t_end in intervals:
        bool_cat_points |= ((t_MPC >= t_start) & (t_MPC <= t_end))
        bool_cat_ref |= ((t_FMU >= t_start) & (t_FMU <= t_end))

    bool_cat_points = np.concatenate([bool_cat_points, np.zeros(N + 1)])
    bool_cat_ref = np.append(bool_cat_ref, bool_cat_ref[-1])

    return (bool_cat_ref.astype(int), bool_cat_points.astype(int))
