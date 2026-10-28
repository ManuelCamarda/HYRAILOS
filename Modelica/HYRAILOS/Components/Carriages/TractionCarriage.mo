within HYRAILOS.Components.Carriages;

model TractionCarriage
  // Traction carriage of the train (contains the energy sources, traction motor, and auxiliary services)
  EnergySources.LithiumIonBatteryDCcontrol lithiumIonBatteryUnit annotation(
    Placement(transformation(origin = {-8, -4}, extent = {{-48, 60}, {-8, 100}})));
  EnergySources.SupercapacitorDCcontrol supercapacitorUnit annotation(
    Placement(transformation(extent = {{-48, 0}, {-8, 40}})));
  EnergySources.HydrogenFuelCellDCcontrol hydrogenFuelCellUnit annotation(
    Placement(transformation(extent = {{-48, -60}, {-8, -20}})));
  ElectricalComponents.CarriageConnection carriageConnection annotation(
    Placement(transformation(origin = {64, 82}, extent = {{-14, -14}, {14, 14}})));
  replaceable ElectricalComponents.TractionAuxiliaryServices tractionAuxiliary annotation(
    Placement(transformation(origin = {53, -61}, extent = {{-19, -19}, {19, 19}}, rotation = -90)));
  BasicElectricalComponents.Resistor Rt annotation(
    Placement(transformation(origin = {54, 30}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  BasicElectricalComponents.Inductor Lt annotation(
    Placement(transformation(origin = {54, -10}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput IbatteryRef annotation(
    Placement(transformation(extent = {{-120, 70}, {-80, 110}}), iconTransformation(extent = {{-140, 40}, {-100, 80}})));
  Modelica.Blocks.Interfaces.RealInput IfuelCellRef annotation(
    Placement(transformation(extent = {{-120, -50}, {-80, -10}}), iconTransformation(extent = {{-140, -80}, {-100, -40}})));
  Modelica.Blocks.Interfaces.RealInput IsupercapacitorRef annotation(
    Placement(transformation(extent = {{-120, 10}, {-80, 50}}), iconTransformation(extent = {{-20, -20}, {20, 20}}, rotation = 0, origin = {-120, 0})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p annotation(
    Placement(transformation(extent = {{-30, -110}, {-10, -90}}), iconTransformation(extent = {{-10, -110}, {10, -90}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p1 annotation(
    Placement(transformation(extent = {{20, 72}, {40, 92}}), iconTransformation(extent = {{-80, 92}, {-60, 112}})));
  Modelica.Electrical.Analog.Interfaces.PositivePin p11 annotation(
    Placement(transformation(extent = {{84, 72}, {104, 92}}), iconTransformation(extent = {{0, 92}, {20, 112}})));
  Modelica.Blocks.Interfaces.RealInput Itref annotation(
    Placement(transformation(extent = {{120, -70}, {80, -30}}), iconTransformation(extent = {{-20, -20}, {20, 20}}, rotation = 90, origin = {-80, -100})));
  Modelica.Blocks.Interfaces.RealInput Iaref annotation(
    Placement(transformation(origin = {0, -8}, extent = {{120, -90}, {80, -50}}), iconTransformation(origin = {80, -100}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Modelica.Blocks.Interfaces.RealOutput SoCb annotation(
    Placement(transformation(extent = {{0, 100}, {20, 120}}), iconTransformation(extent = {{-10, -10}, {10, 10}}, rotation = 0, origin = {110, 60})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc annotation(
    Placement(transformation(extent = {{-6, 40}, {14, 60}}), iconTransformation(extent = {{-10, -10}, {10, 10}}, rotation = 0, origin = {110, 0})));
  Modelica.Blocks.Interfaces.RealOutput LoH annotation(
    Placement(transformation(extent = {{-10, -20}, {10, 0}}), iconTransformation(extent = {{-10, -10}, {10, 10}}, rotation = 0, origin = {110, -60})));
equation
  connect(IbatteryRef, lithiumIonBatteryUnit.Iref) annotation(
    Line(points = {{-100, 90}, {-79, 90}, {-79, 92}, {-56, 92}}, color = {0, 0, 127}));
  connect(hydrogenFuelCellUnit.pin_n_1, p) annotation(
    Line(points = {{-48, -38}, {-70, -38}, {-70, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(supercapacitorUnit.pin_n_1, p) annotation(
    Line(points = {{-48, 22}, {-70, 22}, {-70, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(lithiumIonBatteryUnit.pin_n_1, p) annotation(
    Line(points = {{-56, 78}, {-56, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(lithiumIonBatteryUnit.pin_n_2, p1) annotation(
    Line(points = {{-16, 78}, {11, 78}, {11, 82}, {30, 82}}, color = {0, 0, 255}));
  connect(supercapacitorUnit.pin_n_2, p1) annotation(
    Line(points = {{-8, 22}, {30, 22}, {30, 82}}, color = {0, 0, 255}));
  connect(hydrogenFuelCellUnit.pin_n_2, p1) annotation(
    Line(points = {{-8, -38}, {30, -38}, {30, 82}}, color = {0, 0, 255}));
  connect(lithiumIonBatteryUnit.pin_n_3, p) annotation(
    Line(points = {{-16, 62}, {-16, 66}, {10, 66}, {10, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(supercapacitorUnit.pin_n_3, p) annotation(
    Line(points = {{-8, 6}, {10, 6}, {10, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(hydrogenFuelCellUnit.pin_n_3, p) annotation(
    Line(points = {{-8, -54}, {10, -54}, {10, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(p1, carriageConnection.n) annotation(
    Line(points = {{30, 82}, {50.56, 82}}, color = {0, 0, 255}));
  connect(p11, carriageConnection.p) annotation(
    Line(points = {{94, 82}, {77.72, 82}}, color = {0, 0, 255}));
  connect(p1, p1) annotation(
    Line(points = {{30, 82}, {30, 82}}, color = {0, 0, 255}));
  connect(p1, Rt.p) annotation(
    Line(points = {{30, 82}, {30, 46}, {54, 46}, {54, 40}}, color = {0, 0, 255}));
  connect(Rt.n, Lt.p) annotation(
    Line(points = {{54, 20}, {54, 0}}, color = {0, 0, 255}));
  connect(Lt.n, tractionAuxiliary.p) annotation(
    Line(points = {{54, -20}, {54, -42}, {53, -42}}, color = {0, 0, 255}));
  connect(tractionAuxiliary.n, p) annotation(
    Line(points = {{52.81, -80}, {52, -80}, {52, -86}, {-20, -86}, {-20, -100}}, color = {0, 0, 255}));
  connect(Iaref, tractionAuxiliary.Iaref) annotation(
    Line(points = {{100, -78}, {100, -70}, {59.65, -70}, {59.65, -72.02}}, color = {0, 0, 127}));
  connect(Itref, tractionAuxiliary.Itref) annotation(
    Line(points = {{100, -50}, {80, -50}, {80, -49.79}, {59.46, -49.79}}, color = {0, 0, 127}));
  connect(supercapacitorUnit.SoC, SoCsc) annotation(
    Line(points = {{-8, 38}, {-2, 38}, {-2, 50}, {4, 50}}, color = {0, 0, 127}));
  connect(SoCsc, SoCsc) annotation(
    Line(points = {{4, 50}, {4, 50}}, color = {0, 0, 127}));
  connect(lithiumIonBatteryUnit.SoC, SoCb) annotation(
    Line(points = {{-16, 94}, {-4, 94}, {-4, 110}, {10, 110}}, color = {0, 0, 127}));
  connect(hydrogenFuelCellUnit.SoC, LoH) annotation(
    Line(points = {{-8, -22}, {0, -22}, {0, -10}}, color = {0, 0, 127}));
  connect(IsupercapacitorRef, supercapacitorUnit.Iref) annotation(
    Line(points = {{-100, 30}, {-76, 30}, {-76, 36}, {-48, 36}}, color = {0, 0, 127}));
  connect(IfuelCellRef, hydrogenFuelCellUnit.Iref) annotation(
    Line(points = {{-100, -30}, {-76, -30}, {-76, -24}, {-48, -24}}, color = {0, 0, 127}));
  annotation(
    Icon(coordinateSystem(preserveAspectRatio = false), graphics = {Ellipse(extent = {{20, -80}, {60, -40}}, lineColor = {0, 0, 0}, fillColor = {135, 135, 135}, fillPattern = FillPattern.Solid), Ellipse(extent = {{-60, -80}, {-20, -40}}, lineColor = {0, 0, 0}, fillColor = {135, 135, 135}, fillPattern = FillPattern.Solid), Polygon(points = {{-100, 80}, {40, 80}, {100, -2}, {100, -42}, {60, -60}, {-100, -60}, {-100, 80}}, lineColor = {0, 0, 0}, fillColor = {175, 175, 175}, fillPattern = FillPattern.Solid), Polygon(points = {{40, 60}, {86, 0}, {20, 0}, {20, 60}, {40, 60}}, lineColor = {0, 0, 0}, fillColor = {0, 255, 255}, fillPattern = FillPattern.Solid), Polygon(points = {{0, 60}, {0, 0}, {-30, 0}, {-30, 60}, {0, 60}}, lineColor = {0, 0, 0}, fillColor = {85, 255, 255}, fillPattern = FillPattern.Solid), Polygon(points = {{-100, -60}, {-100, -20}, {100, -20}, {100, -42}, {60, -60}, {-100, -60}}, lineColor = {0, 0, 0}, fillColor = {238, 46, 47}, fillPattern = FillPattern.Solid), Rectangle(extent = {{-94, 60}, {-46, -32}}, lineColor = {0, 0, 0}, fillColor = {28, 108, 200}, fillPattern = FillPattern.Solid), Rectangle(extent = {{-80, 40}, {-60, 36}}, lineColor = {28, 108, 200}, fillColor = {0, 0, 0}, fillPattern = FillPattern.Solid), Rectangle(extent = {{-80, 50}, {-60, 46}}, lineColor = {28, 108, 200}, fillColor = {0, 0, 0}, fillPattern = FillPattern.Solid), Polygon(points = {{32, 80}, {12, 100}, {-68, 100}, {-88, 80}, {32, 80}}, lineColor = {0, 0, 0}, fillColor = {95, 95, 95}, fillPattern = FillPattern.Solid), Line(points = {{-100, -80}, {100, -80}}, color = {95, 95, 95}, thickness = 1)}),
    Diagram(coordinateSystem(preserveAspectRatio = false)));
end TractionCarriage;
