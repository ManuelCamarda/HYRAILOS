within HYRAILOS.Components.ElectricalComponents;
model DCDCConverter
  parameter Real efficiency(min=Modelica.Constants.small, max=1) = 0.97
    "Constant averaged conversion efficiency";
  Real V_in "Input voltage [V], higher voltage";
  Real I_in "Input current [A]";
  Real V_out "Output voltage [V], lower voltage";
  Real I_out "Output current [A]";
  Real P_in "Input Power [W]";
  Real P_out "Output Power [W]";
  Modelica.Blocks.Interfaces.RealOutput lossPower(unit="W", min=0)
    "Converter power loss";
  Modelica.Electrical.Analog.Interfaces.PositivePin p_out annotation(
    Placement(transformation(origin={-140,-120},    extent = {{50, 110}, {70, 90}}), iconTransformation(origin = {-160, -64}, extent = {{50, 110}, {70, 90}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p_in annotation(
    Placement(transformation(origin={20,-120},    extent = {{50, 110}, {70, 90}}), iconTransformation(origin = {40, -68}, extent = {{50, 110}, {70, 90}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n_out annotation(
    Placement(transformation(origin={-21,-160},    extent = {{-70, 110}, {-50, 90}}), iconTransformation(origin = {-39, -148}, extent = {{-70, 110}, {-50, 90}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n_in annotation(
    Placement(transformation(origin={140,-161},    extent = {{-70, 110}, {-50, 90}}), iconTransformation(origin = {160, -145}, extent = {{-70, 110}, {-50, 90}})));
  Modelica.Blocks.Interfaces.RealInput dutyCycle "Duty cycle" annotation(
    Placement(transformation(origin={-11.5,30},   extent={{-80.5,12},{-57.5,-12}}), iconTransformation(origin={31,2},      extent = {{-98, -14}, {-70, 14}},
        rotation=90)));
  Modelica.Blocks.Interfaces.RealOutput i_out(unit = "A") "Current in the branch from p to n as output signal" annotation(
    Placement(transformation(origin={90,30},    extent = {{10, -10}, {-10, 10}}, rotation=180),  iconTransformation(origin={-30,-88},  extent = {{8, -8}, {-8, 8}}, rotation = 90)));
equation
  V_out = p_out.v - n_out.v;
  V_in = p_in.v - n_in.v;
  I_out = p_out.i;
  I_in = p_in.i;
  p_out.i + n_out.i = 0;
  p_in.i + n_in.i = 0;
  i_out = I_out;
  V_out = V_in*(1 - dutyCycle);
  I_in = noEvent(if I_out >= 0 then
      efficiency*I_out*(1 - dutyCycle)
    else
      I_out*(1 - dutyCycle)/efficiency);
  P_in = V_in*I_in;
  P_out = V_out*I_out;
  lossPower = max(P_out - P_in, 0);
  annotation(
    Diagram(graphics),
    Icon(graphics = {Rectangle(fillColor = {255, 155, 155}, fillPattern = FillPattern.Solid, lineThickness = 1, extent = {{-100, 80}, {100, -80}}), Line(points = {{-100, -80}, {100, 80}, {100, 80}, {100, 80}}, thickness = 0.75), Line(origin = {-78, 68}, points = {{-12, 0}, {12, 0}, {12, 0}}), Line(origin = {-78, 58}, points = {{-12, 0}, {12, 0}, {12, 0}}), Line(origin = {76, -58}, points = {{-12, 0}, {12, 0}, {12, 0}}), Line(origin = {76, -68}, points = {{-12, 0}, {12, 0}, {12, 0}}), Text(origin = {-5, 109}, extent = {{-165, 7}, {165, -7}}, textString = "%name")}));
end DCDCConverter;
