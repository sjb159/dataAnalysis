'''
Created on 21 Sep 2017

@author: wvx67826
'''
from Data_Reduction.ReadData import ReadData
import matplotlib.pyplot as plt
import matplotlib.cm as cm

RD = ReadData()

scan = range(412811,412871,5)
print scan
T = []
I = []
F = []
I0 = []
for i in scan:
        
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    RD.read_file(filename)

    T.append(RD.get_data()["th"])
    I.append(RD.get_data()["norm_I0"])
    F.append(RD.get_data()["macr18"])
    I0.append(RD.get_data()["macr16"])
    
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i+3) +".dat"
    RD.read_file(filename)

    T.append(RD.get_data()["th"])
    I.append(RD.get_data()["norm_I0"])
    F.append(RD.get_data()["macr18"])
    I0.append(RD.get_data()["macr16"])
    

for i in range(0, len(T),4):
        
    plt.figure(i)
    plt.subplot(221)
    plt.title('Rh')
    plt.yscale('log')
    plt.plot(T[i],I[i])
    plt.plot(T[i+1],I[i+1])
    plt.subplot(222)
    plt.title('Rh')
    plt.plot(T[i],(I[i]-(I[i+1])/(I[i]+I[i+1])))
    plt.subplot(223)
    plt.title('Fe ')
    plt.yscale('log')
    plt.plot(T[i+2],I[i+2])
    plt.plot(T[i+3],I[i+3])
    plt.subplot(224)
    plt.title('Fe')
    plt.plot(T[i+2],(I[i+2]-(I[i+3])/(I[i+2]+I[i+3])))

plt.show()