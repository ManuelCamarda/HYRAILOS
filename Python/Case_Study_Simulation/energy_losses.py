"""
Computes the energy losses for LPF-EMS, MPC, and DP simulations.
"""

import numpy as np

from converter_model import dc_bus_current


def _line_currents(car_types, traction_idx, data, cat_pos, I_t, I_a, I_fc, I_b, I_sc,
                   duty_fc, duty_b, duty_sc, I_cat, steps,
                   converter_efficiency):
    n_car = len(car_types)
    Il = np.zeros((max(n_car - 1, 0), steps), dtype=float)

    for k in range(steps):
        incoming_left = 0.0

        for c in range(n_car - 1):
            if car_types[c] == "t":
                gen = (
                    dc_bus_current(
                        I_b[c][k],
                        1.0 - duty_b[c][k],
                        converter_efficiency,
                    )
                    + dc_bus_current(
                        I_fc[c][k],
                        1.0 - duty_fc[c][k],
                        converter_efficiency,
                    )
                    + dc_bus_current(
                        I_sc[c][k],
                        1.0 - duty_sc[c][k],
                        converter_efficiency,
                    )
                )
                load = I_t[c, k] + I_a[c, k]
            else:
                gen = 0.0
                load = I_a[c, k]

            cat_inj = I_cat[k] if cat_pos != 0 and c == cat_pos - 1 else 0.0
            Il[c, k] = gen + incoming_left + cat_inj - load
            incoming_left = Il[c, k]

    return Il


def _interval_dict(signal, traction_idx, start, steps):
    interval_signal = {}
    for c in traction_idx:
        values = np.asarray(signal[c], dtype=float)
        if values.size < start + steps:
            raise ValueError("A measured FMU signal is shorter than the simulation")
        interval_signal[c] = values[start : start + steps]
    return interval_signal


def _realized_energy_losses(
    data,
    car_types,
    traction_idx,
    cat_pos,
    tau_s,
    tau_s_MPC,
    sim_steps,
    sim_steps_MPC,
    I_t_ref,
    I_a_ref,
    I_fc,
    I_b,
    I_sc,
    duty_fc,
    duty_b,
    duty_sc,
    P_loss_fc,
    P_loss_b,
    P_loss_sc,
    I_cat,
    signal_start,
    converter_efficiency,
):
    """Evaluate resistive and converter losses from FMU trajectories."""

    I_fc = _interval_dict(I_fc, traction_idx, signal_start, sim_steps)
    I_b = _interval_dict(I_b, traction_idx, signal_start, sim_steps)
    I_sc = _interval_dict(I_sc, traction_idx, signal_start, sim_steps)
    duty_fc = _interval_dict(duty_fc, traction_idx, signal_start, sim_steps)
    duty_b = _interval_dict(duty_b, traction_idx, signal_start, sim_steps)
    duty_sc = _interval_dict(duty_sc, traction_idx, signal_start, sim_steps)
    P_loss_fc = _interval_dict(
        P_loss_fc, traction_idx, signal_start, sim_steps
    )
    P_loss_b = _interval_dict(P_loss_b, traction_idx, signal_start, sim_steps)
    P_loss_sc = _interval_dict(
        P_loss_sc, traction_idx, signal_start, sim_steps
    )

    I_cat = np.asarray(I_cat, dtype=float)
    if I_cat.size < signal_start + sim_steps:
        raise ValueError("The measured catenary signal is shorter than the simulation")
    I_cat = I_cat[signal_start : signal_start + sim_steps]

    Il = _line_currents(
        car_types,
        traction_idx,
        data,
        cat_pos,
        I_t_ref,
        I_a_ref,
        I_fc,
        I_b,
        I_sc,
        duty_fc,
        duty_b,
        duty_sc,
        I_cat,
        sim_steps,
        converter_efficiency,
    )

    Plosstot = 0.0
    for k in range(sim_steps):
        for c in range(len(car_types)):
            Plosstot += (data[c].Rt + data[c].Ra) * I_a_ref[c, k] ** 2

            if car_types[c] == "t":
                I_b_dc = dc_bus_current(
                    I_b[c][k],
                    1.0 - duty_b[c][k],
                    converter_efficiency,
                )
                I_fc_dc = dc_bus_current(
                    I_fc[c][k],
                    1.0 - duty_fc[c][k],
                    converter_efficiency,
                )
                I_sc_dc = dc_bus_current(
                    I_sc[c][k],
                    1.0 - duty_sc[c][k],
                    converter_efficiency,
                )
                Plosstot += (
                    data[c].Rb * I_b[c][k] ** 2
                    + data[c].RDCb * I_b_dc ** 2
                    + data[c].Rfc * I_fc[c][k] ** 2
                    + data[c].RH * I_fc[c][k] ** 2
                    + data[c].RDCfc * I_fc_dc ** 2
                    + data[c].Rsc * I_sc[c][k] ** 2
                    + data[c].RDCsc * I_sc_dc ** 2
                    + P_loss_fc[c][k]
                    + P_loss_b[c][k]
                    + P_loss_sc[c][k]
                    + data[c].Rt * I_t_ref[c, k] ** 2
                )

        if cat_pos != 0:
            Plosstot += data[cat_pos - 1].Rcat * I_cat[k] ** 2

        for line in range(len(car_types) - 1):
            Plosstot += data[line].Rl * Il[line, k] ** 2

    return Plosstot * tau_s / sim_steps_MPC / 1000 / tau_s_MPC


def compute_lpf_ems_energy_losses(
    data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
    sim_steps, sim_steps_MPC, I_t_ref, I_a_ref, results,
    converter_efficiency
):
    return _realized_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
        sim_steps, sim_steps_MPC, I_t_ref, I_a_ref,
        results["I_fc_lpf"], results["I_b_lpf"], results["I_sc_lpf"],
        results["duty_fc_lpf"], results["duty_b_lpf"], results["duty_sc_lpf"],
        results["P_loss_fc_lpf"], results["P_loss_b_lpf"],
        results["P_loss_sc_lpf"], results["I_cat_lpf"], signal_start=0,
        converter_efficiency=converter_efficiency,
    )


def compute_mpc_energy_losses(
    data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
    sim_steps, sim_steps_MPC, I_t_ref, I_a_ref, results,
    converter_efficiency
):
    return _realized_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
        sim_steps, sim_steps_MPC, I_t_ref, I_a_ref,
        results["I_fc"], results["I_b"], results["I_sc"],
        results["duty_fc"], results["duty_b"], results["duty_sc"],
        results["P_loss_fc"], results["P_loss_b"], results["P_loss_sc"],
        results["I_cat"], signal_start=1,
        converter_efficiency=converter_efficiency,
    )


def compute_dp_energy_losses(
    data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
    sim_steps, sim_steps_MPC, I_t_ref, I_a_ref, results,
    converter_efficiency
):
    return _realized_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
        sim_steps, sim_steps_MPC, I_t_ref, I_a_ref,
        results["I_fc_dp"], results["I_b_dp"], results["I_sc_dp"],
        results["duty_fc_dp"], results["duty_b_dp"], results["duty_sc_dp"],
        results["P_loss_fc_dp"], results["P_loss_b_dp"],
        results["P_loss_sc_dp"], results["I_cat_dp"], signal_start=1,
        converter_efficiency=converter_efficiency,
    )
