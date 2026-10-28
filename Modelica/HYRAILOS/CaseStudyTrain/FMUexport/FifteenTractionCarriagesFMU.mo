within HYRAILOS.CaseStudyTrain.FMUexport;

model FifteenTractionCarriagesFMU
  // Export the FMU of a train with 15 traction carriages and run it in Python
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyCatenary catenary annotation(
    Placement(transformation(origin = {4, -34}, extent = {{-220, 80}, {-178, 102}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage annotation(
    Placement(transformation(origin = {4, -34}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Icatref annotation(
    Placement(transformation(origin = {-207, 42}, extent = {{49, 7}, {35, -7}}, rotation = 90), iconTransformation(origin = {-146, 330}, extent = {{-7, -7}, {7, 7}}, rotation = 270)));
  Modelica.Blocks.Interfaces.RealInput booleancatenary annotation(
    Placement(transformation(origin = {-184, 42}, extent = {{49, 7}, {35, -7}}, rotation = 90), iconTransformation(origin = {-114, 330}, extent = {{-7, -7}, {7, 7}}, rotation = 270)));
  Modelica.Blocks.Interfaces.RealInput Iscref annotation(
    Placement(transformation(origin = {-169, -5}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref annotation(
    Placement(transformation(origin = {-168, 13}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref annotation(
    Placement(transformation(origin = {-169, -21}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref annotation(
    Placement(transformation(origin = {-100, -60}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref annotation(
    Placement(transformation(origin = {-139.5, -62.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-161, -22}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-162, 15}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-162, -3}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 420}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {48, -91}, extent = {{-10, -10}, {10, 10}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage1 annotation(
    Placement(transformation(origin = {142, -35}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref1 annotation(
    Placement(transformation(origin = {-31, -6}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref1 annotation(
    Placement(transformation(origin = {-30, 12}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref1 annotation(
    Placement(transformation(origin = {-31, -22}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref1 annotation(
    Placement(transformation(origin = {38, -61}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref1 annotation(
    Placement(transformation(origin = {-1.5, -63.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-23, -23}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-24, 14}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 392}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc1(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-24, -4}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 392}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage2 annotation(
    Placement(transformation(origin = {279, -35}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref2 annotation(
    Placement(transformation(origin = {106, -6}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref2 annotation(
    Placement(transformation(origin = {107, 12}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref2 annotation(
    Placement(transformation(origin = {106, -22}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref2 annotation(
    Placement(transformation(origin = {175, -61}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref2 annotation(
    Placement(transformation(origin = {135.5, -63.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH2(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {114, -23}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb2(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {113, 14}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 362}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc2(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {113, -4}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 362}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage3 annotation(
    Placement(transformation(origin = {417, -35}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref3 annotation(
    Placement(transformation(origin = {244, -6}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref3 annotation(
    Placement(transformation(origin = {245, 12}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref3 annotation(
    Placement(transformation(origin = {244, -22}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref3 annotation(
    Placement(transformation(origin = {313, -61}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref3 annotation(
    Placement(transformation(origin = {273.5, -63.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH3(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {252, -23}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb3(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {251, 14}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 336}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc3(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {251, -4}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 336}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage4 annotation(
    Placement(transformation(origin = {2, -169}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref4 annotation(
    Placement(transformation(origin = {-171, -140}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref4 annotation(
    Placement(transformation(origin = {-170, -122}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref4 annotation(
    Placement(transformation(origin = {-171, -156}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref4 annotation(
    Placement(transformation(origin = {-102, -195}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref4 annotation(
    Placement(transformation(origin = {-141.5, -197.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH4(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-163, -157}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb4(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-164, -120}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 310}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc4(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-164, -138}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 310}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage5 annotation(
    Placement(transformation(origin = {148, -171}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref5 annotation(
    Placement(transformation(origin = {-25, -142}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref5 annotation(
    Placement(transformation(origin = {-24, -124}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref5 annotation(
    Placement(transformation(origin = {-25, -158}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref5 annotation(
    Placement(transformation(origin = {44, -197}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref5 annotation(
    Placement(transformation(origin = {4.5, -199.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH5(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-17, -159}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb5(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-18, -122}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 280}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc5(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-18, -140}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 280}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage6 annotation(
    Placement(transformation(origin = {296, -171}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref6 annotation(
    Placement(transformation(origin = {123, -142}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref6 annotation(
    Placement(transformation(origin = {124, -124}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref6 annotation(
    Placement(transformation(origin = {123, -158}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref6 annotation(
    Placement(transformation(origin = {192, -197}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref6 annotation(
    Placement(transformation(origin = {152.5, -199.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH6(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {131, -159}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb6(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {130, -122}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 254}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc6(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {130, -140}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 254}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage7 annotation(
    Placement(transformation(origin = {436, -171}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref7 annotation(
    Placement(transformation(origin = {263, -142}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref7 annotation(
    Placement(transformation(origin = {264, -124}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref7 annotation(
    Placement(transformation(origin = {263, -158}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref7 annotation(
    Placement(transformation(origin = {332, -197}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref7 annotation(
    Placement(transformation(origin = {292.5, -199.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH7(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {271, -159}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb7(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {270, -122}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc7(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {270, -140}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 226}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Electrical.Analog.Basic.Ground ground1 annotation(
    Placement(transformation(origin = {51, -225}, extent = {{-10, -10}, {10, 10}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage8 annotation(
    Placement(transformation(origin = {0, -300}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref8 annotation(
    Placement(transformation(origin = {-173, -271}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref8 annotation(
    Placement(transformation(origin = {-172, -253}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref8 annotation(
    Placement(transformation(origin = {-173, -287}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref8 annotation(
    Placement(transformation(origin = {-104, -326}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref8 annotation(
    Placement(transformation(origin = {-143.5, -328.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH8(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-165, -288}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb8(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-166, -251}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc8(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-166, -269}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 200}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Electrical.Analog.Basic.Ground ground2 annotation(
    Placement(transformation(origin = {53, -356}, extent = {{-10, -10}, {10, 10}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage9 annotation(
    Placement(transformation(origin = {141, -302}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref9 annotation(
    Placement(transformation(origin = {-32, -273}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref9 annotation(
    Placement(transformation(origin = {-31, -255}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref9 annotation(
    Placement(transformation(origin = {-32, -289}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref9 annotation(
    Placement(transformation(origin = {37, -328}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref9 annotation(
    Placement(transformation(origin = {-2.5, -330.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH9(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-24, -290}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb9(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-25, -253}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 174}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc9(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-25, -271}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 174}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage10 annotation(
    Placement(transformation(origin = {296, -302}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref10 annotation(
    Placement(transformation(origin = {123, -273}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref10 annotation(
    Placement(transformation(origin = {124, -255}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref10 annotation(
    Placement(transformation(origin = {123, -289}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref10 annotation(
    Placement(transformation(origin = {192, -328}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref10 annotation(
    Placement(transformation(origin = {152.5, -330.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH10(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {131, -290}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb10(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {130, -253}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 148}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc10(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {130, -271}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 148}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage11 annotation(
    Placement(transformation(origin = {448, -302}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref11 annotation(
    Placement(transformation(origin = {275, -273}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref11 annotation(
    Placement(transformation(origin = {276, -255}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref11 annotation(
    Placement(transformation(origin = {275, -289}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref11 annotation(
    Placement(transformation(origin = {344, -328}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref11 annotation(
    Placement(transformation(origin = {304.5, -330.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH11(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {283, -290}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb11(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {282, -253}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 124}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc11(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {282, -271}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 124}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage12 annotation(
    Placement(transformation(origin = {-2, -436}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref12 annotation(
    Placement(transformation(origin = {-175, -407}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref12 annotation(
    Placement(transformation(origin = {-174, -389}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref12 annotation(
    Placement(transformation(origin = {-175, -423}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref12 annotation(
    Placement(transformation(origin = {-106, -462}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref12 annotation(
    Placement(transformation(origin = {-145.5, -464.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH12(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-167, -424}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb12(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-168, -387}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 98}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc12(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-168, -405}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 98}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage13 annotation(
    Placement(transformation(origin = {143, -436}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref13 annotation(
    Placement(transformation(origin = {-30, -407}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 72}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref13 annotation(
    Placement(transformation(origin = {-29, -389}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 72}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref13 annotation(
    Placement(transformation(origin = {-30, -423}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 72}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref13 annotation(
    Placement(transformation(origin = {39, -462}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 72}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref13 annotation(
    Placement(transformation(origin = {-0.5, -464.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 72}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH13(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-22, -424}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 74}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb13(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-23, -387}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 74}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc13(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {-23, -405}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 74}, extent = {{-7, -7}, {7, 7}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage14 annotation(
    Placement(transformation(origin = {298, -435}, extent = {{-186, 0}, {-126, 60}})));
  Modelica.Blocks.Interfaces.RealInput Iscref14 annotation(
    Placement(transformation(origin = {125, -406}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-192, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ibref14 annotation(
    Placement(transformation(origin = {126, -388}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-248, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Ifcref14 annotation(
    Placement(transformation(origin = {125, -422}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-220, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Iaref14 annotation(
    Placement(transformation(origin = {194, -461}, extent = {{49, 7}, {35, -7}}, rotation = 180), iconTransformation(origin = {-276, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealInput Itref14 annotation(
    Placement(transformation(origin = {154.5, -463.5}, extent = {{73.5, 10.5}, {52.5, -10.5}}, rotation = 180), iconTransformation(origin = {-304, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput LoH14(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {133, -423}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {484, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCb14(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {132, -386}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {428, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Blocks.Interfaces.RealOutput SoCsc14(max = 1, min = 0, start = 0.8) "State of charge (0..1)" annotation(
    Placement(transformation(origin = {132, -404}, extent = {{60, -6}, {72, 6}}), iconTransformation(origin = {456, 48}, extent = {{-7, -7}, {7, 7}})));
  Modelica.Electrical.Analog.Basic.Ground ground3 annotation(
    Placement(transformation(origin = {52, -490}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(catenary.n, caseStudyTractionCarriage.p1) annotation(
    Line(points = {{-184.5, 50.8714}, {-173, 50.8714}, {-173, 26.6}}, color = {0, 0, 255}));
  connect(booleancatenary, catenary.booleancatenary) annotation(
    Line(points = {{-184, 84}, {-184, 74}, {-184.5, 74}, {-184.5, 63.9143}}, color = {0, 0, 127}));
  connect(Itref, caseStudyTractionCarriage.Itref) annotation(
    Line(points = {{-202.5, -62.5}, {-176, -62.5}, {-176, -34}}, color = {0, 0, 127}));
  connect(Iaref, caseStudyTractionCarriage.Iaref) annotation(
    Line(points = {{-142, -60}, {-126, -60}, {-126, -34}, {-128, -34}}, color = {0, 0, 127}));
  connect(Ifcref, caseStudyTractionCarriage.IfuelCellRef) annotation(
    Line(points = {{-211, -21}, {-202, -21}, {-202, -22}, {-188, -22}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.IsupercapacitorRef, Iscref) annotation(
    Line(points = {{-188, -4}, {-188, -5}, {-211, -5}}, color = {0, 0, 127}));
  connect(Ibref, caseStudyTractionCarriage.IbatteryRef) annotation(
    Line(points = {{-210, 13}, {-210, 14}, {-188, 14}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.SoCb, SoCb) annotation(
    Line(points = {{-119, 14}, {-110, 14}, {-110, 15}, {-96, 15}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.SoCsc, SoCsc) annotation(
    Line(points = {{-119, -4}, {-112, -4}, {-112, -3}, {-96, -3}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.LoH, LoH) annotation(
    Line(points = {{-119, -22}, {-95, -22}}, color = {0, 0, 127}));
  connect(Icatref, catenary.Icatref) annotation(
    Line(points = {{-207, 84}, {-207, 75}, {-206, 75}, {-206, 64}}, color = {0, 0, 127}));
  connect(Itref1, caseStudyTractionCarriage1.Itref) annotation(
    Line(points = {{-64.5, -63.5}, {-38, -63.5}, {-38, -35}}, color = {0, 0, 127}));
  connect(Iaref1, caseStudyTractionCarriage1.Iaref) annotation(
    Line(points = {{-4, -61}, {12, -61}, {12, -35}, {10, -35}}, color = {0, 0, 127}));
  connect(Ifcref1, caseStudyTractionCarriage1.IfuelCellRef) annotation(
    Line(points = {{-73, -22}, {-64, -22}, {-64, -23}, {-50, -23}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.IsupercapacitorRef, Iscref1) annotation(
    Line(points = {{-50, -5}, {-50, -6}, {-73, -6}}, color = {0, 0, 127}));
  connect(Ibref1, caseStudyTractionCarriage1.IbatteryRef) annotation(
    Line(points = {{-72, 12}, {-72, 13}, {-50, 13}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.SoCb, SoCb1) annotation(
    Line(points = {{19, 13}, {28, 13}, {28, 14}, {42, 14}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.SoCsc, SoCsc1) annotation(
    Line(points = {{19, -5}, {26, -5}, {26, -4}, {42, -4}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.LoH, LoH1) annotation(
    Line(points = {{19, -23}, {43, -23}}, color = {0, 0, 127}));
  connect(catenary.p, ground.p) annotation(
    Line(points = {{-206, 50}, {-230, 50}, {-230, -81}, {48, -81}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage1.p1, caseStudyTractionCarriage.p11) annotation(
    Line(points = {{-35, 26}, {-148, 26}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage.p, ground.p) annotation(
    Line(points = {{-152, -34}, {-152, -81}, {48, -81}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage1.p, ground.p) annotation(
    Line(points = {{-14, -34}, {-14, -81}, {48, -81}}, color = {0, 0, 255}));
  connect(Itref2, caseStudyTractionCarriage2.Itref) annotation(
    Line(points = {{72.5, -63.5}, {99, -63.5}, {99, -35}}, color = {0, 0, 127}));
  connect(Iaref2, caseStudyTractionCarriage2.Iaref) annotation(
    Line(points = {{133, -61}, {149, -61}, {149, -35}, {147, -35}}, color = {0, 0, 127}));
  connect(Ifcref2, caseStudyTractionCarriage2.IfuelCellRef) annotation(
    Line(points = {{64, -22}, {73, -22}, {73, -23}, {87, -23}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.IsupercapacitorRef, Iscref2) annotation(
    Line(points = {{87, -5}, {87, -6}, {64, -6}}, color = {0, 0, 127}));
  connect(Ibref2, caseStudyTractionCarriage2.IbatteryRef) annotation(
    Line(points = {{65, 12}, {65, 13}, {87, 13}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.SoCb, SoCb2) annotation(
    Line(points = {{156, 13}, {165, 13}, {165, 14}, {179, 14}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.SoCsc, SoCsc2) annotation(
    Line(points = {{156, -5}, {163, -5}, {163, -4}, {179, -4}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.LoH, LoH2) annotation(
    Line(points = {{156, -23}, {180, -23}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.p1, caseStudyTractionCarriage1.p11) annotation(
    Line(points = {{102, 26}, {-10, 26}}, color = {0, 0, 255}));
  connect(ground.p, caseStudyTractionCarriage2.p) annotation(
    Line(points = {{48, -81}, {124, -81}, {124, -34}}, color = {0, 0, 255}));
  connect(Itref3, caseStudyTractionCarriage3.Itref) annotation(
    Line(points = {{210.5, -63.5}, {237, -63.5}, {237, -35}}, color = {0, 0, 127}));
  connect(Iaref3, caseStudyTractionCarriage3.Iaref) annotation(
    Line(points = {{271, -61}, {287, -61}, {287, -35}, {285, -35}}, color = {0, 0, 127}));
  connect(Ifcref3, caseStudyTractionCarriage3.IfuelCellRef) annotation(
    Line(points = {{202, -22}, {211, -22}, {211, -23}, {225, -23}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage3.IsupercapacitorRef, Iscref3) annotation(
    Line(points = {{225, -5}, {225, -6}, {202, -6}}, color = {0, 0, 127}));
  connect(Ibref3, caseStudyTractionCarriage3.IbatteryRef) annotation(
    Line(points = {{203, 12}, {203, 13}, {225, 13}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage3.SoCb, SoCb3) annotation(
    Line(points = {{294, 13}, {303, 13}, {303, 14}, {317, 14}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage3.SoCsc, SoCsc3) annotation(
    Line(points = {{294, -5}, {301, -5}, {301, -4}, {317, -4}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage3.LoH, LoH3) annotation(
    Line(points = {{294, -23}, {318, -23}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage2.p11, caseStudyTractionCarriage3.p1) annotation(
    Line(points = {{126, 26}, {240, 26}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage3.p, ground.p) annotation(
    Line(points = {{262, -34}, {262, -81}, {48, -81}}, color = {0, 0, 255}));
  connect(Itref4, caseStudyTractionCarriage4.Itref) annotation(
    Line(points = {{-204.5, -197.5}, {-178, -197.5}, {-178, -169}}, color = {0, 0, 127}));
  connect(Iaref4, caseStudyTractionCarriage4.Iaref) annotation(
    Line(points = {{-144, -195}, {-128, -195}, {-128, -169}, {-130, -169}}, color = {0, 0, 127}));
  connect(Ifcref4, caseStudyTractionCarriage4.IfuelCellRef) annotation(
    Line(points = {{-213, -156}, {-204, -156}, {-204, -157}, {-190, -157}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage4.IsupercapacitorRef, Iscref4) annotation(
    Line(points = {{-190, -139}, {-190, -140}, {-213, -140}}, color = {0, 0, 127}));
  connect(Ibref4, caseStudyTractionCarriage4.IbatteryRef) annotation(
    Line(points = {{-212, -122}, {-212, -121}, {-190, -121}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage4.SoCb, SoCb4) annotation(
    Line(points = {{-121, -121}, {-112, -121}, {-112, -120}, {-98, -120}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage4.SoCsc, SoCsc4) annotation(
    Line(points = {{-121, -139}, {-114, -139}, {-114, -138}, {-98, -138}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage4.LoH, LoH4) annotation(
    Line(points = {{-121, -157}, {-97, -157}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage3.p11, caseStudyTractionCarriage4.p1) annotation(
    Line(points = {{264, 26}, {342, 26}, {342, -98}, {-230, -98}, {-230, -108}, {-174, -108}}, color = {0, 0, 255}));
  connect(Itref5, caseStudyTractionCarriage5.Itref) annotation(
    Line(points = {{-58.5, -199.5}, {-32, -199.5}, {-32, -171}}, color = {0, 0, 127}));
  connect(Iaref5, caseStudyTractionCarriage5.Iaref) annotation(
    Line(points = {{2, -197}, {18, -197}, {18, -171}, {16, -171}}, color = {0, 0, 127}));
  connect(Ifcref5, caseStudyTractionCarriage5.IfuelCellRef) annotation(
    Line(points = {{-67, -158}, {-58, -158}, {-58, -159}, {-44, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage5.IsupercapacitorRef, Iscref5) annotation(
    Line(points = {{-44, -141}, {-44, -142}, {-67, -142}}, color = {0, 0, 127}));
  connect(Ibref5, caseStudyTractionCarriage5.IbatteryRef) annotation(
    Line(points = {{-66, -124}, {-66, -123}, {-44, -123}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage5.SoCb, SoCb5) annotation(
    Line(points = {{25, -123}, {34, -123}, {34, -122}, {48, -122}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage5.SoCsc, SoCsc5) annotation(
    Line(points = {{25, -141}, {32, -141}, {32, -140}, {48, -140}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage5.LoH, LoH5) annotation(
    Line(points = {{25, -159}, {49, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage5.p1, caseStudyTractionCarriage4.p11) annotation(
    Line(points = {{-28, -110}, {-150, -110}, {-150, -108}}, color = {0, 0, 255}));
  connect(Itref6, caseStudyTractionCarriage6.Itref) annotation(
    Line(points = {{89.5, -199.5}, {116, -199.5}, {116, -171}}, color = {0, 0, 127}));
  connect(Iaref6, caseStudyTractionCarriage6.Iaref) annotation(
    Line(points = {{150, -197}, {166, -197}, {166, -171}, {164, -171}}, color = {0, 0, 127}));
  connect(Ifcref6, caseStudyTractionCarriage6.IfuelCellRef) annotation(
    Line(points = {{81, -158}, {90, -158}, {90, -159}, {104, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage6.IsupercapacitorRef, Iscref6) annotation(
    Line(points = {{104, -141}, {104, -142}, {81, -142}}, color = {0, 0, 127}));
  connect(Ibref6, caseStudyTractionCarriage6.IbatteryRef) annotation(
    Line(points = {{82, -124}, {82, -123}, {104, -123}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage6.SoCb, SoCb6) annotation(
    Line(points = {{173, -123}, {182, -123}, {182, -122}, {196, -122}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage6.SoCsc, SoCsc6) annotation(
    Line(points = {{173, -141}, {180, -141}, {180, -140}, {196, -140}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage6.LoH, LoH6) annotation(
    Line(points = {{173, -159}, {197, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage6.p1, caseStudyTractionCarriage5.p11) annotation(
    Line(points = {{120, -110}, {-4, -110}}, color = {0, 0, 255}));
  connect(Itref7, caseStudyTractionCarriage7.Itref) annotation(
    Line(points = {{229.5, -199.5}, {256, -199.5}, {256, -171}}, color = {0, 0, 127}));
  connect(Iaref7, caseStudyTractionCarriage7.Iaref) annotation(
    Line(points = {{290, -197}, {306, -197}, {306, -171}, {304, -171}}, color = {0, 0, 127}));
  connect(Ifcref7, caseStudyTractionCarriage7.IfuelCellRef) annotation(
    Line(points = {{221, -158}, {230, -158}, {230, -159}, {244, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.IsupercapacitorRef, Iscref7) annotation(
    Line(points = {{244, -141}, {244, -142}, {221, -142}}, color = {0, 0, 127}));
  connect(Ibref7, caseStudyTractionCarriage7.IbatteryRef) annotation(
    Line(points = {{222, -124}, {222, -123}, {244, -123}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.SoCb, SoCb7) annotation(
    Line(points = {{313, -123}, {322, -123}, {322, -122}, {336, -122}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.SoCsc, SoCsc7) annotation(
    Line(points = {{313, -141}, {320, -141}, {320, -140}, {336, -140}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.LoH, LoH7) annotation(
    Line(points = {{313, -159}, {337, -159}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.p1, caseStudyTractionCarriage6.p11) annotation(
    Line(points = {{260, -110}, {144, -110}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage4.p, ground1.p) annotation(
    Line(points = {{-154, -168}, {-154, -214}, {52, -214}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage5.p, ground1.p) annotation(
    Line(points = {{-8, -170}, {-8, -214}, {52, -214}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage6.p, ground1.p) annotation(
    Line(points = {{140, -170}, {140, -214}, {52, -214}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage7.p, ground1.p) annotation(
    Line(points = {{280, -170}, {280, -214}, {52, -214}}, color = {0, 0, 255}));
  connect(Itref8, caseStudyTractionCarriage8.Itref) annotation(
    Line(points = {{-206.5, -328.5}, {-180, -328.5}, {-180, -300}}, color = {0, 0, 127}));
  connect(Iaref8, caseStudyTractionCarriage8.Iaref) annotation(
    Line(points = {{-146, -326}, {-130, -326}, {-130, -300}, {-132, -300}}, color = {0, 0, 127}));
  connect(Ifcref8, caseStudyTractionCarriage8.IfuelCellRef) annotation(
    Line(points = {{-215, -287}, {-206, -287}, {-206, -288}, {-192, -288}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage8.IsupercapacitorRef, Iscref8) annotation(
    Line(points = {{-192, -270}, {-192, -271}, {-215, -271}}, color = {0, 0, 127}));
  connect(Ibref8, caseStudyTractionCarriage8.IbatteryRef) annotation(
    Line(points = {{-214, -253}, {-214, -252}, {-192, -252}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage8.SoCb, SoCb8) annotation(
    Line(points = {{-123, -252}, {-114, -252}, {-114, -251}, {-100, -251}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage8.SoCsc, SoCsc8) annotation(
    Line(points = {{-123, -270}, {-116, -270}, {-116, -269}, {-100, -269}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage8.LoH, LoH8) annotation(
    Line(points = {{-123, -288}, {-99, -288}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage7.p11, caseStudyTractionCarriage8.p1) annotation(
    Line(points = {{284, -110}, {352, -110}, {352, -232}, {-232, -232}, {-232, -240}, {-176, -240}}, color = {0, 0, 255}));
  connect(Itref9, caseStudyTractionCarriage9.Itref) annotation(
    Line(points = {{-65.5, -330.5}, {-39, -330.5}, {-39, -302}}, color = {0, 0, 127}));
  connect(Iaref9, caseStudyTractionCarriage9.Iaref) annotation(
    Line(points = {{-5, -328}, {11, -328}, {11, -302}, {9, -302}}, color = {0, 0, 127}));
  connect(Ifcref9, caseStudyTractionCarriage9.IfuelCellRef) annotation(
    Line(points = {{-74, -289}, {-65, -289}, {-65, -290}, {-51, -290}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage9.IsupercapacitorRef, Iscref9) annotation(
    Line(points = {{-51, -272}, {-51, -273}, {-74, -273}}, color = {0, 0, 127}));
  connect(Ibref9, caseStudyTractionCarriage9.IbatteryRef) annotation(
    Line(points = {{-73, -255}, {-73, -254}, {-51, -254}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage9.SoCb, SoCb9) annotation(
    Line(points = {{18, -254}, {27, -254}, {27, -253}, {41, -253}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage9.SoCsc, SoCsc9) annotation(
    Line(points = {{18, -272}, {25, -272}, {25, -271}, {41, -271}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage9.LoH, LoH9) annotation(
    Line(points = {{18, -290}, {42, -290}}, color = {0, 0, 127}));
  connect(Itref10, caseStudyTractionCarriage10.Itref) annotation(
    Line(points = {{89.5, -330.5}, {116, -330.5}, {116, -302}}, color = {0, 0, 127}));
  connect(Iaref10, caseStudyTractionCarriage10.Iaref) annotation(
    Line(points = {{150, -328}, {166, -328}, {166, -302}, {164, -302}}, color = {0, 0, 127}));
  connect(Ifcref10, caseStudyTractionCarriage10.IfuelCellRef) annotation(
    Line(points = {{81, -289}, {90, -289}, {90, -290}, {104, -290}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage10.IsupercapacitorRef, Iscref10) annotation(
    Line(points = {{104, -272}, {104, -273}, {81, -273}}, color = {0, 0, 127}));
  connect(Ibref10, caseStudyTractionCarriage10.IbatteryRef) annotation(
    Line(points = {{82, -255}, {82, -254}, {104, -254}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage10.SoCb, SoCb10) annotation(
    Line(points = {{173, -254}, {182, -254}, {182, -253}, {196, -253}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage10.SoCsc, SoCsc10) annotation(
    Line(points = {{173, -272}, {180, -272}, {180, -271}, {196, -271}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage10.LoH, LoH10) annotation(
    Line(points = {{173, -290}, {197, -290}}, color = {0, 0, 127}));
  connect(Itref11, caseStudyTractionCarriage11.Itref) annotation(
    Line(points = {{241.5, -330.5}, {268, -330.5}, {268, -302}}, color = {0, 0, 127}));
  connect(Iaref11, caseStudyTractionCarriage11.Iaref) annotation(
    Line(points = {{302, -328}, {318, -328}, {318, -302}, {316, -302}}, color = {0, 0, 127}));
  connect(Ifcref11, caseStudyTractionCarriage11.IfuelCellRef) annotation(
    Line(points = {{233, -289}, {242, -289}, {242, -290}, {256, -290}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage11.IsupercapacitorRef, Iscref11) annotation(
    Line(points = {{256, -272}, {256, -273}, {233, -273}}, color = {0, 0, 127}));
  connect(Ibref11, caseStudyTractionCarriage11.IbatteryRef) annotation(
    Line(points = {{234, -255}, {234, -254}, {256, -254}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage11.SoCb, SoCb11) annotation(
    Line(points = {{325, -254}, {334, -254}, {334, -253}, {348, -253}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage11.SoCsc, SoCsc11) annotation(
    Line(points = {{325, -272}, {332, -272}, {332, -271}, {348, -271}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage11.LoH, LoH11) annotation(
    Line(points = {{325, -290}, {349, -290}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage8.p11, caseStudyTractionCarriage9.p1) annotation(
    Line(points = {{-152, -240}, {-36, -240}, {-36, -242}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage9.p11, caseStudyTractionCarriage10.p1) annotation(
    Line(points = {{-12, -242}, {120, -242}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage10.p11, caseStudyTractionCarriage11.p1) annotation(
    Line(points = {{144, -242}, {272, -242}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage8.p, ground2.p) annotation(
    Line(points = {{-156, -300}, {-156, -346}, {54, -346}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage9.p, ground2.p) annotation(
    Line(points = {{-14, -302}, {-14, -346}, {54, -346}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage10.p, ground2.p) annotation(
    Line(points = {{140, -302}, {140, -346}, {54, -346}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage11.p, ground2.p) annotation(
    Line(points = {{292, -302}, {292, -346}, {54, -346}}, color = {0, 0, 255}));
  connect(Itref12, caseStudyTractionCarriage12.Itref) annotation(
    Line(points = {{-208.5, -464.5}, {-182, -464.5}, {-182, -436}}, color = {0, 0, 127}));
  connect(Iaref12, caseStudyTractionCarriage12.Iaref) annotation(
    Line(points = {{-148, -462}, {-132, -462}, {-132, -436}, {-134, -436}}, color = {0, 0, 127}));
  connect(Ifcref12, caseStudyTractionCarriage12.IfuelCellRef) annotation(
    Line(points = {{-217, -423}, {-208, -423}, {-208, -424}, {-194, -424}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage12.IsupercapacitorRef, Iscref12) annotation(
    Line(points = {{-194, -406}, {-194, -407}, {-217, -407}}, color = {0, 0, 127}));
  connect(Ibref12, caseStudyTractionCarriage12.IbatteryRef) annotation(
    Line(points = {{-216, -389}, {-216, -388}, {-194, -388}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage12.SoCb, SoCb12) annotation(
    Line(points = {{-125, -388}, {-116, -388}, {-116, -387}, {-102, -387}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage12.SoCsc, SoCsc12) annotation(
    Line(points = {{-125, -406}, {-118, -406}, {-118, -405}, {-102, -405}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage12.LoH, LoH12) annotation(
    Line(points = {{-125, -424}, {-101, -424}}, color = {0, 0, 127}));
  connect(Itref13, caseStudyTractionCarriage13.Itref) annotation(
    Line(points = {{-63.5, -464.5}, {-37, -464.5}, {-37, -436}}, color = {0, 0, 127}));
  connect(Iaref13, caseStudyTractionCarriage13.Iaref) annotation(
    Line(points = {{-3, -462}, {13, -462}, {13, -436}, {11, -436}}, color = {0, 0, 127}));
  connect(Ifcref13, caseStudyTractionCarriage13.IfuelCellRef) annotation(
    Line(points = {{-72, -423}, {-63, -423}, {-63, -424}, {-49, -424}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage13.IsupercapacitorRef, Iscref13) annotation(
    Line(points = {{-49, -406}, {-49, -407}, {-72, -407}}, color = {0, 0, 127}));
  connect(Ibref13, caseStudyTractionCarriage13.IbatteryRef) annotation(
    Line(points = {{-71, -389}, {-71, -388}, {-49, -388}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage13.SoCb, SoCb13) annotation(
    Line(points = {{20, -388}, {29, -388}, {29, -387}, {43, -387}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage13.SoCsc, SoCsc13) annotation(
    Line(points = {{20, -406}, {27, -406}, {27, -405}, {43, -405}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage13.LoH, LoH13) annotation(
    Line(points = {{20, -424}, {44, -424}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage11.p11, caseStudyTractionCarriage12.p1) annotation(
    Line(points = {{296, -242}, {368, -242}, {368, -364}, {-230, -364}, {-230, -376}, {-178, -376}}, color = {0, 0, 255}));
  connect(Itref14, caseStudyTractionCarriage14.Itref) annotation(
    Line(points = {{91.5, -463.5}, {118, -463.5}, {118, -435}}, color = {0, 0, 127}));
  connect(Iaref14, caseStudyTractionCarriage14.Iaref) annotation(
    Line(points = {{152, -461}, {168, -461}, {168, -435}, {166, -435}}, color = {0, 0, 127}));
  connect(Ifcref14, caseStudyTractionCarriage14.IfuelCellRef) annotation(
    Line(points = {{83, -422}, {92, -422}, {92, -423}, {106, -423}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage14.IsupercapacitorRef, Iscref14) annotation(
    Line(points = {{106, -405}, {106, -406}, {83, -406}}, color = {0, 0, 127}));
  connect(Ibref14, caseStudyTractionCarriage14.IbatteryRef) annotation(
    Line(points = {{84, -388}, {84, -387}, {106, -387}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage14.SoCb, SoCb14) annotation(
    Line(points = {{175, -387}, {184, -387}, {184, -386}, {198, -386}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage14.SoCsc, SoCsc14) annotation(
    Line(points = {{175, -405}, {182, -405}, {182, -404}, {198, -404}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage14.LoH, LoH14) annotation(
    Line(points = {{175, -423}, {199, -423}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage12.p11, caseStudyTractionCarriage13.p1) annotation(
    Line(points = {{-154, -376}, {-34, -376}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage13.p11, caseStudyTractionCarriage14.p1) annotation(
    Line(points = {{-10, -376}, {54, -376}, {54, -374}, {122, -374}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage14.p11, ground3.p) annotation(
    Line(points = {{146, -374}, {222, -374}, {222, -480}, {52, -480}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage13.p, ground3.p) annotation(
    Line(points = {{-12, -436}, {-12, -480}, {52, -480}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage12.p, ground3.p) annotation(
    Line(points = {{-158, -436}, {-158, -480}, {52, -480}}, color = {0, 0, 255}));
  connect(caseStudyTractionCarriage14.p, ground3.p) annotation(
    Line(points = {{142, -434}, {142, -480}, {52, -480}}, color = {0, 0, 255}));
  annotation(
    Icon(coordinateSystem(preserveAspectRatio = true, extent = {{-320, 440}, {500, 40}}), graphics = {Rectangle(origin = {125, 220},lineColor = {0, 70, 130}, fillColor = {235, 246, 252}, fillPattern = FillPattern.Solid, lineThickness = 1, extent = {{-283, 62}, {283, -56}}, radius = 12), Line(origin = {-76, 248}, points = {{-90, 72}, {488, 72}}, color = {0, 120, 150}, thickness = 1), Line(origin = {-92, 228}, points = {{-54, 90}, {-38, 30}, {-22, 90}}, color = {0, 120, 150}, thickness = 1), Rectangle(origin = {-76, 220},lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {-76, 220},lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Line(origin = {-76, 212}, points = {{-74, -34}, {476, -34}}, color = {60, 70, 80}, thickness = 1.5), Ellipse(origin = {-80, 222}, lineColor = {40, 48, 56}, fillColor = {40, 48, 56}, fillPattern = FillPattern.Solid, extent = {{-58, -28}, {-42, -44}}), Text(origin = {108, 218}, textColor = {0, 70, 130}, extent = {{-72, 58}, {72, 42}}, textString = "HYRAILOS"), Text(origin = {112, 220},textColor = {0, 70, 130}, extent = {{-72, -44}, {72, -54}}, textString = "15 CARRIAGES FMU"), Rectangle(origin = {26, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {26, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {-42, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {-42, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {-8, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {-8, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {60, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {60, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {162, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {162, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {94, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {94, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {128, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {128, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {196, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {196, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Ellipse(origin = {330, 222}, lineColor = {40, 48, 56}, fillColor = {40, 48, 56}, fillPattern = FillPattern.Solid, extent = {{42, -28}, {58, -44}}), Rectangle(origin = {298, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {298, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {230, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {230, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {264, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {264, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {332, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {332, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {434, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {434, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {366, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {366, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2), Rectangle(origin = {400, 220}, lineColor = {0, 70, 130}, fillColor = {41, 128, 185}, fillPattern = FillPattern.Solid, extent = {{-68, 34}, {-38, -24}}, radius = 5), Rectangle(origin = {400, 220}, lineColor = {255, 255, 255}, fillColor = {218, 240, 250}, fillPattern = FillPattern.Solid, extent = {{-62, 24}, {-44, 4}}, radius = 2)}),
    Diagram(coordinateSystem(extent = {{-240, 100}, {380, -500}}), graphics));
end FifteenTractionCarriagesFMU;
