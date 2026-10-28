within HYRAILOS.Components.EnergySources;
model SupercapacitorDCcontrol // Supercapacitor interfaced with a DC-DC converter
  extends BaseEnergySourceDCcontrol(redeclare replaceable model EnergySource = HYRAILOS.Components.EnergySources.Supercapacitor,
  energySource(
    V_Max_sc=V_Max_sc,
    V_min_sc=V_min_sc,
    C_sc=C_sc,
    R_sc=R_sc,
    c_sc=c_sc,
    V_init_sc=V_init_sc,
    SoC_i=SoC_i),
    DCDCvoltage=1500);

  // Parameters
  parameter Modelica.Units.SI.Voltage V_Max_sc "Supercapacitor voltage when fully charged";
  parameter Modelica.Units.SI.Voltage V_min_sc "Supercapacitor voltage when fully discharged";
  parameter Modelica.Units.SI.Capacitance C_sc "Supercapacitor capacitance";
  parameter Modelica.Units.SI.Resistance R_sc "Supercapacitor internal resistance";
  parameter Types.CapacityWh c_sc "Supercapacitor capacity [Wh]";
  parameter Modelica.Units.SI.Voltage V_init_sc "Supercapacitor starting voltage";
  parameter Modelica.Units.SI.PerUnit SoC_i "Supercapacitor starting SoC";

  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={                                                                                                                                                           Rectangle(                  fillColor = {0, 85, 255}, fillPattern = FillPattern.VerticalCylinder, extent={{-80,60},
              {80,-60}})}),                                      Diagram(
        coordinateSystem(preserveAspectRatio=false)));
end SupercapacitorDCcontrol;
