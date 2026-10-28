within HYRAILOS.Components.EnergySources;
model BaseEnergySourceDCcontrol // common structure of an energy source interfaced with a DC-DC converter
  replaceable model EnergySource = HYRAILOS.Components.EnergySources.BaseEnergySourceInterface
    constrainedby
    HYRAILOS.Components.EnergySources.BaseEnergySourceInterface;

  // Parameters
  parameter Modelica.Units.SI.Inductance Ldc "energy source DC link inductance value";
  parameter Modelica.Units.SI.Resistance Rdc "energy source DC link resistance value";

  // Model instances
  EnergySource energySource  annotation (Placement(transformation(extent={{-100,30},
            {-60,70}})));
  ElectricalComponents.DCDCConverter dCDCConverter annotation (Placement(transformation(extent={{-8,48},{38,94}})));
  Controllers.PIController PID annotation (Placement(transformation(extent={{-2,-80},{38,-40}})));
  BasicElectricalComponents.Resistor resistorDC(R=Rdc) annotation (Placement(transformation(extent={{50,58},{90,98}})));
  BasicElectricalComponents.Inductor inductorDC(L=Ldc) annotation (Placement(
        transformation(
        extent={{-20,-20},{20,20}},
        rotation=270,
        origin={90,36})));
  Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage(V=DCDCvoltage);// annotation (Placement(transformation(extent={{-20,100},{-40,120}})));

  // Inputs and Outputs
  Modelica.Blocks.Interfaces.RealInput Iref annotation (Placement(
        transformation(extent={{-120,-110},{-80,-70}}), iconTransformation(
          extent={{-120,60},{-80,100}})));
  Modelica.Blocks.Interfaces.RealOutput SoC annotation (Placement(
        transformation(extent={{-50,40},{-30,60}}), iconTransformation(extent={{
            90,80},{110,100}})));

  // Electrical Interfaces
  Modelica.Electrical.Analog.Interfaces.NegativePin pin_n_1 annotation (
      Placement(transformation(extent={{-110,-10},{-90,10}}),
        iconTransformation(extent={{-110,0},{-90,20}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin pin_n_3 annotation (
      Placement(transformation(extent={{90,-30},{110,-10}}), iconTransformation(
          extent={{90,-80},{110,-60}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin pin_n_2 annotation (
      Placement(transformation(extent={{90,-10},{110,10}}), iconTransformation(
          extent={{90,0},{110,20}})));

protected
  parameter Real DCDCvoltage;

equation
  connect(energySource.p, dCDCConverter.p_out) annotation (Line(
        points={{-80,70},{-80,80},{-8,80},{-8,79.28}}, color={0,0,255}));
  connect(dCDCConverter.p_in, resistorDC.p) annotation (Line(points={{38,78.36},{38,78},{50,78}}, color={0,0,255}));
  connect(resistorDC.n, inductorDC.p) annotation (Line(points={{90,78},{90,56}}, color={0,0,255}));
  connect(PID.y, dCDCConverter.dutyCycle) annotation (Line(points={{40,-60},{48,
          -60},{48,-24},{22,-24},{22,50},{22.13,50},{22.13,52.14}}, color={0,0,127}));
  connect(dCDCConverter.i_out, PID.u_s) annotation (Line(points={{8.1,50.76},{8.1,
          10},{8,10},{8,-28},{-16,-28},{-16,-60},{-6,-60}}, color={0,0,127}));
  connect(Iref, PID.u_m) annotation (Line(points={{-100,-90},{18,-90},{18,-84}}, color={0,0,127}));
  connect(dCDCConverter.n_in, pin_n_3) annotation (Line(points={{38,60.65},{60,60.65},
          {60,-20},{100,-20}}, color={0,0,255}));
  connect(inductorDC.n, pin_n_2) annotation (Line(points={{90,16},{90,0},{100,0}}, color={0,0,255}));
  connect(energySource.n, pin_n_1) annotation (Line(points={{-80,30},{-80,0},{-100,0}}, color={0,0,255}));
  connect(energySource.SoC, SoC) annotation (Line(points={{-60,50},{-40,50}}, color={0,0,127}));
  connect(constantVoltage.p, dCDCConverter.p_in);// annotation (Line(points={{-20,110},
  //        {42,110},{42,78.36},{38,78.36}}, color={0,0,255}));
  connect(constantVoltage.n, pin_n_1);// annotation (Line(points={{-40,110},{-120,110},
  //        {-120,0},{-100,0}}, color={0,0,255}));
  connect(dCDCConverter.n_out, pin_n_1) annotation (Line(points={{-7.77,59.96},{
          -18,59.96},{-18,0},{-100,0}}, color={0,0,255}));

  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
          Rectangle(extent={{-100,100},{100,-100}}, lineColor={28,108,200})}),
      Diagram(coordinateSystem(preserveAspectRatio=false)));
end BaseEnergySourceDCcontrol;
