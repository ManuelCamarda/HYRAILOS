within HYRAILOS.Components.EnergySources;
model LithiumIonBatteryDCcontrol // Lithium-ion battery interfaced with a DC-DC converter
  extends BaseEnergySourceDCcontrol(redeclare replaceable model EnergySource = HYRAILOS.Components.EnergySources.LithiumIonBattery,
  energySource(
    OCV_Max_b=OCV_Max_b,
    OCV_Min_b=OCV_Min_b,
    c_b=c_b,
    R_b=R_b,
    SoC_i=SoC_i,
    OCV_table=OCV_table),
    DCDCvoltage=1500);

  // Parameters
  parameter Modelica.Units.SI.Voltage OCV_Max_b "Open circuit battery voltage when fully charged";
  parameter Modelica.Units.SI.Voltage OCV_Min_b "Open circuit battery voltage when fully discharged";
  parameter Types.CapacityAh c_b "Battery capacity [Ah]";
  parameter Modelica.Units.SI.Resistance R_b "Battery internal resistance";
  parameter Real SoC_i(min = 0, max = 1) "Initial state of charge (0..1)";
  parameter Real OCV_table[:, 2] "OCV lookup table: SoC, cell OCV [V]";

  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={                                                                                                                                                                                                        Rectangle(                  fillColor = {0, 170, 0}, fillPattern = FillPattern.VerticalCylinder, extent={{-60,90},
              {60,-90}})}),                                      Diagram(
        coordinateSystem(preserveAspectRatio=false)));
end LithiumIonBatteryDCcontrol;
