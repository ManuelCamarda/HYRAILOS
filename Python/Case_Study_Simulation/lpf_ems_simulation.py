"""Run the LPF-EMS simulation.

The benchmark uses frequency splitting instead of fixed operating thresholds:

* a fast low-pass filter separates rapid demand changes from the rest;
* a slower low-pass filter separates the battery's medium-frequency share from
  the fuel-cell/catenary base load;
* local state-of-charge feedback keeps every supercapacitor near 50 percent
  and the batteries near their configured target, while rated-current
  saturation prevents excessive supercapacitor peaks;
* the fuel cells supply a capped, ramp-limited base contribution, reduced to a
  configurable share while the catenary is available; and
* the batteries close the instantaneous current balance.

The controller uses the current demand, its filter states,
and the latest FMU states. Currents inside the controller are DC-bus currents;
they are converted to source-side references before being sent to the FMU.
"""

import numpy as np

from converter_model import (
    conversion_ratio_from_duty,
    dc_bus_current,
    source_current_from_dc_bus,
    validate_converter_efficiency,
)
from fmu_initialization import initialize_fmu, terminate_fmu
from fuel_cell_model import HydrogenRecorder, validate_fuel_cell_parameters


# Edit the LPF-EMS tuning here. Current limits and SoC corrections are per carriage.
LPF_EMS_SETTINGS = {
    "tau_fast": 60.0,                 # First LPF time constant [s]
    "tau_slow": 300.0,                # Base-load LPF time constant [s]
    "sc_target": 0.50,
    "sc_deadband": 0.05,              # No restoration inside 45%-55% SoC
    "sc_soc_gain": 15.0,              # DC-bus A per unit SoC error
    "sc_correction_limit": 4.0,       # Maximum restoration correction [DC-bus A]
    "sc_operating_min": 0.20,         # Discharge taper reaches zero here
    "sc_operating_max": 0.85,         # Charge taper reaches zero here
    "sc_source_current_limit": 300.0, # Symmetric source-side limit [A]
    "b_target": 0.65,
    "b_deadband": 0.05,               # No restoration inside 60%-70% SoC
    "b_soc_gain": 60.0,               # DC-bus A per unit SoC error
    "b_correction_limit": 10.0,       # Maximum restoration correction [DC-bus A]
    "fc_ramp_source_A_per_min": 20.0,
    "fc_source_current_limit": 80.0,  # Source-side current ceiling [A]
    "fc_catenary_share": 0.15,        # Share of positive base demand when electrified
    "fc_loh_soft_min": 0.50,          # Requested contribution reaches zero here
    "fc_loh_full": 0.60,              # Full contribution above this hydrogen level
    "source_current_limit": 6500.0,   # General source-side current bound [A]
    "hard_soc_min": 0.10,
    "hard_soc_max": 0.90,
}


def _deadband(value, target, half_width):
    """Return signed target error after removing a symmetric deadband."""
    error = value - target
    if error > half_width:
        return error - half_width
    if error < -half_width:
        return error + half_width
    return 0.0


def _supercapacitor_taper(command, soc, target, soc_min, soc_max):
    """Smoothly suppress commands that would move the SoC toward a limit."""
    if command >= 0.0:  # discharge
        gain = np.clip((soc - soc_min) / (target - soc_min), 0.0, 1.0)
    else:  # charge / regenerative braking
        gain = np.clip((soc_max - soc) / (soc_max - target), 0.0, 1.0)
    return command * gain


