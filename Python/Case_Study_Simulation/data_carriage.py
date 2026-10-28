"""
Defines the numerical data used for traction and auxiliary carriages.

Users can edit this file to change the train electrical parameters (resistances, inductances, capacitances, 
voltages), energy capacities, threshold limits, initial states.
"""

from dataclasses import dataclass

@dataclass
class TractionCarriageData: # traction carriage data: contains all the data regarding a traction carriage
    Rb: float
    RDCb: float
    Rfc: float
    RH: float
    RDCfc: float
    Rsc: float
    RDCsc: float
    Rt: float
    Ra: float
    Rl: float
    Rcat: float
    LDCb: float
    LDCfc : float
    LDCsc: float
    Lt: float
    La: float
    Ll: float
    CH: float
    Csc: float
    Eb: float
    Vcat: float
    V_nom_fc: float
    V_nom_sc: float
    Dfc: float
    Db: float
    Dsc: float
    SoCbth: float
    LoHth: float
    SoCscth: float
    ccb: float
    mH2_max: float 
    LHV: float  
    Pfc_rated: float  
    ccsc: float
    SoCb_initial: float
    LoH_initial: float
    SoCsc_initial: float

@dataclass
class AuxiliaryCarriageData: # auxiliary carriage data: contains all the data regarding an auxiliary only carriage
    Rt: float
    Ra: float
    Rl: float
    Rcat: float
    Lt: float
    La: float
    Ll: float
    Vcat: float

V_DC = 1500
Vbattery = 420
Vbattery_nom = 398
Vhydrogen_nom = 750
Vsupercapacitor_nom = 360

# Traction carriages
def load_carriage_data_1() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=30e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_2() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=30e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_3() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_4() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_5() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_6() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_7() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_8() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_9() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_10() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_11() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_12() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_13() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_14() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_15() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_16() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_17() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_18() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_19() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)

def load_carriage_data_20() -> TractionCarriageData:
    return TractionCarriageData(Rb=1e-3, RDCb=1e-3, Rfc=2e-3, RH=3e-3, RDCfc=1e-3, Rsc=1e-3, RDCsc=1e-3,
                        Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                        LDCb=1.8e-3, LDCfc=1.8e-3, LDCsc=1.8e-3, Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                        CH=1000, Csc=1200,
                        Eb=Vbattery, Vcat=V_DC, V_nom_fc=Vhydrogen_nom, V_nom_sc=Vsupercapacitor_nom,
                        Dfc=Vhydrogen_nom/V_DC, Db=Vbattery_nom/V_DC, Dsc=Vsupercapacitor_nom/V_DC,
                        SoCbth=0.6, LoHth=0.6, SoCscth=0.6, ccb=200e3/Vbattery,
                        mH2_max=15.4, LHV=120e6, Pfc_rated=100e3, ccsc=20e3,
                        SoCb_initial=0.8, LoH_initial=0.8, SoCsc_initial=0.8)


# Auxiliary carriages
def load_carriage_data_a1() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a2() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a3() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a4() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a5() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a6() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a7() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a8() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a9() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)

def load_carriage_data_a10() -> AuxiliaryCarriageData:
    return AuxiliaryCarriageData(Rt=1e-3, Ra=1e-3, Rl=4e-3, Rcat=4e-3,
                                Lt=1.8e-3, La=1.8e-3, Ll=20e-6,
                                Vcat=V_DC)
