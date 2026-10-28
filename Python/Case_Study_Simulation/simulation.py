"""
Coordinates the complete HYRAILOS Python simulation.

This module reads the user settings, generates current and catenary profiles, initializes the FMU,
runs the DP, MPC, and LPF-EMS simulations, computes energy losses, and sends the results
to the plotting function.
"""

from pathlib import Path

import matplotlib.pyplot as plt

import traction_current
from traction_current import (
    traction_current_disturbance,
    traction_current_generation,
)
from auxiliary_current import auxiliary_current_generation
from catenary_availability import catenary_availability_generation
from dp_simulation import run_dp_simulation
from mpc_simulation import run_mpc_simulation
from lpf_ems_simulation import run_lpf_ems_simulation
from plot_results import plot_simulation_results
from energy_losses import (
    compute_dp_energy_losses,
    compute_lpf_ems_energy_losses,
    compute_mpc_energy_losses,
)
from converter_model import validate_converter_efficiency


plt.rcParams.update({
    # Latex rendering
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble": r"\usepackage{amsmath}",

    # fonts
    "font.size": 21, # all the fonts (generic)
    "axes.labelsize": 23, # axis script size
    "axes.titlesize": 23, # title size
    "xtick.labelsize": 21, # x axis ticks size
    "ytick.labelsize": 21, # y axis ticks size 
    "legend.fontsize": 20, # legend size 

    "lines.linewidth": 2, # line width

    "figure.constrained_layout.use": True, # enables to see the overall figure without blank spaces
})