class LPFEMSController:
    """Causal rule-based controller used by the LPF-EMS FMU simulation."""

    def __init__(
        self,
        tau_s,
        traction_idx,
        data,
        converter_efficiency,
        config=None,
    ):
        config = {**LPF_EMS_SETTINGS, **({} if config is None else config)}
        self.tau_s = float(tau_s)
        self.traction_idx = list(traction_idx)
        self.data = data
        for c in self.traction_idx:
            validate_fuel_cell_parameters(data[c])
        self.n_trac = len(self.traction_idx)
        self.converter_efficiency = validate_converter_efficiency(
            converter_efficiency
        )

        self.tau_fast = float(config["tau_fast"])
        self.tau_slow = float(config["tau_slow"])
        self.sc_target = float(config["sc_target"])
        self.sc_deadband = float(config["sc_deadband"])
        self.sc_soc_gain = float(config["sc_soc_gain"])
        self.sc_correction_limit = float(config["sc_correction_limit"])
        self.sc_operating_min = float(config["sc_operating_min"])
        self.sc_operating_max = float(config["sc_operating_max"])
        self.sc_source_current_limit = float(config["sc_source_current_limit"])

        self.b_target = float(config["b_target"])
        self.b_deadband = float(config["b_deadband"])
        self.b_soc_gain = float(config["b_soc_gain"])
        self.b_correction_limit = float(config["b_correction_limit"])

        self.fc_ramp_source_A_per_min = float(config["fc_ramp_source_A_per_min"])
        self.fc_source_current_limit = float(config["fc_source_current_limit"])
        self.fc_catenary_share = float(config["fc_catenary_share"])
        self.fc_loh_soft_min = float(config["fc_loh_soft_min"])
        self.fc_loh_full = float(config["fc_loh_full"])
        self.source_current_limit = float(config["source_current_limit"])
        self.hard_soc_min = float(config["hard_soc_min"])
        self.hard_soc_max = float(config["hard_soc_max"])

        if self.n_trac == 0:
            raise ValueError("LPF-EMS requires at least one traction carriage")
        if not (0.0 < self.tau_fast < self.tau_slow):
            raise ValueError("Require 0 < tau_fast < tau_slow")
        if not (
            self.hard_soc_min
            < self.sc_operating_min
            < self.sc_target
            < self.sc_operating_max
            < self.hard_soc_max
        ):
            raise ValueError("Invalid supercapacitor SoC targets or limits")
        if not (self.hard_soc_min < self.b_target < self.hard_soc_max):
            raise ValueError("Invalid battery SoC target")
        if not (
            self.hard_soc_min < self.fc_loh_soft_min < self.fc_loh_full <= 1.0
        ):
            raise ValueError("Invalid fuel-cell LoH protection thresholds")
        if not (0.0 < self.fc_source_current_limit <= self.source_current_limit):
            raise ValueError("Invalid fuel-cell source-current limit")
        if not (0.0 <= self.fc_catenary_share <= 1.0):
            raise ValueError("Fuel-cell catenary share must be in [0, 1]")
        if not (0.0 < self.sc_source_current_limit <= self.source_current_limit):
            raise ValueError("Invalid supercapacitor source-current limit")

        self.alpha_fast = np.exp(-self.tau_s / self.tau_fast)
        self.alpha_slow = np.exp(-self.tau_s / self.tau_slow)
        self.fast_state = None
        self.slow_state = None
        self.previous_fc_source = np.zeros(self.n_trac)

    def _state_current_limits(self, c, soc, duty, storage):
        """DC-current limits that keep the next ideal state inside hard bounds."""
        ratio = conversion_ratio_from_duty(duty)
        if storage == "battery":
            capacity_factor = self.data[c].ccb
            device_current_limit = self.source_current_limit
        else:
            capacity_factor = self.data[c].ccsc / self.data[c].V_nom_sc
            device_current_limit = self.sc_source_current_limit

        max_discharge_source = (
            max(soc - self.hard_soc_min, 0.0)
            * capacity_factor
            * 3600.0
            / self.tau_s
        )
        max_charge_source = (
            max(self.hard_soc_max - soc, 0.0)
            * capacity_factor
            * 3600.0
            / self.tau_s
        )
        max_discharge_source = min(max_discharge_source, device_current_limit)
        max_charge_source = min(max_charge_source, device_current_limit)
        return (
            dc_bus_current(
                -max_charge_source, ratio, self.converter_efficiency
            ),
            dc_bus_current(
                max_discharge_source, ratio, self.converter_efficiency
            ),
        )

    @staticmethod
    def _close_residual(commands, residual, lower, upper):
        """Distribute a bus-current residual over devices with available margin."""
        commands = np.asarray(commands, dtype=float).copy()
        for _ in range(len(commands) + 1):
            if abs(residual) <= 1e-10:
                break
            if residual > 0.0:
                margin = np.maximum(np.asarray(upper) - commands, 0.0)
            else:
                margin = np.maximum(commands - np.asarray(lower), 0.0)
            active = margin > 1e-12
            if not np.any(active):
                break
            increment = residual / np.count_nonzero(active)
            if residual > 0.0:
                change = np.minimum(increment, margin)
            else:
                change = -np.minimum(-increment, margin)
            commands += change
            residual -= float(np.sum(change))
        return commands, residual

    def step(self, demand, catenary_available, loh, soc_b, soc_sc, duties):
        """Compute one set of DC-bus current commands."""
        demand = float(demand)

        # Initialize both filters at the first demand so startup is not treated
        # as an artificial high-frequency transient.
        if self.fast_state is None:
            self.fast_state = demand
            self.slow_state = demand
        else:
            self.fast_state = (
                self.alpha_fast * self.fast_state
                + (1.0 - self.alpha_fast) * demand
            )
            self.slow_state = (
                self.alpha_slow * self.slow_state
                + (1.0 - self.alpha_slow) * self.fast_state
            )

        high_frequency = demand - self.fast_state
        medium_frequency = self.fast_state - self.slow_state

        sc_commands = np.zeros(self.n_trac)
        b_desired = np.zeros(self.n_trac)
        sc_lower = np.zeros(self.n_trac)
        sc_upper = np.zeros(self.n_trac)
        b_lower = np.zeros(self.n_trac)
        b_upper = np.zeros(self.n_trac)

        for p, c in enumerate(self.traction_idx):
            sc_feedback = np.clip(
                self.sc_soc_gain
                * _deadband(soc_sc[p], self.sc_target, self.sc_deadband),
                -self.sc_correction_limit,
                self.sc_correction_limit,
            )
            sc_command = high_frequency / self.n_trac + sc_feedback
            sc_command = _supercapacitor_taper(
                sc_command,
                soc_sc[p],
                self.sc_target,
                self.sc_operating_min,
                self.sc_operating_max,
            )
            sc_lower[p], sc_upper[p] = self._state_current_limits(
                c, soc_sc[p], duties["sc"][p], "supercapacitor"
            )
            sc_commands[p] = np.clip(sc_command, sc_lower[p], sc_upper[p])

            b_feedback = np.clip(
                self.b_soc_gain
                * _deadband(soc_b[p], self.b_target, self.b_deadband),
                -self.b_correction_limit,
                self.b_correction_limit,
            )
            b_lower[p], b_upper[p] = self._state_current_limits(
                c, soc_b[p], duties["b"][p], "battery"
            )
            b_desired[p] = np.clip(
                medium_frequency / self.n_trac + b_feedback,
                b_lower[p],
                b_upper[p],
            )

        # The required slow source includes SoC restoration: discharging storage
        # above its target reduces base-source demand; charging it increases it.
        slow_source_required = demand - np.sum(sc_commands) - np.sum(b_desired)

        fc_commands = np.zeros(self.n_trac)
        ramp_per_step = self.fc_ramp_source_A_per_min * self.tau_s / 60.0
        # Keep the fuel cells online in electrified sections by assigning them
        # a small share of positive base demand. They are not forced to produce
        # during zero demand or regenerative braking, avoiding needless export.
        fc_share = self.fc_catenary_share if catenary_available else 1.0
        target_fc_total = fc_share * max(slow_source_required, 0.0)

        for p, c in enumerate(self.traction_idx):
            ratio = conversion_ratio_from_duty(duties["fc"][p])
            rated_current_limit = min(
                self.fc_source_current_limit,
                self.data[c].Pfc_rated / self.data[c].V_nom_fc,
            )
            target_source = source_current_from_dc_bus(
                target_fc_total / self.n_trac,
                ratio,
                self.converter_efficiency,
            )
            # Reduce fuel-cell use continuously below ``fc_loh_full`` and hand
            # the resulting deficit to the batteries. This avoids a new hard
            # switching rule at the fuel reserve threshold.
            loh_gain = np.clip(
                (loh[p] - self.fc_loh_soft_min)
                / (self.fc_loh_full - self.fc_loh_soft_min),
                0.0,
                1.0,
            )
            target_source *= loh_gain
            target_source = np.clip(
                target_source, 0.0, rated_current_limit
            )
            source_command = np.clip(
                target_source,
                self.previous_fc_source[p] - ramp_per_step,
                self.previous_fc_source[p] + ramp_per_step,
            )
            source_command = np.clip(
                source_command, 0.0, rated_current_limit
            )
            self.previous_fc_source[p] = source_command
            fc_commands[p] = dc_bus_current(
                source_command, ratio, self.converter_efficiency
            )

        if catenary_available:
            # The catenary closes the balance after the reduced fuel-cell share.
            b_commands = b_desired
            cat_command = demand - np.sum(fc_commands + b_commands + sc_commands)
        else:
            cat_command = 0.0
            # Batteries are the medium-frequency buffer and close the balance
            # left by the ramp-limited fuel cells.
            b_commands = b_desired.copy()
            residual = demand - np.sum(fc_commands + b_commands + sc_commands)
            b_commands, residual = self._close_residual(
                b_commands, residual, b_lower, b_upper
            )
            if abs(residual) > 1e-10:
                sc_commands, residual = self._close_residual(
                    sc_commands, residual, sc_lower, sc_upper
                )
            if abs(residual) > 1e-6:
                raise RuntimeError(
                    "LPF-EMS cannot balance demand within storage limits "
                    f"(residual {residual:.6g} A)"
                )

        return {
            "fc": fc_commands,
            "b": b_commands,
            "sc": sc_commands,
            "cat": float(cat_command),
            "fast_lpf": float(self.fast_state),
            "slow_lpf": float(self.slow_state),
            "high_frequency": float(high_frequency),
            "medium_frequency": float(medium_frequency),
        }


