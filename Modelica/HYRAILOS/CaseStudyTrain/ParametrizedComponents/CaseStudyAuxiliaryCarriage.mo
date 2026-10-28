within HYRAILOS.CaseStudyTrain.ParametrizedComponents;
model CaseStudyAuxiliaryCarriage // Auxiliary carriage of the train with values
  extends Components.Carriages.AuxiliaryCarriage(
    carriageConnection(R_l=4e-3, L_l=20e-6),
    auxiliary(La=1.8e-3, Ra=1e-3),
    Rt(R=1e-3),
    Lt(L=1.8e-3));
end CaseStudyAuxiliaryCarriage;