def run_simulation(settings):

    # ============================================================
    # Read user settings
    # ============================================================
    case_dir = Path(__file__).resolve().parent
    traction_current_path = str(case_dir / settings["traction_current_path"])
    car_types = settings["car_types"]
    n_car = len(car_types)

    cat_pos = settings["cat_pos"]
    data = settings["data"]

    fmu_path = str(case_dir / settings["fmu_path"])
    converter_efficiency = validate_converter_efficiency(
        settings.get("converter_efficiency", 0.97)
    )

    t_start_min = settings["t_start"]
    t_end_min = settings["t_end"]
    tau_s = settings["tau_s"]

    tau_s_MPC = settings["tau_s_MPC"]
    N = settings["N"]

    wfc = settings["wfc"]
    wb = settings["wb"]
    wsc = settings["wsc"]
    wcat = settings["wcat"]

    solver = settings["solver"]
    plot_results = settings.get("plot_results", True)
    save_figures = settings.get("save_figures", True)
    figures_output_dir = settings.get("figures_output_dir")

    if any(ct not in ("t", "a") for ct in car_types):
        raise ValueError("car_types must contain only 't' or 'a'")

    if len(data) != n_car:
        raise ValueError("data must have the same length as car_types")

    if not (0 <= cat_pos <= n_car):
        raise ValueError(f"cat_pos must be between 0 and {n_car}")

    traction_idx = [c for c, ct in enumerate(car_types) if ct == "t"]
    aux_idx = [c for c, ct in enumerate(car_types) if ct == "a"]

    n_trac = len(traction_idx)
    if t_end_min <= t_start_min:
        raise ValueError("t_end must be greater than t_start")

    t_start = t_start_min * 60
    t_end = t_end_min * 60

    sim_steps = int(round((t_end - t_start) / tau_s)) + 1

    sim_steps_MPC = int(round((t_end - t_start) / tau_s_MPC)) + 1

    # ============================================================
    # Signal References (traction current, auxiliary current, catenary availability)
    # ============================================================
    I_t_ref_nominal, I_t_points_nominal = traction_current_generation(
        t_start,
        tau_s,
        tau_s_MPC,
        sim_steps,
        sim_steps_MPC,
        car_types,
        N,
        traction_current_path,
    )

    (
        I_t_ref_plant,
        I_t_points_plant,
        traction_relative_error_ref,
        traction_relative_error_points,
    ) = traction_current_disturbance(
        I_t_ref_nominal=I_t_ref_nominal,
        I_t_points_nominal=I_t_points_nominal,
        tau_s=tau_s,
        tau_s_MPC=tau_s_MPC,
        sim_steps_MPC=sim_steps_MPC,
        car_types=car_types,
    )

    I_a_ref, I_a_points = auxiliary_current_generation(t_start, t_end, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, car_types, N)

    I_ta_ref_plant = I_t_ref_plant + I_a_ref
    I_ta_points_nominal = I_t_points_nominal + I_a_points

    bool_cat_ref, bool_cat_points = catenary_availability_generation(t_start, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, car_types, settings["catenary_intervals"], N)
    if cat_pos == 0:
        bool_cat_ref[:] = 0
        bool_cat_points[:] = 0


    # ============================================================
    # DP
    # ============================================================
    dp_results = run_dp_simulation(
        fmu_path=fmu_path,
        t_start=t_start,
        tau_s=tau_s,
        tau_s_MPC=tau_s_MPC,
        sim_steps=sim_steps,
        sim_steps_MPC=sim_steps_MPC,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        n_trac=n_trac,
        I_t_ref_plant=I_t_ref_plant,
        I_a_ref=I_a_ref,
        I_t_points_nominal=I_t_points_nominal,
        I_a_points=I_a_points,
        I_ta_points_nominal=I_ta_points_nominal,
        bool_cat_ref=bool_cat_ref,
        bool_cat_points=bool_cat_points,
        wfc=wfc,
        wb=wb,
        wsc=wsc,
        wcat=wcat,
        solver=solver,
        cat_pos=cat_pos,
        converter_efficiency=converter_efficiency,
    )


    # ============================================================
    # MPC
    # ============================================================
    mpc_results = run_mpc_simulation(
        fmu_path=fmu_path,
        t_start=t_start,
        tau_s=tau_s,
        tau_s_MPC=tau_s_MPC,
        sim_steps=sim_steps,
        sim_steps_MPC=sim_steps_MPC,
        N=N,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        n_trac=n_trac,
        I_t_ref_plant=I_t_ref_plant,
        I_a_ref=I_a_ref,
        I_t_points_nominal=I_t_points_nominal,
        I_t_points_plant=I_t_points_plant,
        I_a_points=I_a_points,
        I_ta_points_nominal=I_ta_points_nominal,
        bool_cat_points=bool_cat_points,
        wfc=wfc,
        wb=wb,
        wsc=wsc,
        wcat=wcat,
        solver=solver,
        cat_pos=cat_pos,
        converter_efficiency=converter_efficiency,
    )

    time = mpc_results["time"]

    LoH = mpc_results["LoH"]
    SoCb = mpc_results["SoCb"]
    SoCsc = mpc_results["SoCsc"]

    I_fc = mpc_results["I_fc"]
    I_b = mpc_results["I_b"]
    I_sc = mpc_results["I_sc"]
    I_cat = mpc_results["I_cat"]

    V_fc = mpc_results["V_fc"]
    V_b = mpc_results["V_b"]
    V_sc = mpc_results["V_sc"]

    duty_fc = mpc_results["duty_fc"]
    duty_b = mpc_results["duty_b"]
    duty_sc = mpc_results["duty_sc"]

    x = mpc_results["x"]

    Ifc_MPC = mpc_results["Ifc_MPC"]
    Ib_MPC = mpc_results["Ib_MPC"]
    Isc_MPC = mpc_results["Isc_MPC"]

    deltafc = mpc_results["deltafc"]
    deltas = mpc_results["deltas"]
    deltasc = mpc_results["deltasc"]

    dutyfc_MPC = mpc_results["dutyfc_MPC"]
    dutyb_MPC = mpc_results["dutyb_MPC"]
    dutysc_MPC = mpc_results["dutysc_MPC"]

    Icat_MPC = mpc_results["Icat_MPC"]
    Il_MPC = mpc_results["Il_MPC"]

    # ============================================================
    # LPF-EMS
    # ============================================================
    lpf_ems_results = run_lpf_ems_simulation(
        fmu_path=fmu_path,
        t_start=t_start,
        tau_s=tau_s,
        sim_steps=sim_steps,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        n_trac=n_trac,
        I_t_ref=I_t_ref_plant,
        I_a_ref=I_a_ref,
        I_ta_ref=I_ta_ref_plant,
        bool_cat_ref=bool_cat_ref,
        converter_efficiency=converter_efficiency,
    )

    time_lpf = lpf_ems_results["time_lpf"]

    LoH_lpf = lpf_ems_results["LoH_lpf"]
    SoCb_lpf = lpf_ems_results["SoCb_lpf"]
    SoCsc_lpf = lpf_ems_results["SoCsc_lpf"]

    I_fc_lpf = lpf_ems_results["I_fc_lpf"]
    I_b_lpf = lpf_ems_results["I_b_lpf"]
    I_sc_lpf = lpf_ems_results["I_sc_lpf"]

    V_fc_lpf = lpf_ems_results["V_fc_lpf"]
    V_b_lpf = lpf_ems_results["V_b_lpf"]
    V_sc_lpf = lpf_ems_results["V_sc_lpf"]

    duty_fc_lpf = lpf_ems_results["duty_fc_lpf"]
    duty_b_lpf = lpf_ems_results["duty_b_lpf"]
    duty_sc_lpf = lpf_ems_results["duty_sc_lpf"]

    I_cat_lpf = lpf_ems_results["I_cat_lpf"]

    I_fc_ref = lpf_ems_results["I_fc_ref"]
    I_b_ref = lpf_ems_results["I_b_ref"]
    I_sc_ref = lpf_ems_results["I_sc_ref"]
    I_cat_ref = lpf_ems_results["I_cat_ref"]

    # ============================================================
    # ENERGY LOSSES
    # ============================================================
    lpf_ems_losses_kWh = compute_lpf_ems_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC, sim_steps, sim_steps_MPC, 
        I_t_ref_plant, I_a_ref, lpf_ems_results, converter_efficiency
    )
    mpc_losses_kWh = compute_mpc_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
        sim_steps, sim_steps_MPC, I_t_ref_plant, I_a_ref, mpc_results,
        converter_efficiency
    )
    dp_losses_kWh = compute_dp_energy_losses(
        data, car_types, traction_idx, cat_pos, tau_s, tau_s_MPC,
        sim_steps, sim_steps_MPC, I_t_ref_plant, I_a_ref, dp_results,
        converter_efficiency
    )

    # ============================================================
    # PLOTS
    # ============================================================
    saved_figure_paths = []
    if plot_results or save_figures:
        saved_figure_paths = plot_simulation_results(
            mpc_results=mpc_results,
            lpf_ems_results=lpf_ems_results,
            dp_results=dp_results,
            I_t_ref_nominal=I_t_ref_nominal,
            I_t_ref_plant=I_t_ref_plant,
            I_a_ref=I_a_ref,
            tau_s=tau_s,
            tau_s_MPC=tau_s_MPC,
            t_end=t_end,
            traction_idx=traction_idx,
            lpf_ems_losses_kWh=lpf_ems_losses_kWh,
            mpc_losses_kWh=mpc_losses_kWh,
            dp_losses_kWh=dp_losses_kWh,
            converter_efficiency=converter_efficiency,
            save_figures=save_figures,
            output_dir=figures_output_dir,
        )

    if plot_results:
        plt.show()
    elif save_figures:
        plt.close("all")

    profiles = {
        "I_t_ref_nominal": I_t_ref_nominal,
        "I_t_ref_plant": I_t_ref_plant,
        "I_t_points_nominal": I_t_points_nominal,
        "I_t_points_plant": I_t_points_plant,
        "traction_relative_error_ref": traction_relative_error_ref,
        "traction_relative_error_points": traction_relative_error_points,
        "traction_disturbance_fraction": traction_current.TRACTION_DISTURBANCE_FRACTION,
        "traction_disturbance_seed": traction_current.TRACTION_DISTURBANCE_SEED,
        "converter_efficiency": converter_efficiency,
    }
    return {
        "profiles": profiles,
        "mpc": mpc_results,
        "dp": dp_results,
        "lpf_ems": lpf_ems_results,
        "losses_kWh": {
            "lpf_ems": lpf_ems_losses_kWh,
            "mpc": mpc_losses_kWh,
            "dp": dp_losses_kWh,
        },
        "saved_figure_paths": [str(path) for path in saved_figure_paths],
    }
