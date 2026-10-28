"""
Runs the closed-loop MPC simulation.

At each MPC sampling instant, this module builds and solves the optimization problem, 
applies the selected controls to the FMU, advances the physical model, and stores the resulting trajectories.
"""

import time as tm
import numpy as np

from fmu_initialization import initialize_fmu, terminate_fmu
from mpc_function import mpc_function
from fuel_cell_model import HydrogenRecorder


def build_measured_current_prediction(
    control_index,
    I_t_points_nominal,
    I_t_points_plant,
    I_a_points,
    I_ta_points_nominal,
):
    """Use measured traction now and the nominal traction forecast thereafter."""

    if not 0 <= control_index < I_t_points_nominal.shape[1]:
        raise IndexError("control_index is outside the traction-current profile")

    I_t_prediction = np.array(I_t_points_nominal, dtype=float, copy=True)
    I_ta_prediction = np.array(I_ta_points_nominal, dtype=float, copy=True)

    I_t_prediction[:, control_index] = I_t_points_plant[:, control_index]
    I_ta_prediction[:, control_index] = (
        I_t_points_plant[:, control_index] + I_a_points[:, control_index]
    )

    return I_t_prediction, I_ta_prediction


def run_mpc_simulation(
    fmu_path,
    t_start,
    tau_s,
    tau_s_MPC,
    sim_steps,
    sim_steps_MPC,
    N,
    car_types,
    data,
    traction_idx,
    n_trac,
    I_t_ref_plant,
    I_a_ref,
    I_t_points_nominal,
    I_t_points_plant,
    I_a_points,
    I_ta_points_nominal,
    bool_cat_points,
    wfc,
    wb,
    wsc,
    wcat,
    solver,
    cat_pos,
    converter_efficiency,
):
    n_car = len(car_types)
    cat_connected = cat_pos != 0

    steps_per_control_float = tau_s_MPC / tau_s
    steps_per_control = int(round(steps_per_control_float))
    if steps_per_control <= 0 or not np.isclose(
        steps_per_control_float, steps_per_control
    ):
        raise ValueError("tau_s_MPC must be an integer multiple of tau_s")

    fmu, md, vr = initialize_fmu(
        fmu_path=fmu_path,
        t_start=t_start,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        converter_efficiency=converter_efficiency,
    )

    x0 = np.array(
        [
            val
            for c in traction_idx
            for val in (
                data[c].LoH_initial,
                data[c].SoCb_initial,
                data[c].SoCsc_initial,
            )
        ],
        dtype=float,
    )

    x = np.zeros((3 * n_trac, sim_steps_MPC), dtype=float)

    if n_trac > 0:
        x[:, 0] = x0

    Ifc_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    Ib_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    Isc_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)

    deltafc = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    deltas = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    deltasc = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    deltaIcat_MPC = np.zeros(sim_steps_MPC, dtype=float)

    dutyfc_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    dutyb_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)
    dutysc_MPC = np.zeros((n_trac, sim_steps_MPC), dtype=float)

    Icat_MPC = np.zeros(sim_steps_MPC, dtype=float)

    if n_car > 1:
        Il_MPC = np.zeros((n_car - 1, sim_steps_MPC), dtype=float)
    else:
        Il_MPC = np.zeros((0, sim_steps_MPC), dtype=float)

    time = []

    LoH = {c: [] for c in traction_idx}
    SoCb = {c: [] for c in traction_idx}
    SoCsc = {c: [] for c in traction_idx}

    I_fc = {c: [] for c in traction_idx}
    I_b = {c: [] for c in traction_idx}
    I_sc = {c: [] for c in traction_idx}

    V_fc = {c: [] for c in traction_idx}
    V_b = {c: [] for c in traction_idx}
    V_sc = {c: [] for c in traction_idx}

    duty_fc = {c: [] for c in traction_idx}
    duty_b = {c: [] for c in traction_idx}
    duty_sc = {c: [] for c in traction_idx}

    P_loss_fc = {c: [] for c in traction_idx}
    P_loss_b = {c: [] for c in traction_idx}
    P_loss_sc = {c: [] for c in traction_idx}

    I_cat = []
    hydrogen = HydrogenRecorder(data, traction_idx)

    t_mpc_start = tm.time()
    solve_times = []

    t = t_start
    i = 0
    u_opt = None
    measured_traction_points = np.zeros_like(
        I_t_points_nominal[:, :sim_steps_MPC], dtype=float
    )

    for j in range(sim_steps):

        if j == 0:
            time.append(t)
            hydrogen.record(fmu, vr, t)

            for c in traction_idx:
                LoH[c].append(fmu.getReal([vr["LoH"][c]])[0])
                SoCb[c].append(fmu.getReal([vr["SoCb"][c]])[0])
                SoCsc[c].append(fmu.getReal([vr["SoCsc"][c]])[0])

                I_fc[c].append(fmu.getReal([vr["ifc"][c]])[0])
                I_b[c].append(fmu.getReal([vr["ib"][c]])[0])
                I_sc[c].append(fmu.getReal([vr["isc"][c]])[0])

                V_fc[c].append(fmu.getReal([vr["vfc"][c]])[0])
                V_b[c].append(fmu.getReal([vr["v_b"][c]])[0])
                V_sc[c].append(fmu.getReal([vr["vsc"][c]])[0])

                duty_fc[c].append(fmu.getReal([vr["duty_fc"][c]])[0])
                duty_b[c].append(fmu.getReal([vr["duty_b"][c]])[0])
                duty_sc[c].append(fmu.getReal([vr["duty_sc"][c]])[0])

                P_loss_fc[c].append(fmu.getReal([vr["loss_fc"][c]])[0])
                P_loss_b[c].append(fmu.getReal([vr["loss_b"][c]])[0])
                P_loss_sc[c].append(fmu.getReal([vr["loss_sc"][c]])[0])

            I_cat.append(fmu.getReal([vr["icat_ref"]])[0])

        # Compute MPC every tau_s_MPC
        if i != 0 and j > 0 and j % steps_per_control == 0:

            control_index = min(j // steps_per_control, sim_steps_MPC - 1)
            if control_index != i:
                raise RuntimeError("MPC control index is not aligned with FMU time")

            x_mpc = np.array(
                [
                    val
                    for c in traction_idx
                    for val in (LoH[c][-1], SoCb[c][-1], SoCsc[c][-1])
                ],
                dtype=float,
            )

            duty_fc_last = [duty_fc[c][-1] for c in traction_idx]
            duty_b_last = [duty_b[c][-1] for c in traction_idx]
            duty_sc_last = [duty_sc[c][-1] for c in traction_idx]

            I_t_prediction, I_ta_prediction = build_measured_current_prediction(
                control_index=i,
                I_t_points_nominal=I_t_points_nominal,
                I_t_points_plant=I_t_points_plant,
                I_a_points=I_a_points,
                I_ta_points_nominal=I_ta_points_nominal,
            )
            measured_traction_points[:, i] = I_t_points_plant[:, i]

            solve_started = tm.perf_counter()
            u_opt, slack_opt = mpc_function(
                x_mpc,
                N,
                tau_s_MPC,
                i,
                I_t_prediction,
                I_a_points,
                I_ta_prediction,
                wfc,
                wb,
                wsc,
                wcat,
                data,
                solver,
                duty_fc_last,
                duty_b_last,
                duty_sc_last,
                car_types,
                bool_cat_points,
                cat_pos,
                converter_efficiency,
            )
            solve_times.append(tm.perf_counter() - solve_started)

            for p, c in enumerate(traction_idx):
                Ifc_MPC[p, i] = u_opt[3 * p]
                Ib_MPC[p, i] = u_opt[3 * p + 1]
                Isc_MPC[p, i] = u_opt[3 * p + 2]

                deltafc[p, i] = slack_opt[3 * p]
                deltas[p, i] = slack_opt[3 * p + 1]
                deltasc[p, i] = slack_opt[3 * p + 2]

                x[3 * p, i] = LoH[c][-1]
                x[3 * p + 1, i] = SoCb[c][-1]
                x[3 * p + 2, i] = SoCsc[c][-1]

                dutyfc_MPC[p, i] = fmu.getReal([vr["duty_fc"][c]])[0]
                dutyb_MPC[p, i] = fmu.getReal([vr["duty_b"][c]])[0]
                dutysc_MPC[p, i] = fmu.getReal([vr["duty_sc"][c]])[0]

            if cat_connected:
                Icat_MPC[i] = u_opt[3 * n_trac]
                deltaIcat_MPC[i] = slack_opt[3 * n_trac]

            line_start = 3 * n_trac + (1 if cat_connected else 0)

            if n_car > 1:
                Il_MPC[:, i] = u_opt[
                    line_start : line_start + (n_car - 1)
                ]

            i += 1

        # First MPC computation
        if i == 0:
            x_mpc = np.array(
                [
                    val
                    for c in traction_idx
                    for val in (LoH[c][-1], SoCb[c][-1], SoCsc[c][-1])
                ],
                dtype=float,
            )

            duty_fc_last = [
                duty_fc[c][-1] if len(duty_fc[c]) > 0 else 0.0
                for c in traction_idx
            ]
            duty_b_last = [
                duty_b[c][-1] if len(duty_b[c]) > 0 else 0.0
                for c in traction_idx
            ]
            duty_sc_last = [
                duty_sc[c][-1] if len(duty_sc[c]) > 0 else 0.0
                for c in traction_idx
            ]

            I_t_prediction, I_ta_prediction = build_measured_current_prediction(
                control_index=i,
                I_t_points_nominal=I_t_points_nominal,
                I_t_points_plant=I_t_points_plant,
                I_a_points=I_a_points,
                I_ta_points_nominal=I_ta_points_nominal,
            )
            measured_traction_points[:, i] = I_t_points_plant[:, i]

            solve_started = tm.perf_counter()
            u_opt, slack_opt = mpc_function(
                x_mpc,
                N,
                tau_s_MPC,
                i,
                I_t_prediction,
                I_a_points,
                I_ta_prediction,
                wfc,
                wb,
                wsc,
                wcat,
                data,
                solver,
                duty_fc_last,
                duty_b_last,
                duty_sc_last,
                car_types,
                bool_cat_points,
                cat_pos,
                converter_efficiency,
            )
            solve_times.append(tm.perf_counter() - solve_started)

            for p, c in enumerate(traction_idx):
                Ifc_MPC[p, i] = u_opt[3 * p]
                Ib_MPC[p, i] = u_opt[3 * p + 1]
                Isc_MPC[p, i] = u_opt[3 * p + 2]

                deltafc[p, i] = slack_opt[3 * p]
                deltas[p, i] = slack_opt[3 * p + 1]
                deltasc[p, i] = slack_opt[3 * p + 2]

                dutyfc_MPC[p, i] = fmu.getReal([vr["duty_fc"][c]])[0]
                dutyb_MPC[p, i] = fmu.getReal([vr["duty_b"][c]])[0]
                dutysc_MPC[p, i] = fmu.getReal([vr["duty_sc"][c]])[0]

            if cat_connected:
                Icat_MPC[i] = u_opt[3 * n_trac]
                deltaIcat_MPC[i] = slack_opt[3 * n_trac]

            line_start = 3 * n_trac + (1 if cat_connected else 0)

            if n_car > 1:
                Il_MPC[:, i] = u_opt[
                    line_start : line_start + (n_car - 1)
                ]

            i += 1

        # ========================================================
        # Apply inputs to FMU
        # ========================================================
        vr_set = []
        val_set = []

        for c in range(n_car):
            vr_set.append(vr["ia_ref"][c])
            val_set.append(I_a_ref[c, j])

            if car_types[c] == "t":
                vr_set.append(vr["it_ref"][c])
                val_set.append(I_t_ref_plant[c, j])

        for p, c in enumerate(traction_idx):
            vr_set.extend([
                vr["ifc_ref"][c],
                vr["ib_ref"][c],
                vr["isc_ref"][c],
            ])
            val_set.extend([
                u_opt[3 * p],
                u_opt[3 * p + 1],
                u_opt[3 * p + 2],
            ])

        active_control_index = max(i - 1, 0)
        vr_set.extend([vr["icat_ref"], vr["bool_cat"]])
        val_set.extend([
            u_opt[3 * n_trac] if cat_connected else 0.0,
            bool_cat_points[active_control_index] if cat_connected else 0,
        ])

        fmu.setReal(vr_set, val_set)

        # ========================================================
        # Advance FMU
        # ========================================================
        fmu.doStep(currentCommunicationPoint=t, communicationStepSize=tau_s)
        t += tau_s

        # ========================================================
        # Read outputs
        # ========================================================
        time.append(t)
        hydrogen.record(fmu, vr, t)

        for c in traction_idx:
            LoH[c].append(fmu.getReal([vr["LoH"][c]])[0])
            SoCb[c].append(fmu.getReal([vr["SoCb"][c]])[0])
            SoCsc[c].append(fmu.getReal([vr["SoCsc"][c]])[0])

            I_fc[c].append(fmu.getReal([vr["ifc"][c]])[0])
            I_b[c].append(fmu.getReal([vr["ib"][c]])[0])
            I_sc[c].append(fmu.getReal([vr["isc"][c]])[0])

            V_fc[c].append(fmu.getReal([vr["vfc"][c]])[0])
            V_b[c].append(fmu.getReal([vr["v_b"][c]])[0])
            V_sc[c].append(fmu.getReal([vr["vsc"][c]])[0])

            duty_fc[c].append(fmu.getReal([vr["duty_fc"][c]])[0])
            duty_b[c].append(fmu.getReal([vr["duty_b"][c]])[0])
            duty_sc[c].append(fmu.getReal([vr["duty_sc"][c]])[0])

            P_loss_fc[c].append(fmu.getReal([vr["loss_fc"][c]])[0])
            P_loss_b[c].append(fmu.getReal([vr["loss_b"][c]])[0])
            P_loss_sc[c].append(fmu.getReal([vr["loss_sc"][c]])[0])

        I_cat.append(fmu.getReal([vr["icat_ref"]])[0])

    elapsed = tm.time() - t_mpc_start
    total_solve_time = float(np.sum(solve_times))
    average_solve_time = float(np.mean(solve_times)) if solve_times else 0.0

    terminate_fmu(fmu)

    # ============================================================
    # Convert results to arrays
    # ============================================================
    time = np.array(time)

    for c in traction_idx:
        LoH[c] = np.array(LoH[c])
        SoCb[c] = np.array(SoCb[c])
        SoCsc[c] = np.array(SoCsc[c])

        I_fc[c] = np.array(I_fc[c])
        I_b[c] = np.array(I_b[c])
        I_sc[c] = np.array(I_sc[c])

        V_fc[c] = np.array(V_fc[c])
        V_b[c] = np.array(V_b[c])
        V_sc[c] = np.array(V_sc[c])

        duty_fc[c] = np.array(duty_fc[c])
        duty_b[c] = np.array(duty_b[c])
        duty_sc[c] = np.array(duty_sc[c])

        P_loss_fc[c] = np.array(P_loss_fc[c])
        P_loss_b[c] = np.array(P_loss_b[c])
        P_loss_sc[c] = np.array(P_loss_sc[c])

    I_cat = np.array(I_cat)


    mpc_results = {
        "time": time,

        "LoH": LoH,
        "SoCb": SoCb,
        "SoCsc": SoCsc,

        "I_fc": I_fc,
        "I_b": I_b,
        "I_sc": I_sc,
        "I_cat": I_cat,

        "V_fc": V_fc,
        "V_b": V_b,
        "V_sc": V_sc,

        "duty_fc": duty_fc,
        "duty_b": duty_b,
        "duty_sc": duty_sc,

        "P_loss_fc": P_loss_fc,
        "P_loss_b": P_loss_b,
        "P_loss_sc": P_loss_sc,
        "converter_efficiency": converter_efficiency,

        "x": x,

        "Ifc_MPC": Ifc_MPC,
        "Ib_MPC": Ib_MPC,
        "Isc_MPC": Isc_MPC,

        "deltafc": deltafc,
        "deltas": deltas,
        "deltasc": deltasc,
        "deltaIcat_MPC": deltaIcat_MPC,

        "dutyfc_MPC": dutyfc_MPC,
        "dutyb_MPC": dutyb_MPC,
        "dutysc_MPC": dutysc_MPC,

        "Icat_MPC": Icat_MPC,
        "Il_MPC": Il_MPC,

        "elapsed_MPC_time": elapsed,
        "average_MPC_time": elapsed / sim_steps_MPC,
        "total_MPC_solve_time": total_solve_time,
        "average_MPC_solve_time": average_solve_time,
        "optimization_call_count": len(solve_times),
        "measured_traction_points": measured_traction_points,
        "fuel_cell": hydrogen.results(),
    }

    return mpc_results
