within HYRAILOS.Components.EnergySources;
partial model BaseEnergySourceInterface // Common interface of an energy source (contains pin p and n, as well as the state of charge level)
  Modelica.Electrical.Analog.Interfaces.PositivePin p
    annotation (Placement(transformation(extent={{-10,90},{10,110}})));
  Modelica.Electrical.Analog.Interfaces.NegativePin n
    annotation (Placement(transformation(extent={{-10,-110},{10,-90}})));
  Modelica.Blocks.Interfaces.RealOutput SoC
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
        coordinateSystem(preserveAspectRatio=false)));
end BaseEnergySourceInterface;
