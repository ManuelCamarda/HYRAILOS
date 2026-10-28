"""
Defines the MPC optimization problem solved at each control step.

The model is built with Pyomo and uses the current train state, load forecasts, catenary availability, 
and user-selected weights to compute the optimal output currents.
"""

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
import numpy as np
from pyomo.opt import SolverStatus, TerminationCondition
from fuel_cell_model import pyomo_hydrogen_mass_flow, validate_fuel_cell_parameters

from converter_model import (
    conversion_ratio_from_duty,
    smooth_converter_loss_from_dc,
    smooth_source_current_from_dc,
    validate_converter_efficiency,
)

# ============================================================
# MPC
# ============================================================
def mpc_function(
    xk, N, tau_s, i,
    I_t_values, I_a_values, I_ta_values,
    wfc, wb, wsc, wcat, data, solver,
    duty_fc, duty_b, duty_sc,
    car_types, bool_cat_values, cat_pos, converter_efficiency
):
    """
    car_types: list like ['t','a','a','t']
    - 't' = traction carriage
    - 'a' = auxiliary carriage

    States and controls exist only for traction carriages:
    xk = [LoH_t1, SoCb_t1, SoCsc_t1, LoH_t2, SoCb_t2, SoCsc_t2, ...]
    duty_fc, duty_b, duty_sc are also only for traction carriages, in the same order.

    Output u_opt ordering with catenary:
    [Ifc_t1, Ib_t1, Isc_t1, Ifc_t2, Ib_t2, Isc_t2, ..., Icat, Il_1, Il_2, ...]
    Output u_opt ordering without catenary:
    [Ifc_t1, Ib_t1, Isc_t1, Ifc_t2, Ib_t2, Isc_t2, ..., Il_1, Il_2, ...]
    """

    converter_efficiency = validate_converter_efficiency(converter_efficiency)
    model = ConcreteModel()

    n_car = len(car_types)
    if n_car == 0:
        raise ValueError("car_types cannot be empty")

    if any(ct not in ('t', 'a') for ct in car_types):
        raise ValueError("car_types must contain only 't' or 'a'")

    if not (0 <= cat_pos <= n_car):
        raise ValueError(f"cat_pos must be between 0 and {n_car}")

    cat_connected = cat_pos != 0
    cat_idx = cat_pos - 1 if cat_connected else None

    traction_idx = [c for c, ct in enumerate(car_types) if ct == 't']
    for c in traction_idx:
        validate_fuel_cell_parameters(data[c])
    n_trac = len(traction_idx)
    trac_map = {c: p for p, c in enumerate(traction_idx)}
    if not (
        len(duty_fc) == len(duty_b) == len(duty_sc) == n_trac
    ):
        raise ValueError("duty arrays must contain one value per traction carriage")
    conversion_fc = conversion_ratio_from_duty(duty_fc)
    conversion_b = conversion_ratio_from_duty(duty_b)
    conversion_sc = conversion_ratio_from_duty(duty_sc)

    model.c = RangeSet(0, n_car - 1)     # all carriages
    model.k = RangeSet(0, N)             # states
    model.k_u = RangeSet(0, N - 1)       # controls
    model.k_du = RangeSet(0, N - 2)      # delta-u for fuel cell

    if n_car > 1:
        model.l = RangeSet(0, n_car - 2)  # inter-carriage links

    if n_trac > 0:
        model.p = RangeSet(0, n_trac - 1)  # traction carriage index

    # -------------------------
    # Variables definition
    # -------------------------
    if n_trac > 0:
        model.LoH = Var(model.p, model.k, bounds=(0.0, 1.0))
        model.SoCb = Var(model.p, model.k, bounds=(0.1, 0.9))
        model.SoCsc = Var(model.p, model.k, bounds=(0.1, 0.9))

        def fuel_cell_current_bounds(m, p, k):
            c = traction_idx[p]
            return (0.0, data[c].Pfc_rated / data[c].V_nom_fc)

        model.Ifc = Var(model.p, model.k_u, bounds=fuel_cell_current_bounds)

        # Parametrizing storage controls on the DC-bus side keeps the train
        # current-balance equations linear. Smooth expressions below recover
        # source currents for losses, state dynamics, and FMU commands.

        def battery_dc_bounds(m, p, k):
            ratio = conversion_b[p]
            source_limit = 650.0 * 10.0
            return (
                -ratio * source_limit / converter_efficiency,
                converter_efficiency * ratio * source_limit,
            )

        def supercapacitor_dc_bounds(m, p, k):
            ratio = conversion_sc[p]
            source_limit = 650.0 * 10.0
            return (
                -ratio * source_limit / converter_efficiency,
                converter_efficiency * ratio * source_limit,
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

    # -------------------------
    # Objective function
    # -------------------------
    def obj_rule(m):
        total = 0.0

        for k in m.k_u:
            for c in range(n_car):
                # Auxiliary services losses exist for all carriages
                total += (data[c].Ra + data[c].Rt) * I_a_values[c, i + k] ** 2

                # Losses for traction carriages only
                if car_types[c] == 't':
                    p = trac_map[c]
                    ratio_fc = conversion_fc[p]
                    I_b_dc = m.IbDC[p, k]
                    I_sc_dc = m.IscDC[p, k]
                    I_fc_dc = converter_efficiency * ratio_fc * m.Ifc[p, k]
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
                        * ratio_fc
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
                        + data[c].Rt * I_t_values[c, i + k] ** 2
                        + wfc * m.deltafc[p, k] ** 2
                        + wb * m.deltas[p, k] ** 2
                        + wsc * m.deltasc[p, k] ** 2
                    )

            if cat_connected:
                total += data[cat_idx].Rcat * m.Icat[k] ** 2 + wcat * m.deltaIcat[k] ** 2

            # inter-carriage line losses
            if n_car > 1:
                for l in m.l:
                    total += data[l].Rl * m.Il[l, k] ** 2

        return total

    model.obj = Objective(rule=obj_rule)

    # -------------------------
    # Initial conditions
    # -------------------------
    if n_trac > 0:
        def init_loh_rule(m, p):
            return m.LoH[p, 0] == xk[3 * p]
        def init_socb_rule(m, p):
            return m.SoCb[p, 0] == xk[3 * p + 1]
        def init_socsc_rule(m, p):
            return m.SoCsc[p, 0] == xk[3 * p + 2]

        model.init_LoH = Constraint(model.p, rule=init_loh_rule)
        model.init_SoCb = Constraint(model.p, rule=init_socb_rule)
        model.init_SoCsc = Constraint(model.p, rule=init_socsc_rule)

    # -------------------------
    # Dynamics
    # -------------------------
    if n_trac > 0:
        def loh_dyn_rule(m, p, k):
            c = traction_idx[p]
            flow = pyomo_hydrogen_mass_flow(
                data[c].V_nom_fc * m.Ifc[p, k], data[c].Pfc_rated, data[c].LHV
            )
            return m.LoH[p, k + 1] == m.LoH[p, k] - flow / data[c].mH2_max * tau_s
        def socb_dyn_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCb[p, k + 1] == m.SoCb[p, k] - m.Ib[p, k] / data[c].ccb / 3600 * tau_s
        def socsc_dyn_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCsc[p, k + 1] == m.SoCsc[p, k] - data[c].V_nom_sc * m.Isc[p, k] / data[c].ccsc / 3600 * tau_s

        model.LoH_dyn = Constraint(model.p, model.k_u, rule=loh_dyn_rule)
        model.SoCb_dyn = Constraint(model.p, model.k_u, rule=socb_dyn_rule)
        model.SoCsc_dyn = Constraint(model.p, model.k_u, rule=socsc_dyn_rule)

    # -------------------------
    # Current balance
    # -------------------------
    def current_balance_rule(m, c, k):
        if car_types[c] == 't':
            p = trac_map[c]
            gen = (
                m.IbDC[p, k]
                + converter_efficiency
                * conversion_fc[p]
                * m.Ifc[p, k]
                + m.IscDC[p, k]
            )
            load = I_ta_values[c, i + k]   # traction + auxiliary
        else:
            gen = 0.0
            load = I_a_values[c, i + k]    # only auxiliary

        incoming_left = 0.0 if c == 0 else m.Il[c - 1, k]
        outgoing_right = 0.0 if c == n_car - 1 else m.Il[c, k]
        cat_inj = m.Icat[k] if cat_connected and c == cat_idx else 0.0 # catenary

        return gen + incoming_left + cat_inj == load + outgoing_right

    model.current_balance = Constraint(model.c, model.k_u, rule=current_balance_rule)

    # -------------------------
    # Soft constraints
    # -------------------------
    if n_trac > 0:
        def loh_thres_rule(m, p, k):
            c = traction_idx[p]
            return m.LoH[p, k] >= data[c].LoHth - m.deltafc[p, k]
        def socb_thres_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCb[p, k] >= data[c].SoCbth - m.deltas[p, k]
        def socsc_thres_rule(m, p, k):
            c = traction_idx[p]
            return m.SoCsc[p, k] >= data[c].SoCscth - m.deltasc[p, k]

        model.LoH_thresh = Constraint(model.p, model.k_u, rule=loh_thres_rule)
        model.SoCb_thresh = Constraint(model.p, model.k_u, rule=socb_thres_rule)
        model.SoCsc_thresh = Constraint(model.p, model.k_u, rule=socsc_thres_rule)

    # -------------------------
    # Other input limits
    # -------------------------
    if cat_connected:
        def icat_limit_rule(m, k):
            return m.Icat[k] <= 650 * 10 * bool_cat_values[i + k]

        def negative_icat_slack_rule(m, k):
            return m.Icat[k] >= -m.deltaIcat[k]

        model.icat_limit = Constraint(model.k_u, rule=icat_limit_rule)
        model.negative_icat_slack = Constraint(model.k_u, rule=negative_icat_slack_rule)

    if n_trac > 0:
        def change_of_ifc_limit_rule(m, p, k):
            return inequality(-20, m.Ifc[p, k + 1] - m.Ifc[p, k], 20)

        model.change_of_ifc = Constraint(model.p, model.k_du, rule=change_of_ifc_limit_rule)

    # -------------------------
    # Solve
    # -------------------------
    solve_results = solver.solve(model, tee=True)
    acceptable_statuses = {SolverStatus.ok, SolverStatus.warning}
    acceptable_terminations = {
        TerminationCondition.optimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
    }
    if (
        solve_results.solver.status not in acceptable_statuses
        or solve_results.solver.termination_condition
        not in acceptable_terminations
    ):
        raise RuntimeError(
            "MPC optimization failed: "
            f"status={solve_results.solver.status}, "
            f"termination={solve_results.solver.termination_condition}"
        )

    # -------------------------
    # Outputs
    # -------------------------
    u_opt_list = []

    for p in range(n_trac):
        u_opt_list.extend([value(model.Ifc[p, 0]), value(model.Ib[p, 0]), value(model.Isc[p, 0])])

    if cat_connected:
        u_opt_list.append(value(model.Icat[0]))

    if n_car > 1:
        u_opt_list.extend([value(model.Il[l, 0]) for l in range(n_car - 1)])

    u_opt = np.array(u_opt_list, dtype=float)

    slack_opt_list = []
    for p in range(n_trac):
        slack_opt_list.extend([value(model.deltafc[p, 0]), value(model.deltas[p, 0]), value(model.deltasc[p, 0])])

    if cat_connected:
        slack_opt_list.append(value(model.deltaIcat[0]))

    slack_opt = np.array(slack_opt_list, dtype=float)

    return u_opt, slack_opt
