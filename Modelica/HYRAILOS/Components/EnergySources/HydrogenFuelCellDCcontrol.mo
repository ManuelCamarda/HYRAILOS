within HYRAILOS.Components.EnergySources;
model HydrogenFuelCellDCcontrol // Hydrogen fuel cell interfaced with a DC-DC converter
  extends BaseEnergySourceDCcontrol(redeclare replaceable model EnergySource = HYRAILOS.Components.EnergySources.HydrogenFuelCell,
  energySource(
    OCV_h=OCV_h,
    mH2_max=mH2_max,
    LHV=LHV,
    Pfc_rated=Pfc_rated,
    R_fc=R_fc,
    R_H=R_H,
    C_H=C_H,
    SoC_i=SoC_i),
    DCDCvoltage=1500);

  // Parameters
  parameter Modelica.Units.SI.Voltage OCV_h "Fuel cell potential";
  parameter Modelica.Units.SI.Mass mH2_max(min=Modelica.Constants.small) "Maximum hydrogen mass [kg]";
  parameter Modelica.Units.SI.SpecificEnergy LHV(min=Modelica.Constants.small) "Hydrogen LHV [J/kg]";
  parameter Modelica.Units.SI.Power Pfc_rated(min=Modelica.Constants.small) "Rated nominal fuel-cell power [W]";
  parameter Modelica.Units.SI.Resistance R_fc "Fuel cell resistance";
  parameter Modelica.Units.SI.Resistance R_H "Fuel cell activation resistance";
  parameter Modelica.Units.SI.Capacitance C_H "Fuel cell activation capacitance";
  parameter Real SoC_i(min = 0, max = 1) "Initial normalized hydrogen mass (LoH)";


  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
                     Rectangle(                  fillColor = {0, 255, 255}, fillPattern = FillPattern.VerticalCylinder, extent={{-90,90},
              {90,-90}})}),                                      Diagram(
        coordinateSystem(preserveAspectRatio=false)));
end HydrogenFuelCellDCcontrol;
