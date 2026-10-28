within HYRAILOS.Components.EnergySources;
model HydrogenFuelCell
  extends BaseEnergySourceInterface   (SoC(start = SoC_i, fixed = true, min = 0, max = 1));

  // Parameters
  parameter Modelica.Units.SI.Voltage OCV_h "Fuel cell potential";
  parameter Modelica.Units.SI.Mass mH2_max(min=Modelica.Constants.small)
    "Maximum hydrogen tank mass [kg]";
  parameter Modelica.Units.SI.SpecificEnergy LHV(min=Modelica.Constants.small)
    "Hydrogen lower heating value [J/kg]";
  parameter Modelica.Units.SI.Power Pfc_rated(min=Modelica.Constants.small)
    "Rated nominal pre-converter electrical power [W]";
  parameter Modelica.Units.SI.Resistance R_fc "Fuel cell resistance";
  parameter Modelica.Units.SI.Resistance R_H "Fuel cell activation resistance";
  parameter Modelica.Units.SI.Capacitance C_H "Fuel cell activation capacitance";
  parameter Real SoC_i(min = 0, max = 1) "Initial normalized hydrogen mass (LoH)";

  // Variables
  Modelica.Units.SI.Current I_fc "Fuel cell current (positive = discharge)";
  Modelica.Units.SI.Voltage V_fc "Fuel cell voltage (p-n)";
  Modelica.Units.SI.Power P_fc(min=0) "Nominal pre-converter power OCV_h*I_fc";
  Real PLR(min=0) "Part-load ratio P_fc/Pfc_rated";
  Real eta_H(min=0, max=1) "Hydrogen-to-nominal-electrical-power efficiency";
  Modelica.Units.SI.MassFlowRate mH2_flow(min=0) "Hydrogen consumption [kg/s]";
  Modelica.Units.SI.Mass mH2_remaining "Remaining hydrogen mass [kg]";
protected
  Real normalizedFlow;
  Real u "Normalized position in the 3%-7% load transition";
public

  // Components
  BasicElectricalComponents.Resistor Rfc(R=R_fc) annotation (Placement(
        transformation(
        origin={0,50},
        extent={{-10,-10},{10,10}},
        rotation=-90)));
  BasicElectricalComponents.Resistor RH(R=R_H) annotation (Placement(
        transformation(
        origin={28,0},
        extent={{-10,-10},{10,10}},
        rotation=-90)));
  Modelica.Electrical.Analog.Sources.ConstantVoltage ocv_h(V = OCV_h) annotation(
    Placement(transformation(origin={0,-50},      extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  BasicElectricalComponents.Capacitor CH(C=C_H) annotation (Placement(
        transformation(
        origin={-29,0},
        extent={{-10,-10},{10,10}},
        rotation=-90)));

equation
  I_fc = -p.i "Current positive when discharging";
  V_fc = p.v - n.v;
  P_fc = noEvent(max(OCV_h*I_fc, 0)) "No hydrogen replenishment from current noise";
  PLR = P_fc/Pfc_rated;
  eta_H = noEvent(if PLR > 0 then PLR/normalizedFlow else 0.2716);
  mH2_flow = Pfc_rated/LHV*normalizedFlow;
  mH2_remaining = mH2_max*SoC;
  der(SoC) = -mH2_flow/mH2_max "LoH is normalized remaining hydrogen mass";
  assert(mH2_max > 0 and LHV > 0 and Pfc_rated > 0 and OCV_h > 0,
    "Hydrogen mass capacity, LHV, rated power, and nominal voltage must be positive");
  assert(P_fc <= 1.001*Pfc_rated, "Fuel cell exceeds its rated nominal power",
    AssertionLevel.warning);

  connect(RH.p, Rfc.n) annotation(
    Line(points={{28,10},{28,26},{0,26},{0,40}},                color = {0, 0, 255}));
  connect(RH.n, ocv_h.p) annotation(
    Line(points={{28,-10},{28,-34},{0,-34},{0,-40}},            color = {0, 0, 255}));
  connect(p, Rfc.p) annotation(
    Line(points={{0,100},{0,60}},         color = {0, 0, 255}));
  connect(n, ocv_h.n) annotation(
    Line(points={{0,-100},{0,-60}},         color = {0, 0, 255}));
  connect(Rfc.n, CH.p) annotation(
    Line(points={{0,40},{0,26},{-29,26},{-29,10}},              color = {0, 0, 255}));
  connect(CH.n, ocv_h.p) annotation(
    Line(points={{-29,-10},{-30,-10},{-30,-34},{0,-34},{0,-40}},color = {0, 0, 255}));

algorithm
  // Evaluate the curve stepwise to preserve the arithmetic
  u := 0.04;
  u := (PLR - 0.03)/u;
  if noEvent(PLR <= 0.03) then
    normalizedFlow := PLR/0.2716;
  elseif noEvent(PLR >= 0.07) then
    normalizedFlow := (((((0.9033*PLR - 2.996)*PLR + 3.6503)*PLR
      - 2.0704)*PLR + 0.4623)*PLR + 0.3747);
    normalizedFlow := PLR/normalizedFlow;
  else
    normalizedFlow := -0.3403828459708959*u + 0.8757312783643492;
    normalizedFlow := normalizedFlow*u - 0.617244147882937;
    normalizedFlow := normalizedFlow*u;
    normalizedFlow := normalizedFlow*u + 0.1472754050073638;
    normalizedFlow := normalizedFlow*u + 0.11045655375552282;
  end if;

  annotation (Icon(graphics={
                     Rectangle(                  fillColor = {0, 255, 255}, fillPattern = FillPattern.VerticalCylinder, extent={{-90,90},
              {90,-90}})}));
end HydrogenFuelCell;
