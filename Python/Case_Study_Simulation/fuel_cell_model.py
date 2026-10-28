"""System-level hydrogen flow.

This file calculates hydrogen consumption, based on the efficiency curve.
"""

import numpy as np
from pyomo.environ import Expr_if


LOW_LOAD_EFFICIENCY = 0.2716
TRANSITION_LOW_PLR = 0.03
TRANSITION_HIGH_PLR = 0.07
FLOW_BRIDGE_COEFFICIENTS = (
    0.11045655375552282,
    0.1472754050073638,
    0.0,
    -0.617244147882937,
    0.8757312783643492,
    -0.3403828459708959,
)


def validate_fuel_cell_parameters(data):
    """Reject nonphysical mass, energy, power, and nominal-voltage settings."""
    for name in ("mH2_max", "LHV", "Pfc_rated", "V_nom_fc"):
        parameter = float(getattr(data, name))
        if not np.isfinite(parameter) or parameter <= 0.0:
            raise ValueError(f"Fuel-cell {name} must be finite and positive")
    if not np.isfinite(data.LoH_initial) or not 0.0 <= data.LoH_initial <= 1.0:
        raise ValueError("Fuel-cell LoH_initial must be in [0, 1]")


def polynomial_efficiency(plr):
    """Published high-load polynomial, valid on the modeled rated envelope."""
    return (((((0.9033 * plr - 2.996) * plr + 3.6503) * plr
               - 2.0704) * plr + 0.4623) * plr + 0.3747)


def _bridge_flow(plr):
    u = (plr - TRANSITION_LOW_PLR) / (
        TRANSITION_HIGH_PLR - TRANSITION_LOW_PLR
    )
    result = FLOW_BRIDGE_COEFFICIENTS[-1]
    for coefficient in reversed(FLOW_BRIDGE_COEFFICIENTS[:-1]):
        result = result * u + coefficient
    return result


def normalized_hydrogen_flow(plr):
    """Numerical g(PLR); tiny negative measured currents consume no hydrogen."""
    x = np.maximum(np.asarray(plr, dtype=float), 0.0)
    if not np.isfinite(x).all():
        raise ValueError("Fuel-cell PLR must be finite")
    result = np.empty_like(x)
    low = x <= TRANSITION_LOW_PLR
    high = x >= TRANSITION_HIGH_PLR
    middle = ~(low | high)
    result[low] = x[low] / LOW_LOAD_EFFICIENCY
    result[high] = x[high] / polynomial_efficiency(x[high])
    result[middle] = _bridge_flow(x[middle])
    return float(result) if result.ndim == 0 else result


def fuel_cell_efficiency(plr):
    """Regularized efficiency; eta_H(0)=0.2716 without a 0/0 operation."""
    x = np.maximum(np.asarray(plr, dtype=float), 0.0)
    flow = normalized_hydrogen_flow(x)
    result = np.full_like(x, LOW_LOAD_EFFICIENCY)
    np.divide(x, flow, out=result, where=x > 0.0)
    return float(result) if result.ndim == 0 else result


def hydrogen_mass_flow(power_W, rated_power_W, lhv_J_per_kg):
    """Hydrogen consumption in kg/s from nominal pre-converter source power."""
    if not np.isfinite(rated_power_W) or rated_power_W <= 0.0:
        raise ValueError("rated_power_W must be finite and positive")
    if not np.isfinite(lhv_J_per_kg) or lhv_J_per_kg <= 0.0:
        raise ValueError("lhv_J_per_kg must be finite and positive")
    return (rated_power_W / lhv_J_per_kg) * normalized_hydrogen_flow(
        np.asarray(power_W, dtype=float) / rated_power_W
    )


def pyomo_hydrogen_mass_flow(power_W, rated_power_W, lhv_J_per_kg):
    """
    Power must be bounded by rated power in the optimization.
    """
    x = power_W / rated_power_W
    g = Expr_if(
        IF=x <= TRANSITION_LOW_PLR,
        THEN=x / LOW_LOAD_EFFICIENCY,
        ELSE=Expr_if(
            IF=x >= TRANSITION_HIGH_PLR,
            THEN=x / polynomial_efficiency(x),
            ELSE=_bridge_flow(x),
        ),
    )
    return rated_power_W / lhv_J_per_kg * g


class HydrogenRecorder:
    """Record actual FMU hydrogen variables without altering existing fields."""

    VARIABLE_REFS = {
        "power_W": "pfc",
        "PLR": "plr_fc",
        "eta_H": "eta_H",
        "mass_flow_kg_s": "h2_flow",
        "mass_remaining_kg": "h2_mass",
    }

    def __init__(self, data, traction_idx):
        self.traction_idx = list(traction_idx)
        self.parameters = {
            c: {"mH2_max_kg": data[c].mH2_max,
                "LHV_J_per_kg": data[c].LHV,
                "Pfc_rated_W": data[c].Pfc_rated,
                "E_H_V": data[c].V_nom_fc,
                "LoH_initial": data[c].LoH_initial}
            for c in self.traction_idx
        }
        self.time = []
        self.signals = {
            name: {c: [] for c in self.traction_idx}
            for name in self.VARIABLE_REFS
        }

    def record(self, fmu, vr, time):
        self.time.append(time)
        for c in self.traction_idx:
            values = fmu.getReal([vr[ref][c] for ref in self.VARIABLE_REFS.values()])
            for name, value in zip(self.VARIABLE_REFS, values):
                self.signals[name][c].append(value)

    def results(self):
        signals = {
            name: {c: np.asarray(values, dtype=float) for c, values in series.items()}
            for name, series in self.signals.items()
        }
        signals["mass_consumed_kg"] = {
            c: values[0] - values
            for c, values in signals["mass_remaining_kg"].items()
        }
        return {"time": np.asarray(self.time), "parameters": self.parameters, **signals}
