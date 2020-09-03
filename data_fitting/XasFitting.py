'''
Created on 24 Aug 2020

@author: wvx67826
'''


from Tools import Tools  # import the i10 Tools for data 

import matplotlib.pyplot as plt # this is for ploting graph

import numpy as np # For maths

from scipy.optimize import curve_fit # for the chi-squ fitting
from scipy.stats import chisquare
from lmfit import Model 

dr = Tools.ReadWriteData() #This initialize the read and write class
oPTools = Tools.Output()  #This initialize the prebuild ploting
oPTools.add_clipboard_to_figures() #enable the ctrl-c ctrl-v for copy and paste for graph

folder = "C:\\Users\\wvx67826\\Desktop\\xas fitting\\" #data file dir
dataName = "1A-NP1-edge.dat"

#dataName ="1A-NP1-centre.dat"
# read in the data 
filename = folder +dataName
dr.read_file(filename, meta = False)
data = dr.get_data()


#read in the model

filename = folder +"Co0.dat"
dr.read_file(filename, meta = False)
co0 = dr.get_data()

filename = folder +"Co3o4.dat"
dr.read_file(filename, meta = False)
co3o4 = dr.get_data()

filename = folder +"CoO.dat"
dr.read_file(filename, meta = False)
coO = dr.get_data()



#combine the three models into one single function with weight

def xasModel(energy, *par):
    data = (
            par[0]*np.interp(energy,co0["energy"],co0["intensity"])
            + par[1]*np.interp(energy,co3o4["energy"],co3o4["intensity"])
            + par[2]*np.interp(energy,coO["energy"],coO["intensity"])
            )

    return data


popt, pcov = curve_fit (xasModel, data["energy"], data["intensity"], p0=(0.6,0.5,0.5)) #do the fitting

xasModelFit = xasModel(data["energy"], *popt) #calculate the fitted result
chiSqu = chisquare(data["intensity"],xasModelFit) #get chi -squ

#do some ploting
fig1= plt.figure(1)
plt.title("%s chi-squ = %.2f" %(dataName,chiSqu[0]))
plt.plot( data["energy"], data["intensity"], label = dataName)
plt.plot(data["energy"], xasModelFit, label = "Co0 = %.1f%% Co3o4 = %.1f%% CoO = %.1f%%" %(popt[0]/(popt[0]+popt[1]+popt[2])*100,popt[1]/(popt[0]+popt[1]+popt[2])*100,popt[2]/(popt[0]+popt[1]+popt[2])*100))
plt.legend()


#put it into i10 friendly format to use the tools function
outputDataName = ["energy","data", "fit"]
outputData = np.vstack([data["energy"],data["intensity"],xasModelFit])

#write the data out
outputFilename = folder + "fit" +dataName 
dr.write_ascii(outputFilename, outputDataName, outputData)#write out data
fig1.savefig(outputFilename.split(".")[0]+".jpg") #save the plot 
plt.show()


