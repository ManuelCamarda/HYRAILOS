"""
Build and solve the DP energy management problem.
"""

import time as tm

import numpy as np
from pyomo.environ import (
    ConcreteModel,
    Constraint,
    Expression,
    Objective,
    RangeSet,
    Var,
    inequality,
    sqrt,
    value,
)
from pyomo.opt import SolverStatus, TerminationCondition
from fuel_cell_model import pyomo_hydrogen_mass_flow, validate_fuel_cell_parameters

from converter_model import (
    smooth_converter_loss_from_dc,
    smooth_source_current_from_dc,
    validate_converter_efficiency,
)


def dp_function(
    x0,
    horizon,
    tau_s,
    I_t_values,
    I_a_values,
    I_ta_values,
    wfc,
    wb,
    wsc,
    wcat,
    data,
    solver,
    car_types,
    bool_cat_values,
    cat_pos,
    converter_efficiency,
):
    """Solve the complete known route and return all planned trajectories."""

    converter_efficiency = validate_converter_efficiency(converter_efficiency)
    n_car = len(car_types)
    if n_car == 0:
        raise ValueError("car_types cannot be empty")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if any(ct not in ("t", "a") for ct in car_types):
        raise ValueError("car_types must contain only 't' or 'a'")
    if len(data) != n_car:
        raise ValueError("data must have the same length as car_types")
    if not (0 <= cat_pos <= n_car):
        raise ValueError(f"cat_pos must be between 0 and {n_car}")

    for name, values in (
        ("I_t_values", I_t_values),
        ("I_a_values", I_a_values),
        ("I_ta_values", I_ta_values),
    ):
        if values.shape[0] != n_car or values.shape[1] < horizon:
            raise ValueError(
                f"{name} must have shape ({n_car}, at least {horizon})"
            )
    if len(bool_cat_values) < horizon:
        raise ValueError(
            f"bool_cat_values must contain at least {horizon} samples"
        )

    cat_connected = cat_pos != 0
    cat_idx = cat_pos - 1 if cat_connected else None

    traction_idx = [c for c, ct in enumerate(car_types) if ct == "t"]
    for c in traction_idx:
        validate_fuel_cell_parameters(data[c])
    n_trac = len(traction_idx)
    trac_map = {c: p for p, c in enumerate(traction_idx)}

    x0 = np.asarray(x0, dtype=float)
    if x0.shape != (3 * n_trac,):
        raise ValueError(f"x0 must contain exactly {3 * n_trac} values")

    # The data fields Dfc/Db/Dsc are the nominal source-to-DC-bus current
    # conversion ratios, equivalent to (1 - dutyCycle) in the FMU model.
    conversion_fc = np.array([data[c].Dfc for c in traction_idx], dtype=float)
    conversion_b = np.array([data[c].Db for c in traction_idx], dtype=float)
    conversion_sc = np.array([data[c].Dsc for c in traction_idx], dtype=float)

    model = ConcreteModel()
    model.c = RangeSet(0, n_car - 1)
    model.k = RangeSet(0, horizon)
    model.k_u = RangeSet(0, horizon - 1)

    if horizon > 1:
        model.k_du = RangeSet(0, horizon - 2)
    if n_car > 1:
        model.l = RangeSet(0, n_car - 2)
    if n_trac > 0:
        model.p = RangeSet(0, n_trac - 1)

        model.LoH = Var(model.p, model.k, bounds=(0.0, 1.0))
        model.SoCb = Var(model.p, model.k, bounds=(0.1, 0.9))
        model.SoCsc = Var(model.p, model.k, bounds=(0.1, 0.9))

        def fuel_cell_current_bounds(m, p, k):
            c = traction_idx[p]
            return (0.0, data[c].Pfc_rated / data[c].V_nom_fc)

        model.Ifc = Var(model.p, model.k_u, bounds=fuel_cell_current_bounds)

        def battery_dc_bounds(m, p, k):
            source_limit = 650.0 * 10.0
            return (
                -conversion_b[p] * source_limit / converter_efficiency,
                converter_efficiency * conversion_b[p] * source_limit,
            )

        def supercapacitor_dc_bounds(m, p, k):
            source_limit = 650.0 * 10.0
            return (
                -conversion_sc[p] * source_limit / converter_efficiency,
                converter_efficiency * conversion_sc[p] * source_limit,
            )

        model.IbDC = Var(model.p, model.k_u, bounds=battery_dc_bounds)
        model.IscDC = Var(
            model.p, model.k_u, bounds=supercapacitor_dc_bounds
        )

        def battery_source_current_rule(m, p, k):
            return smooth_source_current_from_dc(
                m.IbDC[p, k],
                conversion_b[p],
                converter_efficiency,
                sqrt,
            )

        def supercapacitor_source_current_rule(m, p, k):
            return smooth_source_current_from_dc(
                m.IscDC[p, k],
                conversion_sc[p],
                converter_efficiency,
                sqrt,
            )

        model.Ib = Expression(
            model.p, model.k_u, rule=battery_source_current_rule
        )
        model.Isc = Expression(
            model.p, model.k_u, rule=supercapacitor_source_current_rule
        )

        model.deltafc = Var(model.p, model.k_u, bounds=(0, None))
        model.deltas = Var(model.p, model.k_u, bounds=(0, None))
        model.deltasc = Var(model.p, model.k_u, bounds=(0, None))

    if cat_connected:
        model.Icat = Var(model.k_u, bounds=(-650 * 10, 650 * 10))
        model.deltaIcat = Var(model.k_u, bounds=(0, None))

    if n_car > 1:
        model.Il = Var(model.l, model.k_u, bounds=(-650 * 10, 650 * 10))

    def obj_rule(m):
        total = 0.0
        for k in m.k_u:
            for c in range(n_car):
                total += (data[c].Ra + data[c].Rt) * I_a_values[c, k] ** 2

                if car_types[c] == "t":
                    p = trac_map[c]
                    I_b_dc = m.IbDC[p, k]
                    I_sc_dc = m.IscDC[p, k]
                    I_fc_dc = (
                        converter_efficiency
                        * conversion_fc[p]
                        * m.Ifc[p, k]
                    )
                    P_loss_b = smooth_converter_loss_from_dc(
                        m.IbDC[p, k],
                        data[c].Vcat,
                        converter_efficiency,
                        sqrt,
                    )
                    P_loss_sc = smooth_converter_loss_from_dc(
                        m.IscDC[p, k],
                        data[c].Vcat,
                        converter_efficiency,
                        sqrt,
                    )
                    P_loss_fc = (
                        data[c].Vcat
                        * conversion_fc[p]
                        * (1.0 - converter_efficiency)
                        * m.Ifc[p, k]
                    )
                    total += (
                        data[c].Rb * m.Ib[p, k] ** 2
                        + data[c].RDCb * I_b_dc ** 2
                        + data[c].Rfc * m.Ifc[p, k] ** 2
                        + data[c].RH * m.Ifc[p, k] ** 2
                        + data[c].RDCfc * I_fc_dc ** 2
                        + data[c].Rsc * m.Isc[p, k] ** 2
                        + data[c].RDCsc * I_sc_dc ** 2
                        + P_loss_b
                        + P_loss_fc
                        + P_loss_sc
                        + data[c].Rt * I_t_values[c, k] ** 2
                        + wfc * m.deltafc[p, k] ** 2
                        + wb * m.deltas[p, k] ** 2
                        + wsc * m.deltasc[p, k] ** 2
                    )

            if cat_connected:
                total += (
                    data[cat_idx].Rcat * m.Icat[k] ** 2
                    + wcat * m.deltaIcat[k] ** 2
                )

            if n_car > 1:
                for line in m.l:
                    total += data[line].Rl * m.Il[line, k] ** 2

        return total

    model.obj = Objective(rule=obj_rule)

    if n_trac > 0:

        def init_loh_rule(m, p):
            return m.LoH[p, 0] == x0[3 * p]

        def init_socb_rule(m, p):
            return m.SoCb[p, 0] == x0[3 * p + 1]

        def init_socsc_rule(m, p):
            return m.SoCsc[p, 0] == x0[3 * p + 2]

        model.init_LoH = Constraint(model.p, rule=init_loh_rule)
        model.init_SoCb = Constraint(model.p, rule=init_socb_rule)
        model.init_SoCsc = Constraint(model.p, rule=init_socsc_rule)

        def loh_dyn_rule(m, p, k):
            c = traction_idx[p]
            flow = pyomo_hydrogen_mass_flow(
                data[c].V_nom_fc * m.Ifc[p, k], data[c].Pfc_rated, data[c].LHV
            )
            return (
                m.LoH[p, k + 1]
                == m.LoH[p, k]
                - flow / data[c].mH2_max * tau_s
            )

        def socb_dyn_rule(m, p, k):
            c = traction_idx[p]
            return (
                m.SoCb[p, k + 1]
                == m.SoCb[p, k] - m.Ib[p, k] / data[c].ccb / 3600 * tau_s
            )

        def socsc_dyn_rule(m, p, k):
            c = traction_idx[p]
            return (
                m.SoCsc[p, k + 1]
                == m.SoCsc[p, k]
                - data[c].V_nom_sc
                * m.Isc[p, k]
                / data[c].ccsc
                / 3600
                * tau_s
            )

        model.LoH_dyn = Constraint(model.p, model.k_u, rule=loh_dyn_rule)
        model.SoCb_dyn = Constraint(model.p, model.k_u, rule=socb_dyn_rule)
        model.SoCsc_dyn = Constraint(model.p, model.k_u, rule=socsc_dyn_rule)

    def current_balance_rule(m, c, k):
        if car_types[c] == "t":
            p = trac_map[c]
            generation = (
                m.IbDC[p, k]
                + converter_efficiency
                * conversion_fc[p]
                * m.Ifc[p, k]
                + m.IscDC[p, k]
            )
            load = I_ta_values[c, k]
        else:
            generation = 0.0
            load = I_a_values[c, k]

        incoming_left = 0.0 if c == 0 else m.Il[c - 1, k]
        outgoing_right = 0.0 if c == n_car - 1 else m.Il[c, k]
        catenary_injection = (
            m.Icat[k] if cat_connected and c == cat_idx else 0.0
        )
        return (
            generation + incoming_left + catenary_injection
            == load + outgoing_right
        )

    model.current_balance = Constraint(model.c, model.k_u, rule=current_balance_rule)

    if n_trac > 0:

        def loh_threshold_rule(m, p, k):
            c = traction_idx[p]
            return m.LoH[p, k] >= data[c].LoHth - m.deltafc[p, k]

        def socb_threshold_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCb[p, k] >= data[c].SoCbth - m.deltas[p, k]

        def socsc_threshold_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCsc[p, k] >= data[c].SoCscth - m.deltasc[p, k]

        model.LoH_threshold = Constraint(
            model.p, model.k_u, rule=loh_threshold_rule
        )
        model.SoCb_threshold = Constraint(
            model.p, model.k_u, rule=socb_threshold_rule
        )
        model.SoCsc_threshold = Constraint(
            model.p, model.k_u, rule=socsc_threshold_rule
        )

    if cat_connected:

        def icat_limit_rule(m, k):
            return m.Icat[k] <= 650 * 10 * bool_cat_values[k]

        def negative_icat_slack_rule(m, k):
            return m.Icat[k] >= -m.deltaIcat[k]

        model.icat_limit = Constraint(model.k_u, rule=icat_limit_rule)
        model.negative_icat_slack = Constraint(
            model.k_u, rule=negative_icat_slack_rule
        )

    if n_trac > 0 and horizon > 1:

        def change_of_ifc_limit_rule(m, p, k):
            return inequality(-20, m.Ifc[p, k + 1] - m.Ifc[p, k], 20)

        model.change_of_ifc = Constraint(
            model.p, model.k_du, rule=change_of_ifc_limit_rule
        )

    solve_started = tm.perf_counter()
    solve_results = solver.solve(model, tee=True)
    solve_time = tm.perf_counter() - solve_started

    acceptable_statuses = {SolverStatus.ok, SolverStatus.warning}
    acceptable_terminations = {
        TerminationCondition.optimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
    }
    if (
        solve_results.solver.status not in acceptable_statuses
        or solve_results.solver.termination_condition not in acceptable_terminations
    ):
        raise RuntimeError(
            "DP optimization failed: "
            f"status={solve_results.solver.status}, "
            f"termination={solve_results.solver.termination_condition}"
        )

    x_dp = np.zeros((3 * n_trac, horizon + 1), dtype=float)
    Ifc_DP = np.zeros((n_trac, horizon), dtype=float)
    Ib_DP = np.zeros((n_trac, horizon), dtype=float)
    Isc_DP = np.zeros((n_trac, horizon), dtype=float)
    deltafc_DP = np.zeros((n_trac, horizon), dtype=float)
    deltas_DP = np.zeros((n_trac, horizon), dtype=float)
    deltasc_DP = np.zeros((n_trac, horizon), dtype=float)

    for p in range(n_trac):
        x_dp[3 * p, :] = [value(model.LoH[p, k]) for k in range(horizon + 1)]
        x_dp[3 * p + 1, :] = [
            value(model.SoCb[p, k]) for k in range(horizon + 1)
        ]
        x_dp[3 * p + 2, :] = [
            value(model.SoCsc[p, k]) for k in range(horizon + 1)
        ]
        Ifc_DP[p, :] = [value(model.Ifc[p, k]) for k in range(horizon)]
        Ib_DP[p, :] = [value(model.Ib[p, k]) for k in range(horizon)]
        Isc_DP[p, :] = [value(model.Isc[p, k]) for k in range(horizon)]
        deltafc_DP[p, :] = [
            value(model.deltafc[p, k]) for k in range(horizon)
        ]
        deltas_DP[p, :] = [
            value(model.deltas[p, k]) for k in range(horizon)
        ]
        deltasc_DP[p, :] = [
            value(model.deltasc[p, k]) for k in range(horizon)
        ]

    if cat_connected:
        Icat_DP = np.array(
            [value(model.Icat[k]) for k in range(horizon)], dtype=float
        )
        deltaIcat_DP = np.array(
            [value(model.deltaIcat[k]) for k in range(horizon)], dtype=float
        )
    else:
        Icat_DP = np.zeros(horizon, dtype=float)
        deltaIcat_DP = np.zeros(horizon, dtype=float)

    if n_car > 1:
        Il_DP = np.array(
            [
                [value(model.Il[line, k]) for k in range(horizon)]
                for line in range(n_car - 1)
            ],
            dtype=float,
        )
    else:
        Il_DP = np.zeros((0, horizon), dtype=float)

    dutyfc_DP = np.repeat((1.0 - conversion_fc)[:, None], horizon, axis=1)
    dutyb_DP = np.repeat((1.0 - conversion_b)[:, None], horizon, axis=1)
    dutysc_DP = np.repeat((1.0 - conversion_sc)[:, None], horizon, axis=1)

    return {
        "x_DP": x_dp,
        "Ifc_DP": Ifc_DP,
        "Ib_DP": Ib_DP,
        "Isc_DP": Isc_DP,
        "deltafc_DP": deltafc_DP,
        "deltas_DP": deltas_DP,
        "deltasc_DP": deltasc_DP,
        "deltaIcat_DP": deltaIcat_DP,
        "dutyfc_DP": dutyfc_DP,
        "dutyb_DP": dutyb_DP,
        "dutysc_DP": dutysc_DP,
        "Icat_DP": Icat_DP,
        "Il_DP": Il_DP,
        "DP_objective": float(value(model.obj)),
        "total_DP_solve_time": solve_time,
        "average_DP_solve_time": solve_time,
    }
