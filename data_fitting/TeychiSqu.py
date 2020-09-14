'''
Created on 29 Nov 2019

@author: wvx67826
'''
from Tools.ReadWriteData import ReadWriteData 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
from Tools.Output.Output import Output

dr = ReadWriteData()
Red = Output()
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


def chiSqu(data,model):
    return (data-model)**2/model


Tdfe = np.arange(0.0, 5.0, 0.025)
ohFe = np.arange(0.6, 2.0, 0.025)
chi = np.array([])
chiCo = np.array([])
x = np.array([])
y = np.array([])

for i in Tdfe:
    for j in ohFe:
        x = np.append(x,i)
        y = np.append(y,j)
        chi = np.append(chi,np.sum((chiSqu((teyFeData["Fe0TEY"]-np.min(teyFeData["Fe0TEY"])), teyCalfnFe(teyFeData["EnTeY"],  j, i)))))
        chiCo = np.append(chiCo,np.sum((chiSqu((teyCoData["Co02TEY"]-np.min(teyCoData["Co02TEY"])), teyCalfnCo(teyCoData["EnCoTEY"],  j, i)))))
        #print chi, chiCo


maximal_value = 11.5
minimal_value = 0.5
print (y[np.argmin(chi)],y[np.argmin(chiCo)] )
plt.subplot(221)
plt.title("Chi-Squ")
plt.tricontourf(x, y , chi, 130,interp = 'linear', cmap=plt.get_cmap('jet'), vmax = maximal_value)
plt.xlabel("TdFe")
plt.ylabel("OhFe")
plt.colorbar()
plt.subplot(222)
plt.plot(teyFeData["EnTeY"], teyFeData["Fe0TEY"], label = "FeTey" )
plt.plot(teyFeData["EnTeY"], teyCalfnFe(teyFeData["EnTeY"], y[np.argmin(chi)], x[np.argmin(chi)])/np.max(teyCalfnFe(teyFeData["EnTeY"], y[np.argmin(chi)], x[np.argmin(chi)])), label = "tdfe = %f, ohFe = %f" %(x[np.argmin(chi)], y[np.argmin(chi)]) )
plt.legend()

plt.subplot(223)
plt.tricontourf(x, y , chi, 130,interp = 'linear', cmap=plt.get_cmap('jet'), vmax = maximal_value)
plt.xlabel("TdFe")
plt.ylabel("OhFe")
plt.title("Chi-Squ")
plt.colorbar()
plt.subplot(224)
plt.plot(teyCoData["EnCoTEY"], teyCoData["Co02TEY"], label = "CoTey" )
plt.plot(teyCoData["EnCoTEY"], teyCalfnCo(teyCoData["EnCoTEY"], y[np.argmin(chiCo)], x[np.argmin(chiCo)])/np.max(teyCalfnCo(teyCoData["EnCoTEY"], y[np.argmin(chiCo)], x[np.argmin(chiCo)])), label = "tdCo = %f, ohCo = %f" %(x[np.argmin(chiCo)], y[np.argmin(chiCo)]) )
plt.legend()
plt.show()
    #print i, np.average(chiSqu(teyFeData["Fe0TEY"], teyCalfnFe(teyFeData["EnTeY"],  0.4, i)))




