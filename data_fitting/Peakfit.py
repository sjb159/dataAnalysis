'''
Created on 23 Oct 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 
from Tools import Tools
from lmfit import models

dr = Tools.ReadWriteData()
folder = "S://Science//I10//LYSMO//data//"
scans = 186387
dr.read_file("%s%s.dat" %(folder,scans))
data = dr.get_data()

y = data["ifioft"]
x = data["ddth"]
peaks, _ = signal.find_peaks(y,  height = 0.01, width = 5)
print peaks
model_1 = models.GaussianModel(prefix='m1_')
model_2 = models.GaussianModel(prefix='m2_')
model_3 = models.GaussianModel(prefix='m3_')
model_4 = models.LinearModel(prefix='l3_')
model_5 = models.LorentzianModel(prefix='m4_')

model = model_1 + model_2  + model_3  + model_4 #+ model_5

model_1.set_param_hint("amplitude", min = 0.002, max = 0.1)
model_1.set_param_hint("sigma", min = 0.00, max = 0.025)
model_1.set_param_hint("center", min = x[peaks[0]]-0.05, max = x[peaks[0]]+0.05)
params_1 = model_1.make_params(amplitude = 0.05, center = x[peaks[0]], sigma = 0.01)

model_2.set_param_hint("amplitude", min = 1e-5, max = 1e-3)
model_2.set_param_hint("sigma", min = 0.0005, max = 0.1)
model_2.set_param_hint("center", min = x[peaks[1]]-0.075, max = x[peaks[1]]+0.075)
params_2 = model_2.make_params(amplitude = 0.005, center = x[peaks[1]], sigma= 0.03)

model_3.set_param_hint("amplitude", min = 1e-6, max = 1e-2)
model_3.set_param_hint("sigma", min = 0.005, max = 0.1)
model_3.set_param_hint("center", min = x[peaks[0]]-0.05, max = x[peaks[0]]+0.1)
params_3 = model_3.make_params(amplitude = 1e-3, center = x[peaks[0]]+0.040, sigma = 0.04)

model_4.set_param_hint("intercept", min = 0, max = 0.01)
model_4.set_param_hint("slope", min = 0)
params_4 = model_4.make_params(slope = 0, intercept = np.min(y))

"""model_5.set_param_hint("amplitude", min = 1e-6, max = 0.06)
model_5.set_param_hint("sigma", min = 0.00, max = 0.025)
model_5.set_param_hint("center", min = x[peaks[0]]-0.05, max = x[peaks[0]]+0.05)
params_5 = model_5.make_params(amplitude = 0.05, center = x[peaks[0]], sigma = 0.01)

"""

params = params_1.update(params_2)
params = params_1.update(params_3)
params = params_1.update(params_4)
#params = params_1.update(params_5)

params = params_1

output = model.fit(y, params, x=x)
print output.fit_report()
print output.best_values["m1_amplitude"]*0.3183099/output.best_values["m1_sigma"]
fig, gridspec = output.plot(data_kws={'markersize': 1})


plt.plot(x,y)
plt.semilogy()
plt.show()
