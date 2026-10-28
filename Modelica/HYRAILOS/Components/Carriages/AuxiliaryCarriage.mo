within HYRAILOS.Components.Carriages;
model AuxiliaryCarriage // Auxiliary carriage of the train (contains only the auxiliary services). It is a load only carriage.
  BasicElectricalComponents.Resistor Rt annotation (Placement(
        transformation(
        origin={20,56},
        extent={{-10,-10},{10,10}},
        rotation=-90)));
  BasicElectricalComponents.Inductor Lt annotation (Placement(
        transformation(
        origin={20,30},
        extent={{-10,-10},{10,10}},
        rotation=-90)));
  replaceable ElectricalComponents.AuxiliaryServices auxiliary annotation (
      Placement(transformation(
        origin={21,-17},
        extent={{-19,-19},{19,19}},
        rotation=-90)));
  ElectricalComponents.CarriageConnection carriageConnection annotation (
      Placement(transformation(origin={58,80}, extent={{-14,-14},{14,14}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p annotation (Placement(
        transformation(extent={{-70,-70},{-50,-50}}), iconTransformation(extent
          ={{-10,-110},{10,-90}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p1 annotation (Placement(
        transformation(extent={{10,70},{30,90}}), iconTransformation(extent={{
            -60,90},{-40,110}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p11 annotation (Placement(
        transformation(extent={{90,70},{110,90}}), iconTransformation(extent={{
            40,90},{60,110}})));
  Modelica.Blocks.Interfaces.RealInput Iaref annotation (Placement(
        transformation(extent={{116,-48},{76,-8}}), iconTransformation(
        extent={{-20,-20},{20,20}},
        rotation=90,
        origin={80,-100})));
equation
  connect(Rt.n,Lt. p) annotation(
    Line(points={{20,46},{20,40}},      color = {0, 0, 255}));
  connect(Lt.n,auxiliary. p) annotation(
    Line(points={{20,20},{21,18},{21,2}},                color = {0, 0, 255}));
  connect(p11, carriageConnection.p)
    annotation (Line(points={{100,80},{71.72,80}}, color={0,0,255}));
  connect(Rt.p, p1)
    annotation (Line(points={{20,66},{20,80}}, color={0,0,255}));
  connect(carriageConnection.n, p1)
    annotation (Line(points={{44.56,80},{20,80}}, color={0,0,255}));
  connect(p, auxiliary.n) annotation (Line(points={{-60,-60},{-60,-42},{20.81,
          -42},{20.81,-36}}, color={0,0,255}));
  connect(p1, p)
    annotation (Line(points={{20,80},{-60,80},{-60,-60}}, color={0,0,255}));
  connect(auxiliary.Iaref, Iaref) annotation (Line(points={{27.65,-28.02},{
          27.65,-28},{96,-28}}, color={0,0,127}));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
        Ellipse(
          extent={{-60,-80},{-20,-40}},
          lineColor={0,0,0},
          fillColor={135,135,135},
          fillPattern=FillPattern.Solid),
        Ellipse(
          extent={{20,-80},{60,-40}},
          lineColor={0,0,0},
          fillColor={135,135,135},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{-100,80},{100,80},{100,-2},{100,-60},{60,-60},{-100,-60},{
              -100,80}},
          lineColor={0,0,0},
          fillColor={175,175,175},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{80,60},{80,0},{20,0},{20,60},{80,60}},
          lineColor={0,0,0},
          fillColor={0,255,255},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{-100,-60},{-100,-20},{100,-20},{100,-42},{100,-60},{-100,-60}},
          lineColor={0,0,0},
          fillColor={238,46,47},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{72,80},{52,100},{-48,100},{-68,80},{72,80}},
          lineColor={0,0,0},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Line(
          points={{-100,-80},{100,-80}},
          color={95,95,95},
          thickness=1),
        Polygon(
          points={{-20,60},{-20,0},{-80,0},{-80,60},{-20,60}},
          lineColor={0,0,0},
          fillColor={0,255,255},
          fillPattern=FillPattern.Solid)}), Diagram(coordinateSystem(
          preserveAspectRatio=false)));
end AuxiliaryCarriage;
