"""
Creates the comparison plots and summary performances table for the case-study simulation.

The figures compare LPF-EMS, MPC, and DP trajectories. The final table summarizes their
performances and highlights the improvements.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

from converter_model import dc_bus_current
from decimal import Decimal, ROUND_HALF_UP


blue = "#0000ff"
orange_strong = "#ff8c00"
green_strong = "#2ca02c"
purple_strong = "#9467bd"
cyan_strong = "#00a6b2"
yellow_strong = "#E0E40B"
grey_strong = "#737377"
brown_strong = "#8c564b"
teal_strong = "#1b9e77"
pink_strong = "#d40ebac7"
gold_strong = "#c0a324"
orange_light = "#d8991297"
grey_light = "#cecdc9"
charcoal_strong = "#404040"
coral_strong = "#e05a47"
dp_yellow = "#FFC107"
dp_green = "#00929C"
traction_nominal_pink = "#D81B60"
LPF_TRACTION_COLORS = (brown_strong, "m")

DEFAULT_FIGURE_OUTPUT_DIR = (
    Path(__file__).resolve().parent / "Results" / "Figures"
)

STATE_FIGURE_FILENAMES = frozenset({"LoH.pdf", "SoCb.pdf", "SoCsc.pdf"})
STATE_FIGURE_SIZE = (6.4, 4.8)
STATE_AXES_RECT = (0.18, 0.16, 0.665, 0.62)
STATE_LEGEND_BBOX = (0.015, 0.805, 0.97, 0.19)

MPC_TRACTION_COLORS = (
    blue,
    orange_strong,
    green_strong,
    purple_strong,
    cyan_strong,
    yellow_strong,
    grey_strong,
    brown_strong,
    teal_strong,
    pink_strong,
    gold_strong,
    orange_light,
    grey_light,
    charcoal_strong,
    coral_strong,
)

DP_TRACTION_COLORS = (
    dp_yellow,
    dp_green,
    purple_strong,
    cyan_strong,
    gold_strong,
    teal_strong,
    grey_strong,
    brown_strong,
)


def get_mpc_traction_color(traction_position):
    """Return the color for a zero-based traction carriage position."""
    return MPC_TRACTION_COLORS[traction_position % len(MPC_TRACTION_COLORS)]


def get_dp_traction_color(traction_position):
    """Return the DP color for a zero-based traction carriage position."""
    return DP_TRACTION_COLORS[traction_position % len(DP_TRACTION_COLORS)]


def window_peak(x, step):
    n = int(np.ceil(len(x) / step))
    x_peak = np.zeros(n)

    for k in range(n):
        chunk = x[k * step:(k + 1) * step]
        idx = np.argmax(np.abs(chunk))
        x_peak[k] = chunk[idx]

    return x_peak


def _round_half_up(value, digits=0):
    quantizer = Decimal("1").scaleb(-digits)
    return Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP)


def _format_half_up(value, digits=0):
    return f"{_round_half_up(value, digits):.{digits}f}"


def _percent_improvement(baseline_value, mpc_value, higher_is_better=False, display_digits=None):
    if display_digits is not None:
        baseline_value = float(_round_half_up(baseline_value, display_digits))
        mpc_value = float(_round_half_up(mpc_value, display_digits))

    if baseline_value == 0:
        return "/"

    if higher_is_better:
        improvement = (mpc_value - baseline_value) / abs(baseline_value) * 100
    else:
        improvement = (baseline_value - mpc_value) / abs(baseline_value) * 100

    rounded_improvement = int(np.sign(improvement) * np.floor(abs(improvement) + 0.5))
    return rf"{rounded_improvement}\%"


def _new_state_figure():
    """Create one of the three state figures with an invariant plot area."""

    figure = plt.figure(
        figsize=STATE_FIGURE_SIZE,
        constrained_layout=False,
    )
    axes = figure.add_axes(STATE_AXES_RECT)
    plt.sca(axes)
    return figure, axes


def _add_state_legend(figure, axes):
    """Add an identically sized, fully enclosed legend to a state figure."""

    handles, labels = axes.get_legend_handles_labels()
    legend_x, legend_y, legend_width, legend_height = STATE_LEGEND_BBOX

    legend_frame = FancyBboxPatch(
        (legend_x, legend_y),
        legend_width,
        legend_height,
        boxstyle="round,pad=0.0,rounding_size=0.01",
        transform=figure.transFigure,
        facecolor="white",
        edgecolor="0.8",
        linewidth=1.0,
        zorder=4,
    )
    figure.add_artist(legend_frame)

    legend = figure.legend(
        handles,
        labels,
        loc="center",
        bbox_to_anchor=STATE_LEGEND_BBOX,
        bbox_transform=figure.transFigure,
        mode="expand",
        ncol=3,
        frameon=False,
        fontsize=19,
        borderaxespad=0.0,
        borderpad=0.15,
        labelspacing=0.4,
        columnspacing=0.65,
        handlelength=1,
        handletextpad=0.3,
    )
    legend.set_zorder(5)
    return legend


def _save_figures(figures, output_dir=None):
    """Overwrite all generated PDFs in the configured results directory."""

    if output_dir is None:
        resolved_output_dir = DEFAULT_FIGURE_OUTPUT_DIR
    else:
        resolved_output_dir = Path(output_dir).expanduser()
        if not resolved_output_dir.is_absolute():
            resolved_output_dir = Path(__file__).resolve().parent / resolved_output_dir

    resolved_output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for filename, figure in figures.items():
        output_path = resolved_output_dir / filename
        if filename in STATE_FIGURE_FILENAMES:
            # Keep the exact same physical PDF dimensions for all state plots.
            figure.savefig(output_path, format="pdf")
        else:
            figure.savefig(output_path, format="pdf", bbox_inches="tight")
        saved_paths.append(output_path)

    print(
        f"Saved {len(saved_paths)} figure PDFs to "
        f"{resolved_output_dir}"
    )
    return saved_paths


def plot_simulation_results(
    mpc_results,
    lpf_ems_results,
    dp_results,
    I_t_ref_nominal,
    I_t_ref_plant,
    I_a_ref,
    tau_s,
    tau_s_MPC,
    t_end,
    traction_idx,
    lpf_ems_losses_kWh,
    mpc_losses_kWh,
    dp_losses_kWh,
    converter_efficiency,
    save_figures=True,
    output_dir=None,
):
    def _dc_current(source_current, duty):
        return dc_bus_current(
            source_current, 1.0 - duty, converter_efficiency
        )

    figures = {}

    time = mpc_results["time"]
    time_lpf = lpf_ems_results["time_lpf"]
    time_dp = dp_results["time_dp"]

    LoH = mpc_results["LoH"]
    SoCb = mpc_results["SoCb"]
    SoCsc = mpc_results["SoCsc"]

    I_fc = mpc_results["I_fc"]
    I_b = mpc_results["I_b"]
    I_sc = mpc_results["I_sc"]
    I_cat = mpc_results["I_cat"]

    duty_fc = mpc_results["duty_fc"]
    duty_b = mpc_results["duty_b"]
    duty_sc = mpc_results["duty_sc"]

    LoH_lpf = lpf_ems_results["LoH_lpf"]
    SoCb_lpf = lpf_ems_results["SoCb_lpf"]
    SoCsc_lpf = lpf_ems_results["SoCsc_lpf"]

    I_fc_lpf = lpf_ems_results["I_fc_lpf"]
    I_b_lpf = lpf_ems_results["I_b_lpf"]
    I_sc_lpf = lpf_ems_results["I_sc_lpf"]
    I_cat_lpf = lpf_ems_results["I_cat_lpf"]

    duty_fc_lpf = lpf_ems_results["duty_fc_lpf"]
    duty_b_lpf = lpf_ems_results["duty_b_lpf"]
    duty_sc_lpf = lpf_ems_results["duty_sc_lpf"]

    LoH_dp = dp_results["LoH_dp"]
    SoCb_dp = dp_results["SoCb_dp"]
    SoCsc_dp = dp_results["SoCsc_dp"]

    I_fc_dp = dp_results["I_fc_dp"]
    I_b_dp = dp_results["I_b_dp"]
    I_sc_dp = dp_results["I_sc_dp"]

    duty_fc_dp = dp_results["duty_fc_dp"]
    duty_b_dp = dp_results["duty_b_dp"]
    duty_sc_dp = dp_results["duty_sc_dp"]

    time_min = time / 60
    x_lim_min = t_end / 60

    step_mpc = int(tau_s_MPC / tau_s)

    time_mpc_min = time_min[::step_mpc]
    time_dp_mpc_min = time_dp[::step_mpc] / 60

    LoH_lpf_smooth = {c: window_peak(LoH_lpf[c], step_mpc) for c in traction_idx}
    SoCb_lpf_smooth = {c: window_peak(SoCb_lpf[c], step_mpc) for c in traction_idx}
    SoCsc_lpf_smooth = {c: window_peak(SoCsc_lpf[c], step_mpc) for c in traction_idx}

    I_fc_lpf_smooth = {
        c: window_peak(_dc_current(I_fc_lpf[c], duty_fc_lpf[c]), step_mpc)
        for c in traction_idx
    }
    I_b_lpf_smooth = {
        c: window_peak(_dc_current(I_b_lpf[c], duty_b_lpf[c]), step_mpc)
        for c in traction_idx
    }
    I_sc_lpf_smooth = {
        c: window_peak(_dc_current(I_sc_lpf[c], duty_sc_lpf[c]), step_mpc)
        for c in traction_idx
    }
    I_cat_lpf_smooth = window_peak(I_cat_lpf, step_mpc)

    time_lpf_mpc_min = time_lpf[::step_mpc] / 60

    # ============================================================
    # LoH
    # ============================================================
    loh_figure, loh_axes = _new_state_figure()
    figures["LoH.pdf"] = loh_figure
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            LoH_lpf_smooth[c],
            label=fr"$LoH^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            LoH_dp[c][::step_mpc],
            label=fr"$LoH^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            LoH[c][::step_mpc],
            label=fr"$LoH^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )
    plt.axhline(y=0.9, color="red", linewidth=2) #label= r"$LoH^{[i]}_{MAX}$ = 0.9"
    plt.axhline(y=0.1, color="red", linewidth=2) #label=r"$LoH^{[i]}_{min}$ = 0.1"
    plt.axhline(y=0.6, color="red", linestyle="--", linewidth=2) #label=r"$LoH^{[i]}_{th}$ = 0.6"
    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Fuel cell LoH")
    plt.xlim([0, x_lim_min])
    plt.ylim([0, 1])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(0, 0.9, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    _add_state_legend(loh_figure, loh_axes)

    # ============================================================
    # SoCb
    # ============================================================
    socb_figure, socb_axes = _new_state_figure()
    figures["SoCb.pdf"] = socb_figure
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            SoCb_lpf_smooth[c],
            label=fr"$SoC_{{\text{{b}}}}^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            SoCb_dp[c][::step_mpc],
            label=fr"$SoC_{{\text{{b}}}}^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            SoCb[c][::step_mpc],
            label=fr"$SoC_{{\text{{b}}}}^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )
    plt.axhline(y=0.1, color="red", linewidth=2)
    plt.axhline(y=0.6, color="red", linestyle="--", linewidth=2)
    plt.axhline(y=0.9, color="red", linewidth=2)
    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Battery SoC")
    plt.xlim([0, x_lim_min])
    plt.ylim([0, 1])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(0, 0.9, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    _add_state_legend(socb_figure, socb_axes)

    # ============================================================
    # SoCsc
    # ============================================================
    socsc_figure, socsc_axes = _new_state_figure()
    figures["SoCsc.pdf"] = socsc_figure
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            SoCsc_lpf_smooth[c],
            label=fr"$SoC_{{\text{{sc}}}}^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            SoCsc_dp[c][::step_mpc],
            label=fr"$SoC_{{\text{{sc}}}}^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            SoCsc[c][::step_mpc],
            label=fr"$SoC_{{\text{{sc}}}}^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )
    plt.axhline(y=0.1, color="red", linewidth=2)
    plt.axhline(y=0.6, color="red", linestyle="--", linewidth=2)
    plt.axhline(y=0.9, color="red", linewidth=2)
    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Supercapacitor SoC")
    plt.xlim([0, x_lim_min])
    plt.ylim([0, 1])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(0, 0.9, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    _add_state_legend(socsc_figure, socsc_axes)

    # ============================================================
    # Fuel cell current
    # ============================================================
    figures["IDCfc.pdf"] = plt.figure()
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            I_fc_lpf_smooth[c],
            label=fr"$I_{{\text{{DCfc}}}}^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            _dc_current(
                I_fc_dp[c][::step_mpc], duty_fc_dp[c][::step_mpc]
            ),
            label=fr"$I_{{\text{{DCfc}}}}^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            _dc_current(I_fc[c][::step_mpc], duty_fc[c][::step_mpc]),
            label=fr"$I_{{\text{{DCfc}}}}^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )

    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Fuel cell current (A)")
    plt.xlim([0, x_lim_min])
    plt.ylim([-5, 80])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(0, 75, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    plt.legend(
        loc="lower center",
        bbox_to_anchor=(0.48, 0.98),
        ncol=3,
        frameon=True,
        columnspacing=0.8, 
        handlelength=1,  
        handletextpad=0.3,  
    )
    
    Ifc_lpf_avg = np.mean(I_fc_lpf_smooth[0])
    I_fc_avg = np.mean([
        np.mean(_dc_current(I_fc[c][::step_mpc], duty_fc[c][::step_mpc]))
        for c in traction_idx
    ])
    I_fc_dp_avg = np.mean([
        np.mean(
            _dc_current(
                I_fc_dp[c][::step_mpc], duty_fc_dp[c][::step_mpc]
            )
        )
        for c in traction_idx
    ])


    LoH_lpf_end = LoH_lpf[0][-1]
    LoH_mpc_end = np.min([LoH[c][-1] for c in traction_idx])
    LoH_dp_end = np.min([LoH_dp[c][-1] for c in traction_idx])
    I_sc_lpf_max = np.max(np.abs(I_sc_lpf_smooth[0]))
    I_sc_mpc_max = np.max([
        np.max(
            np.abs(_dc_current(I_sc[c][::step_mpc], duty_sc[c][::step_mpc]))
        )
        for c in traction_idx
    ])
    I_sc_dp_max = np.max([
        np.max(
            np.abs(
                _dc_current(
                    I_sc_dp[c][::step_mpc],
                    duty_sc_dp[c][::step_mpc],
                )
            )
        )
        for c in traction_idx
    ])

    total_mpc_solve_time = mpc_results["total_MPC_solve_time"]
    average_mpc_solve_time = mpc_results["average_MPC_solve_time"]
    total_dp_solve_time = dp_results["total_DP_solve_time"]
    average_dp_solve_time = dp_results["average_DP_solve_time"]

    # ============================================================
    # Battery current
    # ============================================================
    figures["IDCb.pdf"] = plt.figure()
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            I_b_lpf_smooth[c],
            label=fr"$I_{{\text{{DCb}}}}^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            _dc_current(
                I_b_dp[c][::step_mpc], duty_b_dp[c][::step_mpc]
            ),
            label=fr"$I_{{\text{{DCb}}}}^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            _dc_current(I_b[c][::step_mpc], duty_b[c][::step_mpc]),
            label=fr"$I_{{\text{{DCb}}}}^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )

    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Battery current (A)")
    plt.xlim([0, x_lim_min])
    plt.ylim([-100, 200])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(-70, 140, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    plt.legend(
        loc="lower center",
        bbox_to_anchor=(0.48, 0.98),
        ncol=3,
        frameon=True,
        columnspacing=0.8,  
        handlelength=1,  
        handletextpad=0.3,  
    )

    # ============================================================
    # Supercapacitor current
    # ============================================================
    figures["IDCsc.pdf"] = plt.figure()
    for traction_position, c in enumerate(traction_idx):
        plt.plot(
            time_lpf_mpc_min,
            I_sc_lpf_smooth[c],
            label=fr"$I_{{\text{{DCsc}}}}^{{[{c + 1}]}}$ LPF-EMS",
            linestyle="--",
            color=LPF_TRACTION_COLORS[traction_position % len(LPF_TRACTION_COLORS)],
            linewidth=3,
            zorder=2,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_dp_traction_color(traction_position)
        plt.plot(
            time_dp_mpc_min,
            _dc_current(
                I_sc_dp[c][::step_mpc], duty_sc_dp[c][::step_mpc]
            ),
            label=fr"$I_{{\text{{DCsc}}}}^{{[{c + 1}]}}$ DP",
            color=color,
            linestyle="dotted",
            linewidth=3,
            zorder=3 + traction_position,
        )

    for traction_position, c in enumerate(traction_idx):
        color = get_mpc_traction_color(traction_position)
        plt.plot(
            time_mpc_min,
            _dc_current(I_sc[c][::step_mpc], duty_sc[c][::step_mpc]),
            label=fr"$I_{{\text{{DCsc}}}}^{{[{c + 1}]}}$ MPC",
            color=color,
            linewidth=3,
            zorder=10 + traction_position,
        )

    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Supercapacitor current (A)")
    plt.xlim([0, x_lim_min])
    plt.ylim([-100, 160])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(-60, 120, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5)
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    plt.legend(
        loc="lower center",
        bbox_to_anchor=(0.48, 0.98),
        ncol=3,
        frameon=True,
        columnspacing=0.8,  
        handlelength=1,  
        handletextpad=0.3,  
    )

    # ============================================================
    # Traction current
    # ============================================================
    figures["It.pdf"] = plt.figure()
    plt.plot(
        time_mpc_min,
        I_t_ref_nominal[0, :len(time)][::step_mpc],
        label=r"$I_{\mathrm{t,nom}}^{[1]}$",
        color=traction_nominal_pink,
        linestyle="--",
        linewidth=3,
        zorder=2,
    )
    plt.plot(
        time_mpc_min,
        I_t_ref_plant[0, :len(time)][::step_mpc],
        label=r"$I_{\mathrm{t,plant}}^{[1]}$",
        color=blue,
        linewidth=4,
        zorder=3,
    )

    plt.xlabel(r"Time (min)")
    plt.ylabel(r"Traction current (A)")
    plt.xlim([0, x_lim_min])
    plt.ylim([-150, 250])
    plt.xticks(np.linspace(0, 180, 4))
    plt.yticks(np.linspace(-100, 200, 4))
    plt.axvspan(20, 60, color="0.85", alpha=0.5, label="Catenary-free")
    plt.axvspan(100, 160, color="0.85", alpha=0.5)
    plt.legend(
        loc="lower center",
        bbox_to_anchor=(0.48, 0.98),
        ncol=2,
        frameon=True,
    )

    # ============================================================
    # Performance comparison table
    # ============================================================
    table_rows = [
        [
            r"$LoH_{\mathrm{end}}^{[i]}$",
            _format_half_up(LoH_lpf_end, 2),
            _format_half_up(LoH_dp_end, 2),
            _format_half_up(LoH_mpc_end, 2),
            "/",
            _percent_improvement(LoH_lpf_end, LoH_dp_end, higher_is_better=True, display_digits=2),
            _percent_improvement(LoH_lpf_end, LoH_mpc_end, higher_is_better=True, display_digits=2),
        ],
        [
            r"$I_{\mathrm{DCsc}}^{\max}$",
            _format_half_up(I_sc_lpf_max, 0),
            _format_half_up(I_sc_dp_max, 0),
            _format_half_up(I_sc_mpc_max, 0),
            "A",
            _percent_improvement(I_sc_lpf_max, I_sc_dp_max, display_digits=0),
            _percent_improvement(I_sc_lpf_max, I_sc_mpc_max, display_digits=0),
        ],
        [
            r"$I_{\mathrm{DCfc}}^{\mathrm{avg}}$",
            _format_half_up(Ifc_lpf_avg, 1),
            _format_half_up(I_fc_dp_avg, 1),
            _format_half_up(I_fc_avg, 1),
            "A",
            _percent_improvement(Ifc_lpf_avg, I_fc_dp_avg, display_digits=1),
            _percent_improvement(Ifc_lpf_avg, I_fc_avg, display_digits=1),
        ],
        [
            "Energy losses",
            _format_half_up(lpf_ems_losses_kWh, 2),
            _format_half_up(dp_losses_kWh, 2),
            _format_half_up(mpc_losses_kWh, 2),
            "kWh",
            _percent_improvement(lpf_ems_losses_kWh, dp_losses_kWh, display_digits=2),
            _percent_improvement(lpf_ems_losses_kWh, mpc_losses_kWh, display_digits=2),
        ],
        [
            "Total optimization time",
            "/",
            _format_half_up(total_dp_solve_time, 2),
            _format_half_up(total_mpc_solve_time, 2),
            "s",
            "/",
            "/",
        ],
        [
            "Average solve time",
            "/",
            _format_half_up(average_dp_solve_time, 2),
            _format_half_up(average_mpc_solve_time, 2),
            "s",
            "/",
            "/",
        ],
    ]

    fig, ax = plt.subplots(figsize=(15.5, 4.0))
    figures["Performance_Table_LPF-EMS_vs_DP_vs_MPC.pdf"] = fig
    ax.axis("off")
    table = ax.table(
        cellText=table_rows,
        colLabels=[
            "",
            "LPF-EMS",
            "DP",
            "MPC",
            "Unit",
            "DP improvement",
            "MPC improvement",
        ],
        cellLoc="center",
        colLoc="center",
        loc="center",
        bbox=[0.01, 0.08, 0.98, 0.84],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    table.scale(1.0, 1.65)

    for (row, col), cell in table.get_celld().items():
        cell.visible_edges = ""
        cell.set_linewidth(0.0)
        cell.PAD = 0.18
        if row == 0:
            cell.set_text_props(weight="bold")

    ax.plot([0.01, 0.99], [0.94, 0.94], color="black", linewidth=1.8, transform=ax.transAxes, clip_on=False)
    ax.plot([0.01, 0.99], [0.82, 0.82], color="black", linewidth=0.9, transform=ax.transAxes, clip_on=False)
    ax.plot([0.01, 0.99], [0.06, 0.06], color="black", linewidth=1.8, transform=ax.transAxes, clip_on=False)

    if save_figures:
        return _save_figures(figures, output_dir=output_dir)

    return []