def run_lpf_ems_simulation(
    fmu_path,
    t_start,
    tau_s,
    sim_steps,
    car_types,
    data,
    traction_idx,
    n_trac,
    I_t_ref,
    I_a_ref,
    I_ta_ref,
    bool_cat_ref,
    lpf_ems_config=None,
    converter_efficiency=0.97,
):
    n_car = len(car_types)
    if n_trac != len(traction_idx):
        raise ValueError("n_trac must match traction_idx")

    controller = LPFEMSController(
        tau_s=tau_s,
        traction_idx=traction_idx,
        data=data,
        converter_efficiency=converter_efficiency,
        config=lpf_ems_config,
    )

    fmu, md, vr = initialize_fmu(
        fmu_path=fmu_path,
        t_start=t_start,
        car_types=car_types,
        data=data,
        traction_idx=traction_idx,
        converter_efficiency=converter_efficiency,
    )

    time_lpf = []

    LoH_lpf = {c: [] for c in traction_idx}
    SoCb_lpf = {c: [] for c in traction_idx}
    SoCsc_lpf = {c: [] for c in traction_idx}

    I_fc_lpf = {c: [] for c in traction_idx}
    I_b_lpf = {c: [] for c in traction_idx}
    I_sc_lpf = {c: [] for c in traction_idx}

    V_fc_lpf = {c: [] for c in traction_idx}
    V_b_lpf = {c: [] for c in traction_idx}
    V_sc_lpf = {c: [] for c in traction_idx}

    duty_fc_lpf = {c: [] for c in traction_idx}
    duty_b_lpf = {c: [] for c in traction_idx}
    duty_sc_lpf = {c: [] for c in traction_idx}

    P_loss_fc_lpf = {c: [] for c in traction_idx}
    P_loss_b_lpf = {c: [] for c in traction_idx}
    P_loss_sc_lpf = {c: [] for c in traction_idx}

    I_cat_lpf = []
    I_ta_ref_tot = np.sum(I_ta_ref, axis=0)

    I_fc_ref = {c: np.zeros(sim_steps) for c in traction_idx}
    I_b_ref = {c: np.zeros(sim_steps) for c in traction_idx}
    I_sc_ref = {c: np.zeros(sim_steps) for c in traction_idx}
    I_cat_ref = np.zeros(sim_steps)

    fast_lpf_ref = np.zeros(sim_steps)
    slow_lpf_ref = np.zeros(sim_steps)
    high_frequency_ref = np.zeros(sim_steps)
    medium_frequency_ref = np.zeros(sim_steps)

    current_soc_b = np.array([data[c].SoCb_initial for c in traction_idx])
    current_soc_sc = np.array([data[c].SoCsc_initial for c in traction_idx])
    current_loh = np.array([data[c].LoH_initial for c in traction_idx])
    current_duties = {
        "fc": np.array([1.0 - data[c].Dfc for c in traction_idx]),
        "b": np.array([1.0 - data[c].Db for c in traction_idx]),
        "sc": np.array([1.0 - data[c].Dsc for c in traction_idx]),
    }

    t = t_start
    hydrogen = HydrogenRecorder(data, traction_idx)
    hydrogen.record(fmu, vr, t)

    try:
        for j in range(sim_steps):
            if j == 0:
                for c in traction_idx:
                    LoH_lpf[c].append(data[c].LoH_initial)
                    SoCb_lpf[c].append(data[c].SoCb_initial)
                    SoCsc_lpf[c].append(data[c].SoCsc_initial)

            commands = controller.step(
                demand=I_ta_ref_tot[j],
                catenary_available=bool(bool_cat_ref[j]),
                loh=current_loh,
                soc_b=current_soc_b,
                soc_sc=current_soc_sc,
                duties=current_duties,
            )

            for p, c in enumerate(traction_idx):
                I_fc_ref[c][j] = commands["fc"][p]
                I_b_ref[c][j] = commands["b"][p]
                I_sc_ref[c][j] = commands["sc"][p]
            I_cat_ref[j] = commands["cat"]
            fast_lpf_ref[j] = commands["fast_lpf"]
            slow_lpf_ref[j] = commands["slow_lpf"]
            high_frequency_ref[j] = commands["high_frequency"]
            medium_frequency_ref[j] = commands["medium_frequency"]

            vr_set = []
            val_set = []

            for c in range(n_car):
                vr_set.append(vr["ia_ref"][c])
                val_set.append(I_a_ref[c, j])

                if car_types[c] == "t":
                    vr_set.append(vr["it_ref"][c])
                    val_set.append(I_t_ref[c, j])

            for p, c in enumerate(traction_idx):
                vr_set.extend([
                    vr["ifc_ref"][c],
                    vr["ib_ref"][c],
                    vr["isc_ref"][c],
                ])
                val_set.extend([
                    source_current_from_dc_bus(
                        I_fc_ref[c][j],
                        conversion_ratio_from_duty(current_duties["fc"][p]),
                        converter_efficiency,
                    ),
                    source_current_from_dc_bus(
                        I_b_ref[c][j],
                        conversion_ratio_from_duty(current_duties["b"][p]),
                        converter_efficiency,
                    ),
                    source_current_from_dc_bus(
                        I_sc_ref[c][j],
                        conversion_ratio_from_duty(current_duties["sc"][p]),
                        converter_efficiency,
                    ),
                ])

            vr_set.extend([vr["icat_ref"], vr["bool_cat"]])
            val_set.extend([I_cat_ref[j], bool_cat_ref[j]])

            fmu.setReal(vr_set, val_set)
            fmu.doStep(currentCommunicationPoint=t, communicationStepSize=tau_s)
            t += tau_s
            time_lpf.append(t)
            hydrogen.record(fmu, vr, t)

            for p, c in enumerate(traction_idx):
                LoH_lpf[c].append(fmu.getReal([vr["LoH"][c]])[0])
                SoCb_lpf[c].append(fmu.getReal([vr["SoCb"][c]])[0])
                SoCsc_lpf[c].append(fmu.getReal([vr["SoCsc"][c]])[0])

                I_fc_lpf[c].append(fmu.getReal([vr["ifc"][c]])[0])
                I_b_lpf[c].append(fmu.getReal([vr["ib"][c]])[0])
                I_sc_lpf[c].append(fmu.getReal([vr["isc"][c]])[0])

                V_fc_lpf[c].append(fmu.getReal([vr["vfc"][c]])[0])
                V_b_lpf[c].append(fmu.getReal([vr["v_b"][c]])[0])
                V_sc_lpf[c].append(fmu.getReal([vr["vsc"][c]])[0])

                duty_fc_lpf[c].append(fmu.getReal([vr["duty_fc"][c]])[0])
                duty_b_lpf[c].append(fmu.getReal([vr["duty_b"][c]])[0])
                duty_sc_lpf[c].append(fmu.getReal([vr["duty_sc"][c]])[0])

                P_loss_fc_lpf[c].append(
                    fmu.getReal([vr["loss_fc"][c]])[0]
                )
                P_loss_b_lpf[c].append(
                    fmu.getReal([vr["loss_b"][c]])[0]
                )
                P_loss_sc_lpf[c].append(
                    fmu.getReal([vr["loss_sc"][c]])[0]
                )

                current_soc_b[p] = SoCb_lpf[c][-1]
                current_soc_sc[p] = SoCsc_lpf[c][-1]
                current_loh[p] = LoH_lpf[c][-1]
                current_duties["fc"][p] = duty_fc_lpf[c][-1]
                current_duties["b"][p] = duty_b_lpf[c][-1]
                current_duties["sc"][p] = duty_sc_lpf[c][-1]

            I_cat_lpf.append(fmu.getReal([vr["icat_ref"]])[0])
    finally:
        terminate_fmu(fmu)

    time_lpf = np.array(time_lpf)

    for c in traction_idx:
        LoH_lpf[c] = np.array(LoH_lpf[c])
        SoCb_lpf[c] = np.array(SoCb_lpf[c])
        SoCsc_lpf[c] = np.array(SoCsc_lpf[c])

        I_fc_lpf[c] = np.array(I_fc_lpf[c])
        I_b_lpf[c] = np.array(I_b_lpf[c])
        I_sc_lpf[c] = np.array(I_sc_lpf[c])

        V_fc_lpf[c] = np.array(V_fc_lpf[c])
        V_b_lpf[c] = np.array(V_b_lpf[c])
        V_sc_lpf[c] = np.array(V_sc_lpf[c])

        duty_fc_lpf[c] = np.array(duty_fc_lpf[c])
        duty_b_lpf[c] = np.array(duty_b_lpf[c])
        duty_sc_lpf[c] = np.array(duty_sc_lpf[c])

        P_loss_fc_lpf[c] = np.array(P_loss_fc_lpf[c])
        P_loss_b_lpf[c] = np.array(P_loss_b_lpf[c])
        P_loss_sc_lpf[c] = np.array(P_loss_sc_lpf[c])

    I_cat_lpf = np.array(I_cat_lpf)

    signals = [
        I_fc_lpf,
        I_b_lpf,
        I_sc_lpf,
        V_fc_lpf,
        V_b_lpf,
        V_sc_lpf,
        duty_fc_lpf,
        duty_b_lpf,
        duty_sc_lpf,
        P_loss_fc_lpf,
        P_loss_b_lpf,
        P_loss_sc_lpf,
    ]

    for c in traction_idx:
        for sig in signals:
            sig[c] = np.append(sig[c], sig[c][-1])

    I_cat_lpf = np.append(I_cat_lpf, I_cat_lpf[-1])

    return {
        "strategy_name": "LPF-EMS",
        "time_lpf": time_lpf,
        "LoH_lpf": LoH_lpf,
        "SoCb_lpf": SoCb_lpf,
        "SoCsc_lpf": SoCsc_lpf,
        "I_fc_lpf": I_fc_lpf,
        "I_b_lpf": I_b_lpf,
        "I_sc_lpf": I_sc_lpf,
        "V_fc_lpf": V_fc_lpf,
        "V_b_lpf": V_b_lpf,
        "V_sc_lpf": V_sc_lpf,
        "duty_fc_lpf": duty_fc_lpf,
        "duty_b_lpf": duty_b_lpf,
        "duty_sc_lpf": duty_sc_lpf,
        "P_loss_fc_lpf": P_loss_fc_lpf,
        "P_loss_b_lpf": P_loss_b_lpf,
        "P_loss_sc_lpf": P_loss_sc_lpf,
        "converter_efficiency": converter_efficiency,
        "I_cat_lpf": I_cat_lpf,
        "I_fc_ref": I_fc_ref,
        "I_b_ref": I_b_ref,
        "I_sc_ref": I_sc_ref,
        "I_cat_ref": I_cat_ref,
        "fast_lpf_ref": fast_lpf_ref,
        "slow_lpf_ref": slow_lpf_ref,
        "high_frequency_ref": high_frequency_ref,
        "medium_frequency_ref": medium_frequency_ref,
        "fuel_cell": hydrogen.results(),
    }
