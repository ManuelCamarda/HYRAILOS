# Mass-based hydrogen model validation

Validated on 2026-10-05 with the existing default four-carriage scenario:
195-minute route, 0.5 s FMU step, 60 s control interval, MPC horizon of
30 intervals, 30% traction disturbance, seed 7470, and 97% DC/DC efficiency.
Hydrogen capacity is fixed at 15.4 kg per traction carriage; initial LoH is
0.8. The baseline was captured before replacing the hydrogen model.

## Checks completed

- All case-study Python modules compiled; all eight numerical/unit tests passed.
- OpenModelica checked the single-carriage, four-carriage, and fifteen-carriage
  configurations. Both bundled Windows co-simulation FMUs were regenerated.
- Both installed FMUs passed constant-current tests at zero, low load,
  transition boundaries, intermediate loads, and rated power. The largest
  Python/Modelica efficiency difference was below 9e-12, hydrogen-flow
  difference below 6e-20 kg/s, and analytical LoH depletion error below 4e-12.
- Numerical tests confirmed positive efficiency, nonnegative and increasing
  hydrogen flow, matching first and second transition derivatives, zero
  consumption at zero/negative current, and clear rejection of an old FMU.
- Short controller/FMU tests passed with nominal demand and with the configured
  disturbance, covering traction, regenerative braking, and a catenary transition.
- The full route completed with 197 optimal solves: one offline DP solve and
  196 MPC solves, retaining the existing endpoint-update behavior. Maximum
  optimization current-balance residual was 6.45e-7 A; maximum hydrogen-state
  prediction residual was 1.60e-10. Planned nominal fuel-cell power did not
  exceed 100 kW. Measured peaks also stayed below the rating.
- Recorded states and hydrogen signals were finite; storage states remained
  within their admissible range. Remaining mass equals 15.4 times LoH, and
  cumulative consumption equals initial minus remaining mass. Numerical
  integration of recorded mass flow agreed within 9e-7 relative error.
- Disturbance and nominal/plant demand arrays matched the baseline bitwise.
  Existing figures were refreshed and visually inspected without changing
  plotting styles or interactive behavior.

## Full-route results

Hydrogen consumption is the sum over both traction carriages (1 and 4).

| Strategy | Final LoH, carriage 1 | Final LoH, carriage 4 | Total hydrogen consumed (kg) |
| --- | ---: | ---: | ---: |
| MPC | 0.657433 | 0.657614 | 4.388278 |
| DP | 0.651119 | 0.651420 | 4.580906 |
| LPF-EMS | 0.518733 | 0.518733 | 8.663034 |

| Strategy | Final battery SoC, carriage 1 / 4 | Final supercapacitor SoC, carriage 1 / 4 |
| --- | --- | --- |
| MPC | 0.663523 / 0.663697 | 0.428891 / 0.429521 |
| DP | 0.650563 / 0.650855 | 0.512413 / 0.512857 |
| LPF-EMS | 0.612377 / 0.612377 | 0.477672 / 0.477672 |

## Comparison with the previous hydrogen-state model

The largest LoH trajectory change is 0.002383 (0.2383 percentage points).
Final LoH changes are +0.001831/+0.001887 for MPC,
+0.001620/+0.001713 for DP, and -0.000540/-0.000540 for LPF-EMS.

MPC and DP source-current differences are below 5e-8 A RMS, and their battery
and supercapacitor SoC trajectories differ by less than 2e-10. Thus their
electrical behavior is unchanged within numerical tolerance in this case.
LPF-EMS changes slightly because its existing hydrogen-reserve protection
uses the new mass-based LoH: fuel-cell/battery current differences are
0.175/0.323 A RMS, battery SoC changes by at most 0.000513, and the
supercapacitor trajectory is unchanged. No controller ranking was enforced.

The existing reported electrical-loss metric is preserved, including its
legacy normalization and units label; these values are not a new validation
of its physical energy scaling. Hydrogen conversion heat is excluded.

| Strategy | Baseline reported loss metric | New reported loss metric |
| --- | ---: | ---: |
| MPC | 2.136766104200 | 2.136766104200 |
| DP | 2.256595211269 | 2.256595211271 |
| LPF-EMS | 3.830415257090 | 3.828831041301 |

One full-route measurement gave 0.244 s average MPC solve time (baseline
0.228 s) and 1.628 s for the single DP solve (baseline 1.687 s). These are
run-specific solver timings, not a controlled performance benchmark; figure
generation and other simulation work are excluded.

## Scope

This validates implementation consistency, numerical behavior, and preservation
of the existing case-study behavior. It is not hardware validation of the
literature-derived efficiency curve, tank capacity, or nominal-voltage power
approximation. See the repository README for modeling assumptions and exclusions.
