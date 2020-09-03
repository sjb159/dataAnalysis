'''
Created on 27 Nov 2019

@author: wvx67826
'''
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
    peaks, _ = signal.find_peaks(y,  height = 0.2, width = 5)
    print peaks

    model_1 = models.GaussianModel(prefix='m1_')
    model_4 = models.LinearModel(prefix='l3_')
    
    model = model_1 + model_4# + model_5
    
    #model_1.set_param_hint("amplitude", min = 0.002, max = 0.1)
    model_1.set_param_hint("sigma", min = 0.00, max = 0.025)
    model_1.set_param_hint("center", min = x[peaks[0]]-0.05, max = x[peaks[0]]+0.05)
    params_1 = model_1.make_params(amplitude = 0.05, center = x[peaks[0]], sigma = 0.01)
    
    """    model_4.set_param_hint("intercept", min = 1e-15, max = np.min(y)*1.5)
    model_4.set_param_hint("slope", min = 1e-16)
"""
    params_4 = model_4.make_params(slope = 1e-12, intercept = np.min(y))
    
    """    model_5.set_param_hint("amplitude", min = 1e-6, max = 0.06)
    model_5.set_param_hint("sigma", min = 0.00, max = 0.025)
    model_5.set_param_hint("center", min = x[peaks[0]]-0.1, max = x[peaks[0]]+0.1)
    params_5 = model_5.make_params(amplitude = 0.05, center = x[peaks[0]], sigma = 0.01)
    """


    params_1.update(params_4)
#    params_1.update(params_5) 
    
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

lScans =[186387]
for i, scans in enumerate(lScans):

    print scans
        
    dr.read_file("%s%s.dat" %(folder,scans))
    data = dr.get_data()
    y = data["ifioft"]
    x = data["ddth"]
    output = fitData(x, y)


    lTemp = np.append(lTemp,dr.get_meta_value("temp2"))
    print lTemp
    #lTemp = np.append(lTemp,data["temp2"][0])
    """    lAreaLow = np.append(lAreaLow, output.params["m4_height"].value)
    lAreaLowErr =np.append(lAreaLowErr, output.params["m4_height"].stderr)  
         """                       
    lArea = np.append(lArea, output.params["m1_height"].value)
    lAreaErr =np.append(lAreaErr, output.params["m1_height"].stderr)  
    


#longName = "temperature   lowPeak lowPeakError  refl reflError highPeak highPeakError"
longName = ["scan no", "temperature",  "refl",  "reflError"]
temparray = np.vstack([lScans, lTemp, lArea , lAreaErr])
print temparray


arr = temparray
plt.show()
#np.savetxt("test.test", arr ,header = longName)
dr.write_ascii("O25292.test",longName, temparray)

