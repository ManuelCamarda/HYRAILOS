# In-class hydrogen efficiency refactor

Verified on 2026-10-19 with OpenModelica 1.25.4 and the existing Windows FMU/IPOPT environment.

## Changes

- Removed the standalone `NormalizedHydrogenFlow` Modelica function and its
  `package.order` entry. The complete efficiency/normalized-flow calculation
  is now inside `HydrogenFuelCell`, with no nested or external helper class.
- Kept the published efficiency coefficients, 3%-7% regularization, zero-load
  handling, electrical circuit, and hydrogen-state equations unchanged.
  The curve is evaluated stepwise to preserve the original floating-point
  division and multiplication order when compiling the model equations.
- Removed the duplicate numerical defaults for `mH2_max`, `LHV`, and
  `Pfc_rated` from `HydrogenFuelCell` and `HydrogenFuelCellDCcontrol`.
  Their existing values remain in the case-study `ParametrizedComponents`.
- Regenerated both bundled Windows FMUs. Controller code, user settings,
  parameter values, and existing figures were not changed.

## Before/after comparison

The baseline was rebuilt from the unchanged pre-refactor Modelica source.
It was first checked against the original bundled FMUs: both component
responses and the complete default route reproduced the same numerical
results exactly. The final refactored FMUs were then checked against this
baseline.

- Both FMUs were exercised at zero, low, transition-boundary, intermediate,
  and rated fuel-cell powers. The tests recorded 20 quantities for every
  traction carriage, including electrical states, currents, voltages,
  duty cycles, converter losses, efficiency, and hydrogen flow/mass.
- The complete 195-minute four-carriage case was run with MPC, DP, and
  LPF-EMS: 30% traction disturbance, seed 7470, 97% DC/DC efficiency,
  0.5 s FMU step, 60 s MPC interval, and a 30-step prediction horizon.
- All 197 optimization solves terminated optimally: one DP solve and
  196 MPC solves, retaining the existing endpoint-update behavior.
- All 4,348,727 checked numerical values were bit-for-bit identical,
  including the complete recorded trajectories, nominal/disturbed inputs,
  current references, hydrogen consumption, and reported loss metrics.
  Wall-clock execution times were excluded because they vary between runs.
- The FMU inputs and parameter definitions/defaults remained unchanged:
  306 entries in the four-carriage FMU and 2,048 in the fifteen-carriage FMU.

## Additional checks

- All eight existing Python numerical/unit tests passed.
- The installed four- and fifteen-carriage FMUs passed
  `python tests/validate_fuel_cell_fmu.py`, including analytical
  constant-current depletion, mass conservation, and negative-current
  handling. Maximum analytical LoH error was below 3.5e-12.
- OpenModelica checks passed for the single-, four-, and fifteen-carriage
  configurations: 372, 976, and 6,087 scalar equations/variables respectively.
  The flattened count increases by one algebraic intermediate per fuel cell;
  no additional dynamic state is introduced. The MPC is unchanged at
  23 scalar variables per prediction stage, or 696 over the default horizon.

These are implementation-regression checks, not experimental validation
of the underlying fuel-cell model. Detailed baseline copies, build logs,
and numerical comparisons are retained outside the repository in
`tmp/hydrogen-inline-refactor` under the parent workspace.
