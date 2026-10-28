within HYRAILOS.Components.ElectricalComponents;
model Catenary 
// Overhead catenary line
  parameter Modelica.Units.SI.Resistance Rcatenary;

  Modelica.Electrical.Analog.Interfaces.PositivePin p "Positive electrical pin" annotation(
    Placement(transformation(origin={-27,-1},    extent = {{-110, -10}, {-90, 10}}), iconTransformation(origin={31,-29},   extent = {{-110, -10}, {-90, 10}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n "Negative electrical pin" annotation(
    Placement(transformation(origin={38,1},      extent = {{90, -10}, {110, 10}}), iconTransformation(origin={-30,-29}, extent = {{90, -10}, {110, 10}})));
  Modelica.Blocks.Interfaces.RealInput Icatref annotation(
    Placement(transformation(origin={34,33},     extent = {{105, 15}, {75, -15}}, rotation = 180), iconTransformation(origin={-69,-30},    extent = {{-98, -14}, {-70, 14}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput booleancatenary annotation(
    Placement(transformation(origin={55,-13},   extent = {{105, 15}, {75, -15}}, rotation = 90), iconTransformation(origin={70,-30},    extent = {{-98, -14}, {-70, 14}}, rotation = -90)));
  Modelica.Blocks.Logical.GreaterThreshold greaterThreshold(threshold = 0.5) annotation(
    Placement(transformation(origin={55,35},    extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  BasicElectricalComponents.Resistor Rcat(R=Rcatenary) annotation (Placement(
        transformation(
        origin={-79,0},
        extent={{10,-10},{-10,10}},
        rotation=-0)));
  Modelica.Electrical.Analog.Sources.SignalCurrent catenaryCurrent annotation(
    Placement(transformation(origin={-19,0},     extent = {{-10, -10}, {10, 10}}, rotation = -0)));
  Modelica.Electrical.Analog.Ideal.IdealClosingSwitch closedswitch annotation(
    Placement(transformation(origin={56,0},    extent = {{-10, -10}, {10, 10}})));
equation
  connect(booleancatenary, greaterThreshold.u) annotation(
    Line(points={{55,77},{55,47}},       color = {0, 0, 127}));
  connect(Rcat.n, p) annotation(
    Line(points={{-89,0},{-108,0},{-108,-1},{-127,-1}},
                                            color = {0, 0, 255}));
  connect(catenaryCurrent.p, Rcat.p) annotation(
    Line(points={{-29,0},{-69,0}},         color = {0, 0, 255}));
  connect(Icatref, catenaryCurrent.i) annotation(
    Line(points={{-56,33},{-19,33},{-19,12}},         color = {0, 0, 127}));
  connect(greaterThreshold.y, closedswitch.control) annotation(
    Line(points={{55,24},{55,18},{56,18},{56,12}},
                                      color = {255, 0, 255}));
  connect(closedswitch.p, catenaryCurrent.n) annotation(
    Line(points={{46,0},{-9,0}},          color = {0, 0, 255}));
  connect(closedswitch.n, n) annotation(
    Line(points={{66,0},{101,0},{101,1},{138,1}},           color = {0, 0, 255}));
  annotation(
    Diagram(coordinateSystem(extent={{-140,-60},{140,80}})),
    Icon(graphics = {                                                                                                           Text(origin = {3, -71}, extent = {{-145, 13}, {145, -13}}, textString = "%name"), Polygon(fillColor = {95, 95, 95}, fillPattern = FillPattern.Solid, points = {{120, 40}, {60, -20}, {-60, -20}, {-120, 40}, {120, 40}})},                                                                                                                                                                         coordinateSystem(extent={{-140,
            -60},{140,80}})));
end Catenary;
