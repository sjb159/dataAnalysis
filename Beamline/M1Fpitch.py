'''
Created on 25 Sep 2017

@author: wvx67826
'''
from Data_Reduction.ReadData import ReadData
import matplotlib.pyplot as plt
import matplotlib.cm as cm

RD = ReadData()

for i in range(599,686):
    filename = "Z:/data/2017/cm16783-4/tmp/M1_position.log""
    RD.read_file(filename)
    tth = float(RD.get_meta_value("tth"))
    energy = float(RD.get_meta_value("pgm_energy"))

    for j in range(0,len(RD.get_data()["th"])):    
        dataMap.append([A2Q.cal_qx(tth, RD.get_data()["th"][j], energy),
                        A2Q.cal_qz(tth, RD.get_data()["th"][j], energy),
                        RD.get_data()["norm_I0"][j]])

