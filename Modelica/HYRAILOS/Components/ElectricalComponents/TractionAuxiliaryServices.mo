within HYRAILOS.Components.ElectricalComponents;
model TractionAuxiliaryServices // Traction motor and Auxiliary services 
  // Parameters
  parameter Modelica.Units.SI.Inductance La "inductorAuxiliary inductance value";
  parameter Modelica.Units.SI.Resistance Ra "resistorAuxiliary resistance value";

  // Model instances
  Modelica.Electrical.Analog.Sources.SignalCurrent tractionCurrent annotation(
    Placement(transformation(origin={0,50},       extent = {{-10, -10}, {10, 10}})));
  AuxiliaryServices auxiliaryServices(La = La, Ra = Ra) annotation (Placement(transformation(extent={{-28,-22},{26,-76}})));

  // Inputs
  Modelica.Blocks.Interfaces.RealInput Itref annotation(
    Placement(transformation(origin={-50,79},    extent = {{-105, 15}, {-75, -15}}, rotation = -180), iconTransformation(origin = {-59, -50}, extent = {{-98, -14}, {-70, 14}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput Iaref annotation(
    Placement(transformation(origin={1,-66},    extent = {{-105, 15}, {-75, -15}}, rotation = -180), iconTransformation(origin = {58, -49}, extent = {{-98, -14}, {-70, 14}}, rotation = -90)));

  // Electrical interfaces
  Modelica.Electrical.Analog.Interfaces.PositivePin p "Positive electrical pin" annotation(
    Placement(transformation(extent = {{-110, -10}, {-90, 10}}), iconTransformation(extent = {{-110, -10}, {-90, 10}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n "Negative electrical pin" annotation(
    Placement(transformation(origin={-2,1},      extent = {{90, -10}, {110, 10}}), iconTransformation(origin = {0, -1}, extent = {{90, -10}, {110, 10}})));

equation
  connect(tractionCurrent.p, p) annotation(
    Line(points={{-10,50},{-80,50},{-80,0},{-100,0}},   color = {0, 0, 255}));
  connect(Itref, tractionCurrent.i) annotation(
    Line(points={{40,79},{40,78},{0,78},{0,62}},     color = {0, 0, 127}));
  connect(auxiliaryServices.p, p) annotation (Line(points={{-28,-49},{-28,-50},{
          -80,-50},{-80,0},{-100,0}}, color={0,0,255}));
  connect(auxiliaryServices.Iaref, Iaref) annotation (Line(points={{14.66,-58.45},
          {16,-58.45},{16,-66},{91,-66}}, color={0,0,127}));
  connect(tractionCurrent.n, n) annotation (Line(points={{10,50},{80,50},{80,2},
          {98,2},{98,1}}, color={0,0,255}));
  connect(auxiliaryServices.n, n) annotation(
    Line(points = {{26, -48}, {80, -48}, {80, 2}, {98, 2}}, color = {0, 0, 255}));
  annotation(
    Icon(graphics = {Text(origin = {46, 14}, extent = {{-60, -60}, {60, -80}}, textString = "Ita(t)"), Text(origin = {1, 77}, extent = {{-145, 13}, {145, -13}}, textString = "%name"), Rectangle(fillColor = {255, 255, 155}, fillPattern = FillPattern.Solid, extent = {{-100, 40}, {100, -40}})}));
end TractionAuxiliaryServices;
