%%plot();
%%print(short_ir_dist_voltage[1])
inv_ShortIRVoltage = 1./ShortIRVoltage
fit_equation = fit(ShortIRDist,inv_ShortIRVoltage,'poly1')
plot(fit_equation,ShortIRDist,inv_ShortIRVoltage,'o');