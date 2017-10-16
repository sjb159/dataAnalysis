'''
Created on 4 Oct 2017

@author: wvx67826
'''

from Data_Reduction.ReadData import ReadData
import numpy as np
RD = ReadData()

temp = 0
scan =np.array([412523, 412524])
while temp < 412524:
        
    
    T = []
    I = []
    F = []
    I0 = []
    temp = scan[1]
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
    scan = scan+4
    dataFile = 'data/Escan_th15_CP_CN' +"%s" %Energy + "+field=%s" %Field +'_CoZnMn.dat'
    #dataFile = 'data/Escan_th15_Lh_LV' +"%s" %Energy + "+field=%s" %Field +'_CoZnMn.dat'
    f = open(dataFile, 'w+')
    
    f.write("Energy CP \t ICP \t Energy CN \t ICN \t FCP \t FCN \t IXMCD \t FXMCD \t IXMCDR \t FXMCDR \n")
    #f.write("Energy LH \t ILH \t Energy LV \t ILV \t FLH \t FLV \t IXMCD \t FXMCD \t IXMCDR \t FXMCDR \n")
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
    
    
