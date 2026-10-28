within HYRAILOS.CaseStudyTrain.ParametrizedComponents;
model CaseStudySingleCarriage // Train (consisting of just 1 carriage) with values

  parameter Modelica.Units.SI.Voltage OCV_Max_b = 420 "Open circuit battery voltage when fully charged";
  parameter Modelica.Units.SI.Voltage OCV_Min_b = 250 "Open circuit battery voltage when fully discharged";
  
  extends Components.Carriages.SingleCarriage(lithiumIonBatteryUnit(
      Ldc=1.8e-3,
      Rdc=1e-3,
      OCV_Max_b=420,
      OCV_Min_b=250,
      c_b=480,
      R_b=1e-3,
      SoC_i=0.8,
      OCV_table=[0.00, OCV_Min_b; 0.05, 0.74*OCV_Max_b; 0.10, 0.79*OCV_Max_b; 0.20, 0.85*OCV_Max_b; 0.30, 0.88*OCV_Max_b; 0.40, 0.89*OCV_Max_b; 0.50, 0.90*OCV_Max_b; 0.60, 0.92*OCV_Max_b; 0.70, 0.93*OCV_Max_b; 0.80, 0.95*OCV_Max_b; 0.90, 0.97*OCV_Max_b; 1.00, OCV_Max_b]),
    supercapacitorUnit(
      Ldc=1.8e-3,
      Rdc=1e-3,
      V_Max_sc=400,
      V_min_sc=200,
      C_sc=1200,
      R_sc=1e-3,
      c_sc=30e3,
      V_init_sc=360,
      SoC_i=0.8),
    hydrogenFuelCellUnit(
      Ldc=1.8e-3,
      Rdc=1e-3,
      OCV_h=750,
      mH2_max=15.4,
      LHV=120e6,
      Pfc_rated=100e3,
      R_fc=2e-3,
      R_H=3e-3,
      C_H=1000,
      SoC_i=0.8),
    Rt(R=1e-3),
    Lt(L=1.8e-3),
    tractionAuxiliary(La=1.8e-3, Ra=1e-3));
end CaseStudySingleCarriage;
