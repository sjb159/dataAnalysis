'''
Created on 4 Oct 2017

@author: wvx67826
'''

from Data_Reduction.ReadData import ReadData
import matplotlib.pyplot as plt
import matplotlib.cm as cm


RD = ReadData()

scan = 412209, 412210
T = []
I = []
F = []
I0 = []
Energy = 0
for i in scan:
    print i
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    RD.read_file(filename)
    Energy = float(RD.get_meta_value("pgm_energy"))
    T.append(RD.get_data()["egy_g"])
    I.append(RD.get_data()["mcsr17_g"])
    F.append(RD.get_data()["mcsr18_g"])
    I0.append(RD.get_data()["mcsr16_g"]+0.1)
#dataFile = 'data/Escan_CP_CN_' +"%s" %Energy +'_IrMn3_ordered.dat'
dataFile = 'data/Escan_th15_CP_CN' +"%s" %Energy +'_CoZnMn.dat'
f = open(dataFile, 'w+')
f.write("Energy CP \t ICP \t Energy CN \t ICN \t FLH \t FLV \t IXMCD \t FXMCD \t IXMCDR \t FXMCDR \n")
for i in range (0,len(T[0])):
    icp = (I[0][i]/I0[0][i])
    icn = (I[1][i]/I0[1][i])
    fcp = (F[0][i]/I0[0][i])
    fcn = (F[1][i]/I0[1][i])
    ixmcd = icp- icn
    fxmcd = fcp - fcn
    ixmcdr = ixmcd/(icp+icn)
    fxmcdr = fxmcd/(fcp+fcn)
    f.write("%f" %T[0][i] + "\t %f" %icp + "\t %f" %T[1][i]+ "\t %f" %icn + "\t %f" %fcp + "\t %f" %fcn
            + "\t %f" %ixmcd + "\t %f" %fxmcd + "\t %f" %ixmcdr + "\t %f" %fxmcdr + "\n" )

f.close()


plt.figure(1)
plt.subplot(221)
plt.title('Fe flou')
plt.plot(T[0],I0[0])
plt.subplot(222)
plt.title('Fe refl')
plt.plot(T[0],I[0]/I0[0])
plt.plot(T[1],I[1]/I0[1])
plt.subplot(223)
plt.plot(T[1],I[0])
plt.subplot(224)
plt.title('Rh refl')
plt.plot(T[1],I[1])
plt.show()