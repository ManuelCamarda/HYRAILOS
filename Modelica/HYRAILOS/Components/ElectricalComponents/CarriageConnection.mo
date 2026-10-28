within HYRAILOS.Components.ElectricalComponents;
model CarriageConnection // Connection between carriages
  parameter Modelica.Units.SI.Resistance R_l "Inter-carriage resistance";
  parameter Modelica.Units.SI.Inductance L_l "Inter-carriage inductance";
  BasicElectricalComponents.Resistor Rl(R=R_l) annotation (Placement(
        transformation(origin={-46,20}, extent={{-10,-10},{10,10}})));
  BasicElectricalComponents.Inductor Ll(L=L_l) annotation (Placement(
        transformation(origin={26,20}, extent={{-10,-10},{10,10}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p annotation(
    Placement(transformation(origin = {40, -80}, extent = {{50, 110}, {70, 90}}), iconTransformation(origin = {38, -100}, extent = {{50, 110}, {70, 90}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n annotation(
    Placement(transformation(origin = {-40, -80}, extent = {{-70, 110}, {-50, 90}}), iconTransformation(origin = {-36, -100}, extent = {{-70, 110}, {-50, 90}})));
equation
  connect(Rl.n, Ll.p) annotation(
    Line(points = {{-36, 20}, {16, 20}}, color = {0, 0, 255}));
  connect(Rl.p, n) annotation(
    Line(points = {{-56, 20}, {-100, 20}}, color = {0, 0, 255}));
  connect(Ll.n, p) annotation(
    Line(points = {{36, 20}, {100, 20}}, color = {0, 0, 255}));
  annotation(
    Icon(graphics = {Rectangle(origin = {1, -2}, fillColor = {255, 170, 0}, fillPattern = FillPattern.Solid, extent = {{-93, 90}, {93, -90}}), Text(origin = {-6, 180}, textColor = {0, 0, 255}, extent = {{-186, -60}, {186, -84}}, textString = "%name")}),
    Diagram(graphics));
end CarriageConnection;
