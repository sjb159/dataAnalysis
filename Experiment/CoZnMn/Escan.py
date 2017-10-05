'''
Created on 4 Oct 2017

@author: wvx67826
'''

from Data_Reduction.ReadData import ReadData
import matplotlib.pyplot as plt
import matplotlib.cm as cm


RD = ReadData()

scan = range(412529,412561,4)
T = []
I = []
F = []
I0 = []
Field = 0
Energy = 0
k= 0
for i in scan:
    print i
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    RD.read_file(filename)
    Energy = float(RD.get_meta_value("pgm_energy"))
    Field = float(RD.get_meta_value("emecy1"))
    T.append(RD.get_data()["egy_g"])
    I.append(RD.get_data()["mcsr17_g"])
    F.append(RD.get_data()["mcsr18_g"])
    I0.append(RD.get_data()["mcsr16_g"]+0.1)
#dataFile = 'data/Escan_CP_CN_' +"%s" %Energy +'_IrMn3_ordered.dat'
    dataFile = 'data/Escan_th15_CP_CN' +"%s" %Energy + "+field=%s" %Field +'_CoZnMn.dat'
    f = open(dataFile, 'w+')
    f.write("Energy CP \t ICP \t Energy CN \t ICN \t FLH \t FLV \t IXMCD \t FXMCD \t IXMCDR \t FXMCDR \n")
    for j in range (0,len(T[0])):
        icp = (I[k][j]/I0[k][j])
        icn = (I[k+1][j]/I0[k+1][j])
        fcp = (F[k][j]/I0[k][j])
        fcn = (F[k+1][j]/I0[k+1][j])
        ixmcd = icp- icn
        fxmcd = fcp - fcn
        ixmcdr = ixmcd/(icp+icn)
        fxmcdr = fxmcd/(fcp+fcn)
        f.write("%f" %T[k][j] + "\t %f" %icp + "\t %f" %T[k+1][j]+ "\t %f" %icn + "\t %f" %fcp + "\t %f" %fcn
                + "\t %f" %ixmcd + "\t %f" %fxmcd + "\t %f" %ixmcdr + "\t %f" %fxmcdr + "\n" )
    
    f.close()
    k=k+2

