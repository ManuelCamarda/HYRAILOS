"""Integration checks for both regenerated Windows FMUs (no IPOPT required)."""

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from fmpy import read_model_description

CASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE))

from data_carriage import load_carriage_data_1, load_carriage_data_2, load_carriage_data_a1, load_carriage_data_a2
from fmu_initialization import initialize_fmu, terminate_fmu
from fuel_cell_model import fuel_cell_efficiency, hydrogen_mass_flow


def validate(filename, car_types, data):
    path = CASE / filename
    md = read_model_description(str(path))
    names = {v.name for v in md.modelVariables}
    assert not any(name.endswith(".c_fc") for name in names)
    traction_idx = [c for c, kind in enumerate(car_types) if kind == "t"]
    fmu, _, vr = initialize_fmu(str(path), 0.0, car_types, data, traction_idx, 0.97)
    step = 0.5
    time = 0.0
    worst_flow_error = 0.0
    worst_eta_error = 0.0
    worst_constant_loh_error = 0.0
    try:
        for power in (0., 1000., 2999., 3000., 4000., 5000., 6000., 7000., 7001., 20000., 50000., 100000.):
            c = traction_idx[0]
            fmu.setReal([vr["ifc_ref"][c]], [power/data[c].V_nom_fc])
            for _ in range(40):  # Settle the existing electrical current-control dynamics.
                fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step)
                time += step
            actual_power, actual_eta, actual_flow = fmu.getReal(
                [vr["pfc"][c], vr["eta_H"][c], vr["h2_flow"][c]]
            )
            expected_flow = hydrogen_mass_flow(actual_power, data[c].Pfc_rated, data[c].LHV)
            expected_eta = fuel_cell_efficiency(actual_power/data[c].Pfc_rated)
            worst_flow_error = max(worst_flow_error, abs(actual_flow-expected_flow))
            worst_eta_error = max(worst_eta_error, abs(actual_eta-expected_eta))
            np.testing.assert_allclose(actual_flow, expected_flow, rtol=1e-10, atol=1e-13)
            np.testing.assert_allclose(actual_eta, expected_eta, rtol=1e-10, atol=1e-12)
            assert actual_flow >= 0.0 and 0.0 < actual_eta <= 1.0
            np.testing.assert_allclose(actual_power, power, rtol=1e-6, atol=0.05)
            loh_before = fmu.getReal([vr["LoH"][c]])[0]
            for _ in range(120):
                fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step)
                time += step
            loh_after, mass = fmu.getReal([vr["LoH"][c], vr["h2_mass"][c]])
            expected_loh = loh_before-expected_flow*60.0/data[c].mH2_max
            error = abs(loh_after-expected_loh)
            worst_constant_loh_error = max(worst_constant_loh_error, error)
            assert error < 2e-6, (filename, power, error)
            np.testing.assert_allclose(mass, data[c].mH2_max*loh_after, atol=1e-10)
        # A tiny negative source command must not replenish the tank.
        fmu.setReal([vr["ifc_ref"][traction_idx[0]]], [-1e-6])
        for _ in range(40):
            fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step)
            time += step
        assert fmu.getReal([vr["h2_flow"][traction_idx[0]]])[0] >= 0.0
        for c in traction_idx:
            np.testing.assert_allclose(
                fmu.getReal([vr["mH2_max"][c], vr["LHV"][c], vr["Pfc_rated"][c]]),
                [15.4, 120e6, 100e3],
            )
            # Converter efficiency is still 97%, distinct from eta_H.
            np.testing.assert_allclose(fmu.getReal([vr["eta_fc"][c]]), [0.97])
    finally:
        terminate_fmu(fmu)
    return {"FMU": filename, "traction_carriages": len(traction_idx),
            "max_flow_error_kg_s": worst_flow_error,
            "max_efficiency_error": worst_eta_error,
            "max_constant_current_LoH_error": worst_constant_loh_error}


def main():
    reports = []
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory(prefix="hyrailos-hydrogen-fmu-") as scratch:
        try:
            os.chdir(scratch)
            reports.append(validate("FourCarriagesFMU.fmu", ["t", "a", "a", "t"],
                [load_carriage_data_1(), load_carriage_data_a1(), load_carriage_data_a2(), load_carriage_data_2()]))
            reports.append(validate("FifteenTractionCarriagesFMU.fmu", ["t"]*15,
                [load_carriage_data_1() for _ in range(15)]))
        finally:
            os.chdir(original_cwd)
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
