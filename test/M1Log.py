'''
Created on 22 Nov 2018

@author: wvx67826

'''
import matplotlib.pyplot as plt
import numpy as np

filename = ("//dc/dls_sw/i10/scripts/beamline/logs/M1_position.log")
strings = ("RBV=", "string2", "string3")
RBV = np.array([])
with open(filename,'r') as f:
    for line in f:
        if any(s in line for s in strings):
            #RBV.append(float(line[-35:-27])/0.02*1.6)
            RBV = np.append(RBV, float(line[-35:-27])/0.02*1.6)
            
print np.max(RBV)-np.min(RBV)
k = open("M1_Log1.dat", 'w+')
print RBV
for i in RBV:
    k.write("%s \n" %i)

plt.plot(RBV)
plt.show()