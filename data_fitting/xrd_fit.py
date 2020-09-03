'''
Created on 23 Oct 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 
from Tools import Tools
from lmfit import models

def fitData(x,y):
    peaks, _ = signal.find_peaks(y,  height = 0.01, width = 5)
    print peaks
    if peaks.size <3:
        if peaks[0]>100:
            peaks = np.insert(peaks, 0, peaks[0]-100)
        if peaks.size<3:
            if peaks[-1]<200:
                peaks = np.append(peaks,peaks[1]+90)
    print peaks
    

    model_1 = models.GaussianModel(prefix='m1_')
    model_2 = models.GaussianModel(prefix='m2_')
    model_3 = models.GaussianModel(prefix='m3_')
    model_4 = models.LinearModel(prefix='l3_')
    model_5 = models.LorentzianModel(prefix='m4_')
    
    model = model_1 + model_2  + model_3  + model_4 + model_5
    
    model_1.set_param_hint("amplitude", min = 0.002, max = 0.1)
    model_1.set_param_hint("sigma", min = 0.00, max = 0.025)
    model_1.set_param_hint("center", min = x[peaks[1]]-0.05, max = x[peaks[1]]+0.05)
    params_1 = model_1.make_params(amplitude = 0.05, center = x[peaks[1]], sigma = 0.01)
    
    model_2.set_param_hint("amplitude", min = 1e-5, max = 1e-3)
    model_2.set_param_hint("sigma", min = 0.0005, max = 0.1)
    model_2.set_param_hint("center", min = x[peaks[2]]-0.075, max = x[peaks[2]]+0.075)
    params_2 = model_2.make_params(amplitude = 0.005, center = x[peaks[2]], sigma= 0.03)
    
    model_3.set_param_hint("amplitude", min = 1e-6, max = 1e-2)
    model_3.set_param_hint("sigma", min = 0.005, max = 0.08)
    model_3.set_param_hint("center", min = x[peaks[1]], max = x[peaks[1]]+0.075)
    params_3 = model_3.make_params(amplitude = 1e-3, center = x[peaks[1]]+0.050, sigma = 0.02)
    
    """
    model_4.set_param_hint("intercept", min = 1e-15, max = np.min(y)*1.5)
    model_4.set_param_hint("slope", min = 1e-16)
    """
    params_4 = model_4.make_params(slope = -1e-12, intercept = np.min(y))
    
    model_5.set_param_hint("amplitude", min = 1e-6, max = 0.06)
    model_5.set_param_hint("sigma", min = 0.00, max = 0.025)
    model_5.set_param_hint("center", min = x[peaks[0]]-0.1, max = x[peaks[0]]+0.1)
    params_5 = model_5.make_params(amplitude = 0.05, center = x[peaks[0]], sigma = 0.01)


    params_1.update(params_2)
    params_1.update(params_3)
    params_1.update(params_4)
    params_1.update(params_5) 
    
    params = params_1
    
    output = model.fit(y, params, x=x)
    print output.fit_report()
    output.plot(data_kws={'markersize': 1})
    plt.plot(x,y)
    plt.semilogy()
    plt.show(block=False)

    return output

dr = Tools.ReadWriteData()
folder = "S://Science//I10//LYSMO//data//"

lTemp = np.array([])
lAreaLow = np.array([])
lArea = np.array([])
lAreaHigh = np.array([])
lAreaLowErr = np.array([])
lAreaErr = np.array([])
lAreaHighErr = np.array([])
lScans =[186387]#, 186385, 186429
for i, scans in enumerate(lScans):

    print scans
        
    dr.read_file("%s%s.dat" %(folder,scans))
    data = dr.get_data()
    y = data["ifioft"]
    x = data["ddth"]
    output = fitData(x, y)


    lTemp = np.append(lTemp,dr.get_meta_value("temp2"))

    #lTemp = np.append(lTemp,data["temp2"][0])
    lAreaLow = np.append(lAreaLow, output.params["m4_height"].value)
    lAreaLowErr =np.append(lAreaLowErr, output.params["m4_height"].stderr)  
                           
    lArea = np.append(lArea, output.params["m1_height"].value)
    lAreaErr =np.append(lAreaErr, output.params["m1_height"].stderr)  
    
    lAreaHigh = np.append(lAreaHigh, output.params["m2_height"].value)
    lAreaHighErr =np.append(lAreaHighErr, output.params["m2_height"].stderr)  
    


longName = ["Scan no", "temperature",   "lowPeak", "lowPeakError",  "refl", "reflError", "highPeak", "highPeakError"]
#longName = ["Scan no", "temperature",   "lowPeak",  "refl", "highPeak"]

temparray = np.vstack([lScans, lTemp,lAreaLow,lAreaLowErr,  lArea , lAreaErr , lAreaHigh, lAreaHighErr])
#temparray = np.vstack([lScans, lTemp, lAreaLow,  lArea , lAreaHigh])



arr = temparray
plt.show()
#np.savetxt("test.test", arr ,header = longName)
dr.write_ascii("C:\\Users\\wvx67826\Desktop\\TEY_Fit#\\test.test",longName, temparray)