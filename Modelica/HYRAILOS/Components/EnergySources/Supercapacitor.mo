within HYRAILOS.Components.EnergySources;
model Supercapacitor
  extends BaseEnergySourceInterface   (SoC(start = SoC_i, fixed = true, min = 0, max = 1));

  // Parameters
  parameter Modelica.Units.SI.Voltage V_Max_sc "Supercapacitor voltage when fully charged";
  parameter Modelica.Units.SI.Voltage V_min_sc "Supercapacitor voltage when fully discharged";
  parameter Modelica.Units.SI.Capacitance C_sc "Supercapacitor capacitance";
  parameter Modelica.Units.SI.Resistance R_sc "Supercapacitor internal resistance";
  parameter Types.CapacityWh c_sc "Supercapacitor capacity [Wh]";
  parameter Modelica.Units.SI.Voltage V_init_sc "Supercapacitor starting voltage";
  parameter Modelica.Units.SI.PerUnit SoC_i "Supercapacitor starting SoC";

  // Variables
  Modelica.Units.SI.Voltage V_Csc "Capacitor voltage";
  Modelica.Units.SI.Voltage V_sc "Supercapacitor voltage (p-n)";
  Modelica.Units.SI.Current I_sc "Supercapacitor current (positive = discharge, negative = charge)";

  BasicElectricalComponents.Resistor resistor(R=R_sc) annotation (Placement(
        transformation(
        origin={0,40},
        extent={{10,10},{-10,-10}},
        rotation=-270)));
  BasicElectricalComponents.Capacitor capacitor(C=C_sc, v(start=V_init_sc,
        fixed=true)) annotation (Placement(transformation(
        origin={0,-10},
        extent={{-10,-10},{10,10}},
        rotation=-90)));

equation
  V_Csc = capacitor.v;
  V_sc = p.v - n.v;
  I_sc = -p.i "Current positive when discharging";
  der(SoC) = -V_Csc*I_sc/c_sc/3600 "SoC decreases when discharging, no discontinuities";
  connect(p, resistor.p) annotation(
    Line(points = {{0, 100}, {0, 50}}, color = {0, 0, 255}));
  connect(resistor.n, capacitor.p) annotation(
    Line(points = {{0, 30}, {0, 0}}, color = {0, 0, 255}));
  connect(capacitor.n, n) annotation(
    Line(points = {{0, -20}, {0, -100}}, color = {0, 0, 255}));

  annotation (Icon(graphics={                                                                                                                                                                                                        Rectangle(                  fillColor = {0, 85, 255}, fillPattern = FillPattern.VerticalCylinder, extent={{-80,60},
              {80,-60}}),                                                                                                                                                                                                        Line(origin={0,72},    points = {{0, 18}, {0, -18}}, color = {0, 85, 255}, thickness = 4),
                                                                                                                                                                                                        Line(origin={0,-72},   points = {{0, 18}, {0, -18}}, color = {0, 85, 255}, thickness = 4)}));
end Supercapacitor;
