"""
Initializes and terminates the FMU used as the train plant model.

It maps Modelica variable names to FMU value references, sets the initial parameters from the carriage data, 
and provides a termination function for repeated simulations.
"""

from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave

from converter_model import validate_converter_efficiency
from fuel_cell_model import validate_fuel_cell_parameters

def initialize_fmu(
    fmu_path,
    t_start,
    car_types,
    data,
    traction_idx,
    converter_efficiency,
):
    converter_efficiency = validate_converter_efficiency(converter_efficiency)
    n_car = len(car_types)

    md = read_model_description(fmu_path)
    # Check the binary interface before extracting or instantiating an old FMU.
    names = {v.name for v in md.modelVariables}
    traction_count = 0
    for c in traction_idx:
        validate_fuel_cell_parameters(data[c])
        suffix = "" if traction_count == 0 else str(traction_count)
        prefix = f"caseStudyTractionCarriage{suffix}.hydrogenFuelCellUnit."
        required = [prefix + name for name in ("mH2_max", "LHV", "Pfc_rated")]
        required += [prefix + "energySource." + name for name in
                     ("P_fc", "PLR", "eta_H", "mH2_flow", "mH2_remaining")]
        missing = [name for name in required if name not in names]
        if missing:
            raise ValueError(
                "The FMU does not expose the mass-based hydrogen model. "
                "Regenerate the FMU from the updated HYRAILOS Modelica package "
                f"and replace {fmu_path}. Missing variables: {', '.join(missing)}"
            )
        traction_count += 1
    unzipdir = extract(fmu_path)
    fmu = FMU2Slave(
        guid=md.guid,
        unzipDirectory=unzipdir,
        modelIdentifier=md.coSimulation.modelIdentifier,
        instanceName='instance1'
    )

    fmu.instantiate()
    fmu.setupExperiment(startTime=t_start)
    fmu.enterInitializationMode()

    vr = {v.name: v.valueReference for v in md.modelVariables}

    vr_refs = {
        "icat_ref": vr["Icatref"],
        "bool_cat": vr["booleancatenary"],

        "ifc_ref": [None] * n_car,
        "ib_ref": [None] * n_car,
        "isc_ref": [None] * n_car,
        "it_ref": [None] * n_car,
        "ia_ref": [None] * n_car,

        "duty_fc": [None] * n_car,
        "duty_b": [None] * n_car,
        "duty_sc": [None] * n_car,

        "eta_fc": [None] * n_car,
        "eta_b": [None] * n_car,
        "eta_sc": [None] * n_car,

        "loss_fc": [None] * n_car,
        "loss_b": [None] * n_car,
        "loss_sc": [None] * n_car,

        "LoH": [None] * n_car,
        "SoCb": [None] * n_car,
        "SoCsc": [None] * n_car,

        "ifc": [None] * n_car,
        "ib": [None] * n_car,
        "isc": [None] * n_car,

        "vfc": [None] * n_car,
        "v_b": [None] * n_car,
        "vsc": [None] * n_car,

        "c_b": [None] * n_car,
        "SoCb_initial": [None] * n_car,
        "R_b": [None] * n_car,

        "mH2_max": [None] * n_car,
        "LHV": [None] * n_car,
        "Pfc_rated": [None] * n_car,
        "pfc": [None] * n_car,
        "plr_fc": [None] * n_car,
        "eta_H": [None] * n_car,
        "h2_flow": [None] * n_car,
        "h2_mass": [None] * n_car,
        "LoH_initial": [None] * n_car,
        "vfc_nom": [None] * n_car,
        "Rfc": [None] * n_car,
        "RH": [None] * n_car,
        "CH": [None] * n_car,

        "csc": [None] * n_car,
        "SoCsc_initial": [None] * n_car,
        "vsc_nom": [None] * n_car,
        "Rsc": [None] * n_car,
        "Csc": [None] * n_car,

        "Rt": [None] * n_car,
        "Lt": [None] * n_car,

        "RDCfc": [None] * n_car,
        "LDCfc": [None] * n_car,

        "RDCb": [None] * n_car,
        "LDCb": [None] * n_car,

        "RDCsc": [None] * n_car,
        "LDCsc": [None] * n_car,

        "Ra": [None] * n_car,
        "La": [None] * n_car,
    }

    t_count = 0
    a_count = 0

    for c in range(n_car):

        if car_types[c] == "t":
            s_t = "" if t_count == 0 else str(t_count)

            vr_refs["it_ref"][c] = vr[f"Itref{s_t}"]
            vr_refs["ia_ref"][c] = vr[f"Iaref{s_t}"]
            vr_refs["ifc_ref"][c] = vr[f"Ifcref{s_t}"]
            vr_refs["ib_ref"][c] = vr[f"Ibref{s_t}"]
            vr_refs["isc_ref"][c] = vr[f"Iscref{s_t}"]

            vr_refs["duty_fc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.dCDCConverter.dutyCycle"]
            vr_refs["duty_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.dCDCConverter.dutyCycle"]
            vr_refs["duty_sc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.dCDCConverter.dutyCycle"]

            vr_refs["eta_fc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.dCDCConverter.efficiency"]
            vr_refs["eta_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.dCDCConverter.efficiency"]
            vr_refs["eta_sc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.dCDCConverter.efficiency"]

            vr_refs["loss_fc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.dCDCConverter.lossPower"]
            vr_refs["loss_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.dCDCConverter.lossPower"]
            vr_refs["loss_sc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.dCDCConverter.lossPower"]

            vr_refs["LoH"][c] = vr[f"LoH{s_t}"]
            vr_refs["SoCb"][c] = vr[f"SoCb{s_t}"]
            vr_refs["SoCsc"][c] = vr[f"SoCsc{s_t}"]

            vr_refs["ifc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.energySource.I_fc"]
            vr_refs["ib"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.energySource.I_b"]
            vr_refs["isc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.energySource.I_sc"]

            vr_refs["vfc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.energySource.V_fc"]
            vr_refs["v_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.energySource.V_b"]
            vr_refs["vsc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.energySource.V_sc"]

            vr_refs["c_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.c_b"]
            vr_refs["SoCb_initial"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.SoC_i"]
            vr_refs["R_b"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.R_b"]

            prefix = f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit."
            for parameter in ("mH2_max", "LHV", "Pfc_rated"):
                vr_refs[parameter][c] = vr[prefix + parameter]
            for ref, variable in (("pfc", "P_fc"), ("plr_fc", "PLR"),
                                  ("eta_H", "eta_H"), ("h2_flow", "mH2_flow"),
                                  ("h2_mass", "mH2_remaining")):
                vr_refs[ref][c] = vr[prefix + "energySource." + variable]
            vr_refs["LoH_initial"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.SoC_i"]
            vr_refs["vfc_nom"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.OCV_h"]
            vr_refs["Rfc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.R_fc"]
            vr_refs["RH"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.R_H"]
            vr_refs["CH"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.C_H"]

            vr_refs["csc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.c_sc"]
            vr_refs["SoCsc_initial"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.SoC_i"]
            vr_refs["vsc_nom"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.V_init_sc"]
            vr_refs["Rsc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.R_sc"]
            vr_refs["Csc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.C_sc"]

            vr_refs["Rt"][c] = vr[f"caseStudyTractionCarriage{s_t}.Rt.R"]
            vr_refs["Lt"][c] = vr[f"caseStudyTractionCarriage{s_t}.Lt.L"]

            vr_refs["RDCfc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.resistorDC.R"]
            vr_refs["LDCfc"][c] = vr[f"caseStudyTractionCarriage{s_t}.hydrogenFuelCellUnit.inductorDC.L"]

            vr_refs["RDCb"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.resistorDC.R"]
            vr_refs["LDCb"][c] = vr[f"caseStudyTractionCarriage{s_t}.lithiumIonBatteryUnit.inductorDC.L"]

            vr_refs["RDCsc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.resistorDC.R"]
            vr_refs["LDCsc"][c] = vr[f"caseStudyTractionCarriage{s_t}.supercapacitorUnit.inductorDC.L"]

            vr_refs["Ra"][c] = vr[f"caseStudyTractionCarriage{s_t}.tractionAuxiliary.Ra"]
            vr_refs["La"][c] = vr[f"caseStudyTractionCarriage{s_t}.tractionAuxiliary.La"]

            t_count += 1

        else:
            s_a = "" if a_count == 0 else str(a_count)
            vr_refs["ia_ref"][c] = vr[f"Iaref_a{s_a}"]
            a_count += 1

    # Set initial FMU parameters
    vr_set = []
    val_set = []

    for c in traction_idx:
        vr_set.extend([
            vr_refs["mH2_max"][c],
            vr_refs["LHV"][c],
            vr_refs["Pfc_rated"][c],
            vr_refs["c_b"][c],
            vr_refs["csc"][c],
            vr_refs["LoH_initial"][c],
            vr_refs["SoCb_initial"][c],
            vr_refs["SoCsc_initial"][c],
            vr_refs["vfc_nom"][c],
            vr_refs["vsc_nom"][c],
            vr_refs["R_b"][c],
            vr_refs["Rsc"][c],
            vr_refs["Rfc"][c],
            vr_refs["RH"][c],
            vr_refs["CH"][c],
            vr_refs["Csc"][c],
            vr_refs["Rt"][c],
            vr_refs["Lt"][c],
            vr_refs["RDCfc"][c],
            vr_refs["LDCfc"][c],
            vr_refs["RDCb"][c],
            vr_refs["LDCb"][c],
            vr_refs["RDCsc"][c],
            vr_refs["LDCsc"][c],
            vr_refs["Ra"][c],
            vr_refs["La"][c],
            vr_refs["eta_fc"][c],
            vr_refs["eta_b"][c],
            vr_refs["eta_sc"][c],
        ])

        val_set.extend([
            data[c].mH2_max,
            data[c].LHV,
            data[c].Pfc_rated,
            data[c].ccb,
            data[c].ccsc,
            data[c].LoH_initial,
            data[c].SoCb_initial,
            data[c].SoCsc_initial,
            data[c].V_nom_fc,
            data[c].V_nom_sc,
            data[c].Rb,
            data[c].Rsc,
            data[c].Rfc,
            data[c].RH,
            data[c].CH,
            data[c].Csc,
            data[c].Rt,
            data[c].Lt,
            data[c].RDCfc,
            data[c].LDCfc,
            data[c].RDCb,
            data[c].LDCb,
            data[c].RDCsc,
            data[c].LDCsc,
            data[c].Ra,
            data[c].La,
            converter_efficiency,
            converter_efficiency,
            converter_efficiency,
        ])

    if len(vr_set) > 0:
        fmu.setReal(vr_set, val_set)

    fmu.exitInitializationMode()

    return fmu, md, vr_refs


def terminate_fmu(fmu):
    fmu.terminate()
    fmu.freeInstance()
