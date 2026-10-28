"""Averaged DC/DC converter relations.

Positive source current denotes discharge toward the DC bus.  Negative source
current denotes charging from the DC bus.  Switching ripple and thermal
dynamics are intentionally outside this system-level model.
"""

import numpy as np


SMOOTH_CURRENT_EPSILON_A = 1.0e-3


def validate_converter_efficiency(efficiency):
    """Return a validated constant converter efficiency."""
    efficiency = float(efficiency)
    if not 0.0 < efficiency <= 1.0:
        raise ValueError("converter_efficiency must be in the interval (0, 1]")
    return efficiency


def conversion_ratio_from_duty(duty):
    """Return the numerically safe source-to-DC voltage conversion ratio."""
    ratio = np.clip(1.0 - np.asarray(duty, dtype=float), 0.05, 1.0)
    return float(ratio) if ratio.ndim == 0 else ratio


def dc_bus_current(source_current, conversion_ratio, efficiency):
    """Convert source current to DC-bus current with bidirectional losses."""
    efficiency = validate_converter_efficiency(efficiency)
    current = np.asarray(source_current, dtype=float)
    ratio = np.asarray(conversion_ratio, dtype=float)
    result = np.where(
        current >= 0.0,
        efficiency * ratio * current,
        ratio * current / efficiency,
    )
    return float(result) if result.ndim == 0 else result


def source_current_from_dc_bus(dc_current, conversion_ratio, efficiency):
    """Convert a DC-bus current request to its source-side current."""
    efficiency = validate_converter_efficiency(efficiency)
    current = np.asarray(dc_current, dtype=float)
    ratio = np.asarray(conversion_ratio, dtype=float)
    result = np.where(
        current >= 0.0,
        current / (efficiency * ratio),
        efficiency * current / ratio,
    )
    return float(result) if result.ndim == 0 else result


def smooth_current_components(source_current, sqrt_function):
    """Return differentiable discharge and charge-current magnitudes."""
    smooth_abs = sqrt_function(
        source_current**2 + SMOOTH_CURRENT_EPSILON_A**2
    )
    discharge = 0.5 * (smooth_abs + source_current)
    charge = 0.5 * (smooth_abs - source_current)
    return discharge, charge


def smooth_source_current_from_dc(
    dc_current,
    conversion_ratio,
    efficiency,
    sqrt_function,
):
    """IPOPT-compatible source current expressed from DC-bus current."""
    efficiency = validate_converter_efficiency(efficiency)
    discharge, charge = smooth_current_components(dc_current, sqrt_function)
    return (discharge / efficiency - efficiency * charge) / conversion_ratio


def smooth_converter_loss_from_dc(
    dc_current,
    dc_voltage,
    efficiency,
    sqrt_function,
):
    """IPOPT-compatible converter loss expressed from DC-bus current."""
    efficiency = validate_converter_efficiency(efficiency)
    discharge, charge = smooth_current_components(dc_current, sqrt_function)
    return dc_voltage * (
        (1.0 / efficiency - 1.0) * discharge
        + (1.0 - efficiency) * charge
    )
