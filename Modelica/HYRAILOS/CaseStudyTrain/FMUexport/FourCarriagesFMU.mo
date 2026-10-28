within HYRAILOS.CaseStudyTrain.FMUexport;

model FourCarriagesFMU
  // Export the FMU of a train with 4 carriages and run it in Python
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyCatenary catenary annotation(
    Placement(transformation(extent = {{-220, 80}, {-178, 102}})));
  ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage annotation(
    Placement(transformation(extent = {{-186, 0}, {-126, 60}})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {0, -51}, extent = {{-10, -10}, {10, 10}})));
  ParametrizedComponents.CaseStudyAuxiliaryCarriage caseStudyAuxiliaryCarriage annotation(
    Placement(transformation(extent = {{-78, 0}, {-18, 60}})));
  ParametrizedComponents.CaseStudyAuxiliaryCarriage caseStudyAuxiliaryCarriage1 annotation(
    Placement(transformation(extent = {{22, 0}, {82, 60}})));
  ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage1 annotation(
    Placement(transformation(extent = {{132, 0}, {192, 60}})));
  Modelica.Blocks.Interfaces.RealInput Icatref annotation(
    Placement(transformation(origin = {-211, 76}, extent = {{49, 7}, {35, -7}}, rotation = 90), iconTransformation(origin = {-70, 112}, extent = {{-6, -6}, {6, 6}}, rotation = 270)));
  Modelica.Blocks.Interfaces.RealInput booleancatenary annotation(
    Placement(transformation(origin = {-188, 76}, extent = {{49, 7}, {35, -7}}, rotation = 90), iconTransformation(origin = {-38, 112}, extent = {{-6, -6}, {6, 6}}, rotation = 270)));
  Modelica.Blocks.Interfaces.RealInput Iscref annotation(
    Placement(transformation(origin = {-173, 29}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-98, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Ibref annotation(
    Placement(transformation(origin = {-172, 47}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-134, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref annotation(
    Placement(transformation(origin = {-173, 13}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-116, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Iaref annotation(
    Placement(transformation(origin = {-104, -26}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-152, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Itref annotation(
    Placement(transformation(origin = {-143.5, -28.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-170, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput LoH(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-165, 12}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {132, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-166, 49}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {96, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-166, 31}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {114, 40}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput LoH1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {158, 12}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {132, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {157, 49}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {96, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {157, 30}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {114, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Iaref_a annotation(
    Placement(transformation(origin = {5, -26}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-98, 18}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Iaref_a1 annotation(
    Placement(transformation(origin = {105, -27}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-98, -4}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Itref1 annotation(
    Placement(transformation(origin = {152, -25}, extent = {{35, 5}, {25, -5}}, rotation = 180), iconTransformation(origin = {-170, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Iaref1 annotation(
    Placement(transformation(origin = {214, -23}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-152, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref1 annotation(
    Placement(transformation(origin = {145, 12}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-116, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Ibref1 annotation(
    Placement(transformation(origin = {144, 48}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-134, -26}, extent = {{-6, -6}, {6, 6}})));
  Modelica.Blocks.Interfaces.RealInput Iscref1 annotation(
    Placement(transformation(origin = {144, 31}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-98, -26}, extent = {{-6, -6}, {6, 6}})));
equation
  connect(catenary.p, ground.p) annotation(
    Line(points = {{-209.35, 84.8714}, {-240, 84.8714}, {-240, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage.p, ground.p) annotation(
    Line(points = {{-156, 0}, {-156, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage.p11, caseStudyAuxiliaryCarriage.p1) annotation(
    Line(points = {{-153, 60.6}, {-146, 60.6}, {-146, 60}, {-63, 60}}, color = {0, 0, 255}));
  connect(catenary.n, caseStudyTractionCarriage.p1) annotation(
    Line(points = {{-188.5, 84.8714}, {-177, 84.8714}, {-177, 60.6}}, color = {0, 0, 255}));
  connect(caseStudyAuxiliaryCarriage.p11, caseStudyAuxiliaryCarriage1.p1) annotation(
    Line(points = {{-33, 60}, {37, 60}}, color = {0, 0, 255}));
  connect(caseStudyAuxiliaryCarriage1.p, ground.p) annotation(
    Line(points = {{52, 0}, {52, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(caseStudyAuxiliaryCarriage1.p11, caseStudyTractionCarriage1.p1) annotation(
    Line(points = {{67, 60}, {142, 60}, {142, 60.6}, {141, 60.6}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage1.p11, ground.p) annotation(
    Line(points = {{165, 60.6}, {208, 60.6}, {208, 60}, {240, 60}, {240, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage1.p, ground.p) annotation(
    Line(points = {{162, 0}, {162, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(caseStudyAuxiliaryCarriage.p, ground.p) annotation(
    Line(points = {{-48, 0}, {-48, -41}, {0, -41}}, color = {0, 0, 255}));
  connect(booleancatenary, catenary.booleancatenary) annotation(
    Line(points = {{-188, 118}, {-188, 108}, {-188.5, 108}, {-188.5, 97.9143}}, color = {0, 0, 127}));
  connect(Itref, caseStudyTractionCarriage.Itref) annotation(
    Line(points = {{-206.5, -28.5}, {-180, -28.5}, {-180, 0}}, color = {0, 0, 127}));
  connect(Iaref, caseStudyTractionCarriage.Iaref) annotation(
    Line(points = {{-146, -26}, {-130, -26}, {-130, 0}, {-132, 0}}, color = {0, 0, 127}));
  connect(Ifcref, caseStudyTractionCarriage.IfuelCellRef) annotation(
    Line(points = {{-215, 13}, {-206, 13}, {-206, 12}, {-192, 12}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.IsupercapacitorRef, Iscref) annotation(
    Line(points = {{-192, 30}, {-192, 29}, {-215, 29}}, color = {0, 0, 127}));
  connect(Ibref, caseStudyTractionCarriage.IbatteryRef) annotation(
    Line(points = {{-214, 47}, {-214, 48}, {-192, 48}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.SoCb, SoCb) annotation(
    Line(points = {{-123, 48}, {-114, 48}, {-114, 49}, {-100, 49}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.SoCsc, SoCsc) annotation(
    Line(points = {{-123, 30}, {-116, 30}, {-116, 31}, {-100, 31}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.LoH, LoH) annotation(
    Line(points = {{-123, 12}, {-99, 12}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.SoCb, SoCb1) annotation(
    Line(points = {{195, 48}, {212, 48}, {212, 49}, {223, 49}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.SoCsc, SoCsc1) annotation(
    Line(points = {{195, 30}, {223, 30}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.LoH, LoH1) annotation(
    Line(points = {{195, 12}, {224, 12}}, color = {0, 0, 127}));
  connect(Iaref_a, caseStudyAuxiliaryCarriage.Iaref) annotation(
    Line(points = {{-37, -26}, {-24, -26}, {-24, 0}}, color = {0, 0, 127}));
  connect(Iaref_a1, caseStudyAuxiliaryCarriage1.Iaref) annotation(
    Line(points = {{63, -27}, {76, -27}, {76, 0}}, color = {0, 0, 127}));
  connect(Iaref1, caseStudyTractionCarriage1.Iaref) annotation(
    Line(points = {{172, -23}, {172, -22}, {186, -22}, {186, 0}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.IfuelCellRef, Ifcref1) annotation(
    Line(points = {{126, 12}, {103, 12}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.IbatteryRef, Ibref1) annotation(
    Line(points = {{126, 48}, {102, 48}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.IsupercapacitorRef, Iscref1) annotation(
    Line(points = {{126, 30}, {112, 30}, {112, 31}, {102, 31}}, color = {0, 0, 127}));
  connect(Itref1, caseStudyTractionCarriage1.Itref) annotation(
    Line(points = {{122, -24}, {138, -24}, {138, 0}}, color = {0, 0, 127}));
  connect(Icatref, catenary.Icatref) annotation(
    Line(points = {{-211, 118}, {-211, 109}, {-210, 109}, {-210, 98}}, color = {0, 0, 127}));
  annotation(
    Icon(coordinateSystem(preserveAspectRatio = true, extent = {{-180, 120}, {140, -60}}), graphics = {Rectangle(lineColor = {0, 70, 130}, fillColor = {235, 246, 252}, fillPattern = FillPattern.Solid, lineThickness = 1, extent = {{-82, 62}, {82, -56}}, radius = 12), Line(origin = {0, 28}, points = {{-90, 72}, {90, 72}}, color = {0, 120, 150}, thickness = 1), Line(origin = {-16, 8},points = {{-54, 90}, {-38, 30}, {-22, 90}}, color = {0, 120, 150}, thickness = 1), Rectangle(lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(lineColor = {0, 70, 130}, fillColor = {75, 179, 166}, fillPattern = FillPattern.Solid, extent = {{-34, 34}, {-4, -24}}, radius = 5), Rectangle(lineColor = {0, 70, 130}, fillColor = {75, 179, 166}, fillPattern = FillPattern.Solid, extent = {{0, 34}, {30, -24}}, radius = 5), Rectangle(lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Line(origin = {0, -8},points = {{-74, -34}, {74, -34}}, color = {60, 70, 80}, thickness = 1.5), Ellipse(origin = {-4, 2},lineColor = {40, 48, 56}, fillColor = {40, 48, 56}, fillPattern = FillPattern.Solid, extent = {{-58, -28}, {-42, -44}}), Ellipse(origin = {0, 2},lineColor = {40, 48, 56}, fillColor = {40, 48, 56}, fillPattern = FillPattern.Solid, extent = {{42, -28}, {58, -44}}), Text(origin = {0, -2},textColor = {0, 70, 130}, extent = {{-72, 58}, {72, 42}}, textString = "HYRAILOS"), Text(textColor = {0, 70, 130}, extent = {{-72, -44}, {72, -54}}, textString = "4 CARRIAGES FMU"), Rectangle(origin = {102, 0},lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {102, 0},lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2)}),
    Diagram(coordinateSystem(preserveAspectRatio = false, extent = {{-240, 160}, {240, -60}}), graphics));
end FourCarriagesFMU;
