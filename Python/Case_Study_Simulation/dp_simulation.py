"""
Run the DP energy management simulation.

The complete control trajectory is optimized once, then replayed open loop on
the same FMU plant used by the LPF-EMS and MPC simulations.
"""

import time as tm

import numpy as np

from dp_function import dp_function
from fmu_initialization import initialize_fmu, terminate_fmu
from fuel_cell_model import HydrogenRecorder


def run_dp_simulation(
    fmu_path,
    t_start,
    tau_s,
    tau_s_MPC,
    sim_steps,
    sim_steps_MPC,
    car_types,
    data,
    traction_idx,
    n_trac,
    I_t_ref_plant,
    I_a_ref,
    I_t_points_nominal,
    I_a_points,
    I_ta_points_nominal,
    bool_cat_ref,
    bool_cat_points,
    wfc,
    wb,
    wsc,
    wcat,
    solver,
    cat_pos,
    converter_efficiency,
):
    """Solve the full route once and replay the planned controls in the FMU."""

    n_car = len(car_types)
    if n_trac != len(traction_idx):
        raise ValueError("n_trac must match traction_idx")

    steps_per_control_float = tau_s_MPC / tau_s
    steps_per_control = int(round(steps_per_control_float))
    if steps_per_control <= 0 or not np.isclose(
        steps_per_control_float, steps_per_control
    ):
        raise ValueError("tau_s_MPC must be an integer multiple of tau_s")

    run_started = tm.perf_counter()
    fmu, _, vr = initialize_fmu(
        fmu_path=fmu_path,
        t_start=t_start,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        converter_efficiency=converter_efficiency,
    )

    try:
        x0 = np.array(
            [
                value
                for c in traction_idx
                for value in (
                    data[c].LoH_initial,
                    data[c].SoCb_initial,
                    data[c].SoCsc_initial,
                )
            ],
            dtype=float,
        )

        plan = dp_function(
            x0=x0,
            horizon=sim_steps_MPC,
            tau_s=tau_s_MPC,
            I_t_values=I_t_points_nominal,
            I_a_values=I_a_points,
            I_ta_values=I_ta_points_nominal,
            wfc=wfc,
            wb=wb,
            wsc=wsc,
            wcat=wcat,
            data=data,
            solver=solver,
            car_types=car_types,
            bool_cat_values=bool_cat_points,
            cat_pos=cat_pos,
            converter_efficiency=converter_efficiency,
        )

        time_dp = []
        LoH_dp = {c: [] for c in traction_idx}
        SoCb_dp = {c: [] for c in traction_idx}
        SoCsc_dp = {c: [] for c in traction_idx}

        I_fc_dp = {c: [] for c in traction_idx}
        I_b_dp = {c: [] for c in traction_idx}
        I_sc_dp = {c: [] for c in traction_idx}

        V_fc_dp = {c: [] for c in traction_idx}
        V_b_dp = {c: [] for c in traction_idx}
        V_sc_dp = {c: [] for c in traction_idx}

        duty_fc_dp = {c: [] for c in traction_idx}
        duty_b_dp = {c: [] for c in traction_idx}
        duty_sc_dp = {c: [] for c in traction_idx}
        P_loss_fc_dp = {c: [] for c in traction_idx}
        P_loss_b_dp = {c: [] for c in traction_idx}
        P_loss_sc_dp = {c: [] for c in traction_idx}
        I_cat_dp = []
        hydrogen = HydrogenRecorder(data, traction_idx)

        def record_outputs(current_time):
            time_dp.append(current_time)
            hydrogen.record(fmu, vr, current_time)
            for c in traction_idx:
                LoH_dp[c].append(fmu.getReal([vr["LoH"][c]])[0])
                SoCb_dp[c].append(fmu.getReal([vr["SoCb"][c]])[0])
                SoCsc_dp[c].append(fmu.getReal([vr["SoCsc"][c]])[0])

                I_fc_dp[c].append(fmu.getReal([vr["ifc"][c]])[0])
                I_b_dp[c].append(fmu.getReal([vr["ib"][c]])[0])
                I_sc_dp[c].append(fmu.getReal([vr["isc"][c]])[0])

                V_fc_dp[c].append(fmu.getReal([vr["vfc"][c]])[0])
                V_b_dp[c].append(fmu.getReal([vr["v_b"][c]])[0])
                V_sc_dp[c].append(fmu.getReal([vr["vsc"][c]])[0])

                duty_fc_dp[c].append(fmu.getReal([vr["duty_fc"][c]])[0])
                duty_b_dp[c].append(fmu.getReal([vr["duty_b"][c]])[0])
                duty_sc_dp[c].append(fmu.getReal([vr["duty_sc"][c]])[0])

                P_loss_fc_dp[c].append(
                    fmu.getReal([vr["loss_fc"][c]])[0]
                )
                P_loss_b_dp[c].append(
                    fmu.getReal([vr["loss_b"][c]])[0]
                )
                P_loss_sc_dp[c].append(
                    fmu.getReal([vr["loss_sc"][c]])[0]
                )

            I_cat_dp.append(fmu.getReal([vr["icat_ref"]])[0])

        t = t_start
        record_outputs(t)

        for j in range(sim_steps):
            control_index = min(j // steps_per_control, sim_steps_MPC - 1)

            vr_set = []
            val_set = []
            for c in range(n_car):
                vr_set.append(vr["ia_ref"][c])
                val_set.append(I_a_ref[c, j])

                if car_types[c] == "t":
                    vr_set.append(vr["it_ref"][c])
                    val_set.append(I_t_ref_plant[c, j])

            for p, c in enumerate(traction_idx):
                vr_set.extend(
                    [
                        vr["ifc_ref"][c],
                        vr["ib_ref"][c],
                        vr["isc_ref"][c],
                    ]
                )
                val_set.extend(
                    [
                        plan["Ifc_DP"][p, control_index],
                        plan["Ib_DP"][p, control_index],
                        plan["Isc_DP"][p, control_index],
                    ]
                )

            vr_set.extend([vr["icat_ref"], vr["bool_cat"]])
            val_set.extend(
                [
                    plan["Icat_DP"][control_index] if cat_pos != 0 else 0.0,
                    bool_cat_ref[j] if cat_pos != 0 else 0,
                ]
            )
            fmu.setReal(vr_set, val_set)

            fmu.doStep(currentCommunicationPoint=t, communicationStepSize=tau_s)
            t += tau_s
            record_outputs(t)

    finally:
        terminate_fmu(fmu)

    elapsed = tm.perf_counter() - run_started
    time_dp = np.asarray(time_dp, dtype=float)

    measured_signals = (
        LoH_dp,
        SoCb_dp,
        SoCsc_dp,
        I_fc_dp,
        I_b_dp,
        I_sc_dp,
        V_fc_dp,
        V_b_dp,
        V_sc_dp,
        duty_fc_dp,
        duty_b_dp,
        duty_sc_dp,
        P_loss_fc_dp,
        P_loss_b_dp,
        P_loss_sc_dp,
    )
    for signal in measured_signals:
        for c in traction_idx:
            signal[c] = np.asarray(signal[c], dtype=float)
    I_cat_dp = np.asarray(I_cat_dp, dtype=float)

    dp_results = {
        "time_dp": time_dp,
        "LoH_dp": LoH_dp,
        "SoCb_dp": SoCb_dp,
        "SoCsc_dp": SoCsc_dp,
        "I_fc_dp": I_fc_dp,
        "I_b_dp": I_b_dp,
        "I_sc_dp": I_sc_dp,
        "I_cat_dp": I_cat_dp,
        "V_fc_dp": V_fc_dp,
        "V_b_dp": V_b_dp,
        "V_sc_dp": V_sc_dp,
        "duty_fc_dp": duty_fc_dp,
        "duty_b_dp": duty_b_dp,
        "duty_sc_dp": duty_sc_dp,
        "P_loss_fc_dp": P_loss_fc_dp,
        "P_loss_b_dp": P_loss_b_dp,
        "P_loss_sc_dp": P_loss_sc_dp,
        "converter_efficiency": converter_efficiency,
        "elapsed_DP_time": elapsed,
        "optimization_call_count": 1,
        "fuel_cell": hydrogen.results(),
    }
    dp_results.update(plan)
    return dp_results
