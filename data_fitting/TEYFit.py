'''
Created on 27 Nov 2019

@author: wvx67826
'''
from Tools import Tools 
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from lmfit import Model 
dr = Tools.ReadWriteData()
Red = Tools.Output()
Red.add_clipboard_to_figures()
folder = "C:\\Users\\wvx67826\\Desktop\\Tey_Fit#\\"
#read data 

filename = folder +"Tey_Fe.dat"
dr.read_file(filename, meta = False)
teyFeData = dr.get_data()

filename = folder +"Tey_Co.dat"
dr.read_file(filename, meta = False)
teyCoData = dr.get_data()

filename = folder +"Tey_cal.dat"
dr.read_file(filename, meta = False)
teyCal = dr.get_data()
teyCoCalName = ["Ene_Co"  ,  "OhCo"  ,  "TdCo" ,   "ohTdCo"]
teyFeCalName = ["EneFe"   ,  "OhFe"  ,  "TdFe" ,   "OhTdFe"]


calSpec = teyCal 
calname = teyFeCalName
def teyCalfnFe(energy, *par):
    data = (#par[0] + par[1]*energy 
            + par[0]*np.interp(energy,calSpec[calname[0]],calSpec[calname[1]])
            + par[1]*np.interp(energy,calSpec[calname[0]],calSpec[calname[2]]))

    return data


calnameCo = teyCoCalName


def teyCalfnCo(energy, *par):
    data = (#par[0] + par[1]*energy 
            + par[0]*np.interp(energy,calSpec[calnameCo[0]],calSpec[calnameCo[1]])
            + par[1]*np.interp(energy,calSpec[calnameCo[0]],calSpec[calnameCo[2]]))

    return data


#         c,   m   ,Ohfe ,TdFe ,OhTDFe
feProp = [0.0, 0.0 ,0.0  ,1.0  ,0.0]

energy = np.arange(680,720,0.1)
teyCalfnFe(710.85, 1e-3, -1e-3, 0.5, 0.5)


popt, pcov = curve_fit(teyCalfnFe, teyFeData["EnTeY"], teyFeData["Fe0TEY"], p0=(0.4,2.0))
print popt

plt.plot(teyFeData["EnTeY"], teyFeData["Fe0TEY"], label = "FeTey" )
plt.plot(teyFeData["EnTeY"], teyCalfnFe(teyFeData["EnTeY"], *popt), label = "FeModel ohFe = %i%% TdFe = %i%%" %(popt[0]/(popt[0]+popt[1])*100,popt[1]/(popt[0]+popt[1])*100))

popt, pcov = curve_fit(teyCalfnCo, teyCoData["EnCoTEY"], teyCoData["Co02TEY"], p0=(0.4,0.5))
print popt

plt.plot(teyCoData["EnCoTEY"], teyCoData["Co02TEY"],  label = "CoTey" )
plt.plot(teyCoData["EnCoTEY"], teyCalfnCo(teyCoData["EnCoTEY"], *popt), label = "CoModel ohCo = %i%% TdCo = %i%%"  %(popt[0]/(popt[0]+popt[1])*100,popt[1]/(popt[0]+popt[1])*100))
plt.legend()
plt.show()

