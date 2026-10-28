within HYRAILOS.Components.ElectricalComponents;
model AuxiliaryServices // Auxiliary services of the train (HVAC, lighting system, passenger device charging ports, ...)
  // Parameters
  parameter Modelica.Units.SI.Inductance La "inductorAuxiliary inductance value";
  parameter Modelica.Units.SI.Resistance Ra "resistorAuxiliary resistance value";

  // Model instances
  Modelica.Electrical.Analog.Sources.SignalCurrent auxiliaryCurrent annotation(
    Placement(transformation(origin={40,0},      extent={{-20,-20},{20,20}})));
  BasicElectricalComponents.Resistor resistorAuxiliary(R=Ra) annotation (
      Placement(transformation(origin={-66,0}, extent={{-10,-10},{10,10}})));
  BasicElectricalComponents.Inductor inductorAuxiliary(L=La) annotation (
      Placement(transformation(origin={-30,0}, extent={{-10,-10},{10,10}})));

  // Input
  Modelica.Blocks.Interfaces.RealInput Iaref annotation(
    Placement(transformation(origin={-11,38},     extent = {{-105, 15}, {-75, -15}}, rotation = -180), iconTransformation(origin = {58, -49}, extent = {{-98, -14}, {-70, 14}}, rotation = -90)));

  // Electrical interfaces
  Modelica.Electrical.Analog.Interfaces.PositivePin p "Positive electrical pin" annotation(
    Placement(transformation(extent = {{-110, -10}, {-90, 10}}), iconTransformation(extent = {{-110, -10}, {-90, 10}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n "Negative electrical pin" annotation(
    Placement(transformation(origin={0,1},      extent = {{90, -10}, {110, 10}}), iconTransformation(origin = {0, -1}, extent = {{90, -10}, {110, 10}})));

equation
  connect(Iaref, auxiliaryCurrent.i) annotation(
    Line(points={{79,38},{40,38},{40,24}},           color = {0, 0, 127}));
  connect(resistorAuxiliary.p, p) annotation (Line(points={{-76,0},{-100,0}}, color={0,0,255}));
  connect(resistorAuxiliary.n, inductorAuxiliary.p) annotation (Line(points={{-56,0},{-40,0}}, color={0,0,255}));
  connect(auxiliaryCurrent.n, n) annotation (Line(points={{60,0},{100,0},{100,1}}, color={0,0,255}));
  connect(auxiliaryCurrent.p, inductorAuxiliary.n) annotation (Line(points={{20,0},{-20,0}}, color={0,0,255}));
  annotation(
    Icon(graphics = {Text(origin = {1, 77}, extent = {{-145, 13}, {145, -13}}, textString = "%name"), Rectangle(fillColor = {255, 255, 155}, fillPattern = FillPattern.Solid, extent = {{-100, 40}, {100, -40}}),
                                                                                                   Text(origin={60,84},    extent = {{-60, -60}, {60, -80}}, textString = "Ia(t)")}));
end AuxiliaryServices;
