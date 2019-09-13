'''
Created on 2 Jul 2019

@author: wvx67826
'''
import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
from Tools.Tools import Tools

dr = Tools()
folder =  "Y:\\SQUID\\Relm\\3dice\\"
filename = folder +"HvM_NoAu_00001.dat"
with  open(filename,'r') as f:
    meta = True
    tMeta = []
    tData = []
    # break up the meta and data
    for line in f:
        tMeta.append(line) 
        if not meta:
            tData.append(line) 
        if "[Data]" in line:
            meta = False

k = np.genfromtxt(tData, names = True, delimiter = ",")
l =  ascii.read(tData,delimiter=',')
print  l["Magnetic Field (Oe)"][0]

x = "Magnetic Field (Oe)"
y = "Moment (emu)"#"DC Moment Fixed Ctr (emu)" #"Moment (emu)"#
z = "Temperature (K)"
#print l["Temperature (K)"], l["Magnetic Field (Oe)"][0], l["Moment (emu)"]

lastT = l[z][0]
field = []
moment = []
plt.figure(1)
for i, tempData in enumerate (l[z]):
    newT = l[z][i]
    if abs(newT-lastT)<1:
        print tempData, l[z][i], l[y][i]
        field.append(l[x][i])
        moment.append(l[y][i])
        
    else:
        plt.plot(field,moment, label  = "%s" %lastT)

        field = []
        moment = []
        
        print "next T"
    lastT = newT
plt.legend()
plt.show()
        
        