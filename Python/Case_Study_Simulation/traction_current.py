"""
Generates the traction current demand used by the simulation.

The reference is loaded from a .mat file.
"""

import numpy as np
from scipy.io import loadmat

# Plant-only traction prediction error. Set the fraction to 0.0 for nominal operation.
TRACTION_DISTURBANCE_FRACTION = 0.30
TRACTION_DISTURBANCE_SEED = 7470

# ============================================================
# Discretization of the traction current reference
# ============================================================
# The traction current reference must be a .mat file with 2 columns (with no headers) containing:
#     - first column: time values
#     - second column: traction current values
def traction_current_generation(t_start, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, car_types, N, traction_current_path):
    n_car = len(car_types)

    # data on the traction current
    mat = loadmat(traction_current_path)

    # MATLAB variable saved as: data = [time, current]
    data = mat['data']
    time_base = data[:, 0].squeeze()
    current_base = data[:, 1].squeeze()
    time_points = t_start + np.arange(sim_steps_MPC) * tau_s_MPC

    if time_points[0] < time_base[0] or time_points[-1] > time_base[-1]:
        raise ValueError(
            f"Requested simulation time [{time_points[0]}, {time_points[-1]}] s is outside "
            f"the traction current reference [{time_base[0]}, {time_base[-1]}] s"
        )

    I_t_points_base = np.interp(time_points, time_base, current_base)

    # creation of references at MPC sampling time
    I_t_points = np.zeros((n_car, sim_steps_MPC))

    # creation of all the traction and auxiliary currents in the carriages
    for c, ct in enumerate(car_types):
        if ct == 't':
            I_t_points[c, :] = I_t_points_base
        else:
            I_t_points[c, :] = 0.0

    # creation of references each tau_s
    I_t_ref = np.zeros((n_car, sim_steps))

    for c in range(n_car):
        It_ref_c = []

        for k in range(len(time_points) - 1):
            nseg = int((time_points[k + 1] - time_points[k]) / tau_s)
            It_ref_c.extend(np.full(nseg, I_t_points[c, k]))

        It_ref_c = np.array(It_ref_c)

        It_ref_c = np.append(It_ref_c, I_t_points[c, -1])

        I_t_ref[c, :] = It_ref_c[:sim_steps]

    I_t_points = np.concatenate((I_t_points, np.zeros((n_car, N + 1))), axis=1)

    I_t_ref = np.concatenate((I_t_ref, I_t_ref[:, -1][:, None]), axis=1)

    return (I_t_ref, I_t_points)


def traction_current_disturbance(
    I_t_ref_nominal,
    I_t_points_nominal,
    tau_s,
    tau_s_MPC,
    sim_steps_MPC,
    car_types,
    disturbance_fraction=None,
    disturbance_seed=None,
):

    if disturbance_fraction is None:
        disturbance_fraction = TRACTION_DISTURBANCE_FRACTION
    if disturbance_seed is None:
        disturbance_seed = TRACTION_DISTURBANCE_SEED

    if not 0.0 <= disturbance_fraction < 1.0:
        raise ValueError("traction_disturbance_fraction must be in [0, 1)")
    if not isinstance(disturbance_seed, (int, np.integer)):
        raise TypeError("traction_disturbance_seed must be an integer")

    steps_per_control_float = tau_s_MPC / tau_s
    steps_per_control = int(round(steps_per_control_float))
    if steps_per_control <= 0 or not np.isclose(
        steps_per_control_float, steps_per_control
    ):
        raise ValueError("tau_s_MPC must be an integer multiple of tau_s")

    rng = np.random.default_rng(int(disturbance_seed))
    relative_error_points = rng.uniform(
        -disturbance_fraction,
        disturbance_fraction,
        size=sim_steps_MPC,
    )

    I_t_points_plant = np.array(I_t_points_nominal, dtype=float, copy=True)
    I_t_ref_plant = np.array(I_t_ref_nominal, dtype=float, copy=True)

    sample_indices = np.minimum(
        np.arange(I_t_ref_plant.shape[1]) // steps_per_control,
        sim_steps_MPC - 1,
    )
    relative_error_ref = relative_error_points[sample_indices]

    for c, carriage_type in enumerate(car_types):
        if carriage_type != "t":
            continue

        I_t_points_plant[c, :sim_steps_MPC] *= 1.0 + relative_error_points
        I_t_ref_plant[c, :] *= 1.0 + relative_error_ref

    return (
        I_t_ref_plant,
        I_t_points_plant,
        relative_error_ref,
        relative_error_points,
    )
