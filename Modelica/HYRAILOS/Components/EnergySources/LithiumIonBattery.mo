within HYRAILOS.Components.EnergySources;
model LithiumIonBattery
  extends BaseEnergySourceInterface(SoC(start = SoC_i, fixed = true, min = 0, max = 1));

  // Parameters
  parameter Types.CapacityAh c_b "Battery capacity [Ah]";
  parameter Real SoC_i(min = 0, max = 1) "Initial state of charge (0..1)";
  parameter Real OCV_table[:, 2] "OCV lookup table: SoC, OCV [V]";
  parameter Modelica.Units.SI.Voltage OCV_Max_b "Open circuit battery voltage when fully charged";
  parameter Modelica.Units.SI.Voltage OCV_Min_b "Open circuit battery voltage when fully discharged";
  parameter Modelica.Units.SI.Resistance R_b "Battery internal resistance";

  // Variables
  Modelica.Units.SI.Voltage OCV_b "Battery OCV dependent on SoC";
  Modelica.Units.SI.Voltage V_b "Battery voltage (p-n)";
  Modelica.Units.SI.Current I_b "Battery current (positive = discharge, negative = charge)";

  // Components
  Modelica.Electrical.Analog.Sources.SignalVoltage ocv_b(v = OCV_b) annotation(
    Placement(transformation(origin = {0, -17}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
  BasicElectricalComponents.Resistor resistor(R=R_b) annotation (Placement(
        transformation(
        origin={0,37},
        extent={{10,10},{-10,-10}},
        rotation=-270)));

  // 1D lookup table for OCV_cell = f(SoC)
  Modelica.Blocks.Tables.CombiTable1Ds ocv_vs_soc(table = OCV_table, columns = {2}, smoothness = Modelica.Blocks.Types.Smoothness.LinearSegments, extrapolation = Modelica.Blocks.Types.Extrapolation.HoldLastPoint, tableOnFile = false) annotation(
    Placement(transformation(origin={-70,70},     extent = {{-10, -10}, {10, 10}})));

equation
  I_b = -p.i "Current positive when discharging";
  V_b = p.v - n.v "Battery voltage";
  OCV_b = ocv_vs_soc.y[1];
  der(SoC) = -I_b/c_b/3600 "SoC decreases when discharging, no discontinuities";

  // Table input and output
  SoC = ocv_vs_soc.u;

  connect(p, resistor.p) annotation(
    Line(points={{0,100},{0,47}},      color = {0, 0, 255}));
  connect(resistor.n, ocv_b.p) annotation(
    Line(points={{0,27},{0,-7}},      color = {0, 0, 255}));
  connect(ocv_b.n, n) annotation(
    Line(points={{0,-27},{0,-100}},      color = {0, 0, 255}));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={                                                                                                                                                                                                        Rectangle(                  fillColor = {0, 170, 0}, fillPattern = FillPattern.VerticalCylinder, extent={{-60,90},
              {60,-90}})}),                                      Diagram(
        coordinateSystem(preserveAspectRatio=false)));

end LithiumIonBattery;
