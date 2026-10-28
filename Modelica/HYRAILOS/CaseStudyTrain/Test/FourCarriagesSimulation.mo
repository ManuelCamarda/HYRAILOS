within HYRAILOS.CaseStudyTrain.Test;
model FourCarriagesSimulation // A train with 4 carriages used only for simulation testing
  extends Modelica.Icons.Example;

  parameter Real tractioncurrentTable_raw[:, 2] = [0, 0; 60, 0; 120, 0; 180, 0; 240, 0; 300, 26.66; 360, 51.82; 420, 76.86; 480, 102.20; 540, 135.71; 600, 160.85; 660, 185.57; 720, 218.85; 780, 225.01; 840, 16.54; 900, 16.58; 960, 16.58; 1020, 16.58; 1080, 16.58; 1140, 16.58; 1200, 15.55; 1260, 10.39; 1320, 7.28; 1380, 7.28; 1440, 7.28; 1500, 7.28; 1560, 7.28; 1620, 7.28; 1680, 7.28; 1740, 7.28; 1800, 7.28; 1860, -126.01; 1920, -139.42; 1980, -46.76; 2040, 11.56; 2100, 13.09; 2160, 24.71; 2220, 39.41; 2280, 39.41; 2340, 17.70; 2400, 11.56; 2460, 11.56; 2520, 11.56; 2580, 11.56; 2640, 11.56; 2700, 11.56; 2760, 11.56; 2820, 11.56; 2880, 11.56; 2940, 11.56; 3000, 11.56; 3060, 11.56; 3120, 46.45; 3180, 42.37; 3240, 40.68; 3300, 20.60; 3360, 9.94; 3420, 6.93; 3480, 4.77; 3540, 4.61; 3600, 4.61; 3660, 4.61; 3720, 4.61; 3780, 6.21; 3840, 8.38; 3900, 10.55; 3960, 11.56; 4020, 13.22; 4080, 16.50; 4140, 22.91; 4200, 10.15; 4260, 4.71; 4320, 4.61; 4380, 4.61; 4440, 4.61; 4500, 4.61; 4560, 4.61; 4620, 4.61; 4680, 20.99; 4740, 27.51; 4800, 23.47; 4860, 25.86; 4920, 17.70; 4980, 11.57; 5040, -102.85; 5100, -94.64; 5160, -77.94; 5220, -55.79; 5280, -39.36; 5340, -22.67; 5400, -4.23; 5460, -0.20; 5520, 0; 5580, 0; 5640, 0; 5700, 0; 5760, 0; 5820, 0; 5880, 0; 5940, 0; 6000, 0; 6060, 0; 6120, 0; 6180, 0; 6240, 0; 6300, 0; 6360, 0; 6420, 0; 6480, 0; 6540, 0; 6600, 0; 6660, 0; 6720, 30.44; 6780, 49.23; 6840, 82.63; 6900, 108.01; 6960, 133.11; 7020, 166.44; 7080, 191.33; 7140, 216.28; 7200, 182.81; 7260, 21.79; 7320, 21.79; 7380, 21.79; 7440, 21.79; 7500, -125.40; 7560, -132.72; 7620, -40.30; 7680, 4.70; 7740, 4.61; 7800, 4.61; 7860, 4.61; 7920, 4.61; 7980, 6.73; 8040, 4.61; 8100, 4.61; 8160, 11.55; 8220, 24.71; 8280, 10.81; 8340, 4.61; 8400, 4.61; 8460, 6.83; 8520, 10.31; 8580, 13.78; 8640, 15.73; 8700, 15.73; 8760, 15.73; 8820, 15.73; 8880, 15.73; 8940, 13.39; 9000, 23.86; 9060, 27.33; 9120, 21.11; 9180, 21.11; 9240, 21.11; 9300, 21.11; 9360, 21.11; 9420, 21.11; 9480, 21.11; 9540, 10.92; 9600, 5.74; 9660, 4.61; 9720, 4.61; 9780, 4.61; 9840, 4.61; 9900, 4.61; 9960, 19.69; 10020, 32.55; 10080, 16.45; 10140, 27.03; 10200, 14.37; 10260, 4.93; 10320, 4.61; 10380, 4.61; 10440, 4.61; 10500, 4.61; 10560, 5.93; 10620, 8.94; 10680, 11.19; 10740, 11.84; 10800, 11.84; 10860, 11.84; 10920, 10.13; 10980, 7.12; 11040, -105.95; 11100, -93.47; 11160, -71.32; 11220, -54.69; 11280, -38.24; 11340, -14.13; 11400, -3.79; 11460, -0.10; 11520, 0; 11580, 0; 11640, 0; 11700, 0] "Time-current pairs [s, A] for the reference traction current profile";
  parameter Real tractioncurrentTable[:, 2] = [tractioncurrentTable_raw[:, 1], 5*tractioncurrentTable_raw[:, 2]];
  parameter Real auxiliarycurrentTable[:, 2] = [60, 3.92; 120, 4.48; 180, 12.21; 240, 1.38; 300, 9.00; 360, 10.93; 420, 2.82; 480, 0.83; 540, 4.12; 600, 9.86; 660, 8.43; 720, 2.25; 780, 6.49; 840, 10.04; 900, 6.34; 960, 9.50; 1020, 14.51; 1080, 10.25; 1140, 5.87; 1200, 2.81; 1260, 5.19; 1320, 7.67; 1380, 13.37; 1440, 11.63; 1500, 4.77; 1560, 13.86; 1620, 7.06; 1680, 10.41; 1740, 1.61; 1800, 1.57; 1860, 3.03; 1920, 13.27; 1980, 10.20; 2040, 12.74; 2100, 9.67; 2160, 6.10; 2220, 7.75; 2280, 8.90; 2340, 12.93; 2400, 6.57; 2460, 13.38; 2520, 9.21; 2580, 12.44; 2640, 7.47; 2700, 10.39; 2760, 5.09; 2820, 7.84; 2880, 3.24; 2940, 1.51; 3000, 0.58; 3060, 10.53; 3120, 6.85; 3180, 13.47; 3240, 12.53; 3300, 5.78; 3360, 14.61; 3420, 8.88; 3480, 11.49; 3540, 6.11; 3600, 2.94; 3660, 2.58; 3720, 2.72; 3780, 9.06; 3840, 1.69; 3900, 0.30; 3960, 12.49; 4020, 1.49; 4080, 6.76; 4140, 7.33; 4200, 9.30; 4260, 7.56; 4320, 14.06; 4380, 11.26; 4440, 8.62; 4500, 9.26; 4560, 7.60; 4620, 14.47; 4680, 3.40; 4740, 10.34; 4800, 8.33; 4860, 0.63; 4920, 4.44; 4980, 13.91; 5040, 11.77; 5100, 0.19; 5160, 4.45; 5220, 0.15; 5280, 12.41; 5340, 1.66; 5400, 0.86; 5460, 14.73; 5520, 6.69; 5580, 4.78; 5640, 0.74; 5700, 5.84; 5760, 5.49; 5820, 7.85; 5880, 0.10; 5940, 2.22; 6000, 3.15; 6060, 6.61; 6120, 4.53; 6180, 9.20; 6240, 4.28; 6300, 13.64; 6360, 14.43; 6420, 0.89; 6480, 3.14; 6540, 8.45; 6600, 11.56; 6660, 0.96; 6720, 2.77; 6780, 6.85; 6840, 10.03; 6900, 13.55; 6960, 13.00; 7020, 11.91; 7080, 0.79; 7140, 14.65; 7200, 9.22; 7260, 1.29; 7320, 3.82; 7380, 9.31; 7440, 5.78; 7500, 6.70; 7560, 12.07; 7620, 12.36; 7680, 8.20; 7740, 11.89; 7800, 6.09; 7860, 14.62; 7920, 9.08; 7980, 14.52; 8040, 0.66; 8100, 13.24; 8160, 8.39; 8220, 10.70; 8280, 2.89; 8340, 8.23; 8400, 4.34; 8460, 1.58; 8520, 0.05; 8580, 13.60; 8640, 10.06; 8700, 3.08; 8760, 3.87; 8820, 6.98; 8880, 12.27; 8940, 1.76; 9000, 14.52; 9060, 14.16; 9120, 3.67; 9180, 9.61; 9240, 5.40; 9300, 10.46; 9360, 1.30; 9420, 7.05; 9480, 8.83; 9540, 9.40; 9600, 10.39; 9660, 13.37; 9720, 3.62; 9780, 2.30; 9840, 5.86; 9900, 8.53; 9960, 14.41; 10020, 10.66; 10080, 11.08; 10140, 14.59; 10200, 4.02; 10260, 3.89; 10320, 6.34; 10380, 4.43; 10440, 9.77; 10500, 14.28; 10560, 2.30; 10620, 7.77; 10680, 10.16; 10740, 7.40; 10800, 13.71; 10860, 11.05; 10920, 13.23; 10980, 1.68; 11040, 2.94; 11100, 0.99; 11160, 12.44; 11220, 14.44; 11280, 0.21; 11340, 11.84; 11400, 10.92; 11460, 13.62; 11520, 4.06; 11580, 10.72; 11640, 3.56; 11700, 1.14; 11760, 11.18] "Time-current pairs [s, A] for the reference auxiliary current profile";

  ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage
    annotation (Placement(transformation(extent={{-186,-20},{-126,40}})));
  ParametrizedComponents.CaseStudyAuxiliaryCarriage caseStudyAuxiliaryCarriage
    annotation (Placement(transformation(extent={{-78,-20},{-18,40}})));
  ParametrizedComponents.CaseStudyAuxiliaryCarriage caseStudyAuxiliaryCarriage1
    annotation (Placement(transformation(extent={{22,-20},{82,40}})));
  ParametrizedComponents.CaseStudyTractionCarriage caseStudyTractionCarriage1
    annotation (Placement(transformation(extent={{132,-20},{192,40}})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin={0,-71},      extent = {{-10, -10}, {10, 10}})));
  HYRAILOS.CaseStudyTrain.ParametrizedComponents.CaseStudyCatenary catenary
    annotation (Placement(transformation(extent={{-220,60},{-178,82}})));
  Modelica.Blocks.Sources.CombiTimeTable AuxiliaryCurrent(table=
        auxiliarycurrentTable, extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint)                                                             annotation(
    Placement(transformation(origin={-41,-139},  extent = {{-20, 40}, {0, 60}})));
  Modelica.Blocks.Sources.Constant catenarycurrent(k= 100)   annotation(
    Placement(transformation(origin={-250,110},   extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Step step(
    height=-1,
    offset=1,
    startTime=1000)                                                            annotation(
    Placement(transformation(origin={-230,150},  extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.CombiTimeTable TractionCurrent(table=
        tractioncurrentTable, extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint)                                                            annotation(
    Placement(transformation(origin={-260,-140},  extent = {{-20, 40}, {0, 60}})));
  Modelica.Blocks.Sources.CombiTimeTable AuxiliaryCurrent1(table=
        auxiliarycurrentTable, extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint)                                                             annotation(
    Placement(transformation(origin={-259,-181}, extent = {{-20, 40}, {0, 60}})));
  Modelica.Blocks.Math.Add add annotation(
    Placement(transformation(origin={-430,-30}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.CombiTimeTable TractionCurrent1(table=
        tractioncurrentTable, extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint)                                                            annotation(
    Placement(transformation(origin={120,-160},   extent = {{-20, 40}, {0, 60}})));
  Modelica.Blocks.Sources.CombiTimeTable AuxiliaryCurrent2(table=
        auxiliarycurrentTable, extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint)                                                             annotation(
    Placement(transformation(origin={121,-201},  extent = {{-20, 40}, {0, 60}})));
  Modelica.Blocks.Math.Gain gain(k=0.5)   annotation(
    Placement(transformation(origin={-358,20},  extent = {{10, -10}, {-10, 10}}, rotation = -0)));
  Modelica.Blocks.Math.Add add1(k2=-1)  annotation(
    Placement(transformation(origin={-408,26},    extent = {{10, -10}, {-10, 10}})));
  Modelica.Blocks.Math.Gain gain1(k=0.8) annotation (
    Placement(transformation(origin={-454,19},    extent = {{10, -10}, {-10, 10}})));
  Modelica.Blocks.Math.Add add2(k2=-1) annotation (
    Placement(transformation(origin={-491,51},    extent = {{10, -10}, {-10, 10}})));
  Modelica.Blocks.Math.Add add3
                               annotation(
    Placement(transformation(origin={344,-46},  extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Gain gain2(k=0.5)  annotation(
    Placement(transformation(origin={416,4},    extent = {{10, -10}, {-10, 10}}, rotation = -0)));
  Modelica.Blocks.Math.Add add4(k2=-1)  annotation(
    Placement(transformation(origin={366,10},     extent = {{10, -10}, {-10, 10}})));
  Modelica.Blocks.Math.Gain gain3(k=0.8) annotation (
    Placement(transformation(origin={320,3},      extent = {{10, -10}, {-10, 10}})));
  Modelica.Blocks.Math.Add add5(k2=-1) annotation (
    Placement(transformation(origin={283,35},     extent = {{10, -10}, {-10, 10}})));
equation
  connect(caseStudyTractionCarriage.p, ground.p)
    annotation (Line(points={{-156,-20},{-156,-61},{0,-61}}, color={0,0,255}));
  connect(caseStudyAuxiliaryCarriage.p, ground.p)
    annotation (Line(points={{-48,-20},{-48,-61},{0,-61}}, color={0,0,255}));
  connect(caseStudyAuxiliaryCarriage1.p, ground.p)
    annotation (Line(points={{52,-20},{52,-61},{0,-61}}, color={0,0,255}));
  connect(caseStudyTractionCarriage1.p, ground.p)
    annotation (Line(points={{162,-20},{162,-61},{0,-61}}, color={0,0,255}));
  connect(caseStudyTractionCarriage.p11, caseStudyAuxiliaryCarriage.p1) annotation (
      Line(points={{-153,40.6},{-146,40.6},{-146,40},{-63,40}}, color={0,0,255}));
  connect(caseStudyAuxiliaryCarriage.p11, caseStudyAuxiliaryCarriage1.p1)
    annotation (Line(points={{-33,40},{37,40}}, color={0,0,255}));
  connect(caseStudyAuxiliaryCarriage1.p11, caseStudyTractionCarriage1.p1) annotation
    (Line(points={{67,40},{142,40},{142,40.6},{141,40.6}}, color={0,0,255}));
  connect(caseStudyTractionCarriage1.p11, ground.p) annotation (Line(points={{165,40.6},
          {208,40.6},{208,40},{240,40},{240,-61},{0,-61}}, color={0,0,255}));
  connect(catenary.n, caseStudyTractionCarriage.p1) annotation (Line(points={{-188.5,
          64.8714},{-177,64.8714},{-177,40.6}}, color={0,0,255}));
  connect(catenary.p, ground.p) annotation (Line(points={{-209.35,64.8714},{
          -240,64.8714},{-240,-61},{0,-61}},
                                        color={0,0,255}));
  connect(AuxiliaryCurrent.y[1], caseStudyAuxiliaryCarriage.Iaref) annotation (
      Line(points={{-40,-89},{-32,-89},{-32,-72},{-24,-72},{-24,-20}}, color={0,
          0,127}));
  connect(AuxiliaryCurrent.y[1], caseStudyAuxiliaryCarriage1.Iaref) annotation (
      Line(points={{-40,-89},{16,-89},{16,-80},{76,-80},{76,-20}}, color={0,0,127}));
  connect(catenarycurrent.y, catenary.Icatref) annotation (Line(points={{-239,
          110},{-209.35,110},{-209.35,77.9143}},
                                            color={0,0,127}));
  connect(step.y, catenary.booleancatenary) annotation (Line(points={{-219,150},
          {-188.5,150},{-188.5,77.9143}}, color={0,0,127}));
  connect(TractionCurrent.y[1], caseStudyTractionCarriage.Itref) annotation (Line(
        points={{-259,-90},{-180,-90},{-180,-20}}, color={0,0,127}));
  connect(AuxiliaryCurrent1.y[1], caseStudyTractionCarriage.Iaref) annotation (
      Line(points={{-258,-131},{-220,-131},{-220,-130},{-132,-130},{-132,-20}},
        color={0,0,127}));
  connect(TractionCurrent1.y[1], caseStudyTractionCarriage1.Itref) annotation (
      Line(points={{121,-110},{138,-110},{138,-20}}, color={0,0,127}));
  connect(AuxiliaryCurrent2.y[1], caseStudyTractionCarriage1.Iaref) annotation (
      Line(points={{122,-151},{138,-151},{138,-150},{186,-150},{186,-20}},
        color={0,0,127}));
  connect(TractionCurrent.y[1], add.u2) annotation (Line(points={{-259,-90},{-252,
          -90},{-252,-66},{-456,-66},{-456,-36},{-442,-36}}, color={0,0,127}));
  connect(AuxiliaryCurrent1.y[1], add.u1) annotation (Line(points={{-258,-131},{
          -250,-131},{-250,-130},{-242,-130},{-242,-148},{-470,-148},{-470,-24},
          {-442,-24}}, color={0,0,127}));
  connect(add.y, gain.u) annotation (Line(points={{-419,-30},{-316,-30},{-316,20},
          {-346,20}}, color={0,0,127}));
  connect(gain.y, caseStudyTractionCarriage.IfuelCellRef) annotation (Line(points={
          {-369,20},{-374,20},{-374,-8},{-192,-8}}, color={0,0,127}));
  connect(add1.y, gain1.u) annotation (Line(points={{-419,26},{-430,26},{-430,19},
          {-442,19}}, color={0,0,127}));
  connect(add1.y, add2.u1) annotation (Line(points={{-419,26},{-430,26},{-430,57},
          {-479,57}}, color={0,0,127}));
  connect(gain1.y, add2.u2) annotation (Line(points={{-465,19},{-470,19},{-470,45},
          {-479,45}}, color={0,0,127}));
  connect(add2.y, caseStudyTractionCarriage.IsupercapacitorRef) annotation (Line(
        points={{-502,51},{-514,51},{-514,84},{-300,84},{-300,10},{-192,10}},
        color={0,0,127}));
  connect(add3.y, gain2.u) annotation (Line(points={{355,-46},{458,-46},{458,4},
          {428,4}}, color={0,0,127}));
  connect(add4.y, gain3.u) annotation (Line(points={{355,10},{344,10},{344,3},{332,
          3}}, color={0,0,127}));
  connect(add4.y, add5.u1) annotation (Line(points={{355,10},{344,10},{344,41},{
          295,41}}, color={0,0,127}));
  connect(gain3.y, add5.u2) annotation (Line(points={{309,3},{304,3},{304,29},{295,
          29}}, color={0,0,127}));
  connect(TractionCurrent1.y[1], add3.u1) annotation (Line(points={{121,-110},{202,
          -110},{202,-82},{286,-82},{286,-40},{332,-40}}, color={0,0,127}));
  connect(AuxiliaryCurrent2.y[1], add3.u2) annotation (Line(points={{122,-151},{
          312,-151},{312,-52},{332,-52}}, color={0,0,127}));
  connect(gain2.y, caseStudyTractionCarriage1.IfuelCellRef) annotation (Line(
        points={{405,4},{398,4},{398,-20},{220,-20},{220,-48},{108,-48},{108,-8},
          {126,-8}}, color={0,0,127}));
  connect(add5.y, caseStudyTractionCarriage1.IsupercapacitorRef) annotation (Line(
        points={{272,35},{268,35},{268,34},{258,34},{258,68},{98,68},{98,10},{126,
          10}}, color={0,0,127}));
  connect(gain.y, add1.u2) annotation(
    Line(points = {{-368, 20}, {-396, 20}}, color = {0, 0, 127}));
  connect(add.y, add1.u1) annotation(
    Line(points = {{-418, -30}, {-386, -30}, {-386, 32}, {-396, 32}}, color = {0, 0, 127}));
  connect(add3.y, add4.u1) annotation(
    Line(points = {{356, -46}, {390, -46}, {390, 16}, {378, 16}}, color = {0, 0, 127}));
  connect(gain2.y, add4.u2) annotation(
    Line(points = {{406, 4}, {378, 4}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage.IbatteryRef, gain1.y) annotation(
    Line(points = {{-192, 28}, {-249, 28}, {-249, 30}, {-280, 30}, {-280, 98}, {-470, 98}, {-470, 20}, {-464, 20}}, color = {0, 0, 127}));
  connect(caseStudyTractionCarriage1.IbatteryRef, gain3.y) annotation(
    Line(points = {{126, 28}, {110, 28}, {110, 90}, {304, 90}, {304, 4}, {310, 4}}, color = {0, 0, 127}));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
        coordinateSystem(preserveAspectRatio = false, extent = {{-520, 160}, {460, -180}})),
    experiment(
      StopTime=11700,
      Interval=0.5,
      Tolerance=1e-06, StartTime = 0));
end FourCarriagesSimulation;
