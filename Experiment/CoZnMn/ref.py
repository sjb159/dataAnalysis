
'''
Created on 21 Sep 2017

@author: wvx67826
'''
from Data_Reduction.ReadData import ReadData
from Data_Reduction.AngleToQ import AngleToQ
import matplotlib.pyplot as plt
import matplotlib.cm as cm

RD = ReadData()
A2Q =AngleToQ()
scan = range(412215,412233)
field = []
TH = []
TTH = []
I = []
F = []
I0 = []
Inorm = []
E = []
for i in scan:
        
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    RD.read_file(filename)
    E.append(float(RD.get_meta_value("pgm_energy")))
    field.append(float(RD.get_meta_value("emecy1")))
    TH.append(RD.get_data()["th"])
    TTH.append(RD.get_data()["tth"])
    Inorm.append(RD.get_data()["norm_I0"])
    F.append(RD.get_data()["refl_sens"])
    I0.append(RD.get_data()["macr16"])
    I.append(RD.get_data()["macr17"])
    print i

q = A2Q.cal_qz(TH[0], TH[0], E[0])
for i in range (0, len(I),2):
        
    dataFile = 'data/Ref_E' +"%s" %E[i]+"F %s" %field[i] +'_CoZnMn.dat'
    f = open(dataFile, 'w+')
    f.write("Q \t ICP \t  ICN \t IXMCDR  \n")
    for j in range (0,len(q)):
        ixmcd = Inorm[i][j] -Inorm[i+1][j] 
        ixmcdr = ixmcd/(Inorm[i][j] + Inorm[i+1][j])

        f.write("%g" %q[j] + "\t %g" %Inorm[i][j] + "\t %g"  %Inorm[i+1][j]
                + "\t %g" %ixmcd + "\t %g" %ixmcdr +  "\n" )

    f.close()

