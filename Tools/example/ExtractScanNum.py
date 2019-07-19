'''
Created on 24 Jun 2019

@author: wvx67826
'''

from Tools import Tools
from Tools.I10DataReduction import I10DataReduction
import matplotlib.pyplot as plt
import numpy as np

#rd = Tools.ReadWriteData()
dr = I10DataReduction()
a2q = Tools.AngleToQ()
folder = "Z:/2019/cm22968-3/i10-"
lEscan = []
lRef = []
lBadScan = range(546531,546533)
temp = [546457,546514,546699,546696,546731,546736,546739,546740, 546741]+range(546712,546718) +range(546720,546731) +range(546748,546753)
lBadScan = lBadScan +temp# .append(546699)
#print lBadScan


#============================      This part read out the scan numbers for different scans ===============================
for i, scanNo in enumerate ([546455,546474,546509]): #(range (546455,546509)): #546522-546572,(range (546638,546976) 
    #print scanNo
    if (int(scanNo) in lBadScan):
        print "Passing escan"
        
    else:
        dr.tools.read_nexus_data(folder, scanNo)
        scanType = dr.tools.get_scan_type()
        if scanType[-6:] == "energy":
            temperature = dr.tools.get_nexus_meta("/ls340/Channel0Temp")
            sx = dr.tools.get_nexus_meta("/sx/sx")
            th = dr.tools.get_nexus_meta("/th/th")
            pol = dr.tools.get_nexus_meta("/pol/value") 
            energy = dr.tools.get_nexus_meta("/pgm_energy/pgm_energy")
            temp = "%s,%s,%.2f,%.2f,%.2f,%.2f" %(scanNo, pol, energy, sx, temperature, th) 
            lEscan.append(temp.split(","))
        if scanType == "th":
            energy = dr.tools.get_nexus_meta("/pgm_energy/pgm_energy")
            if 643>float(energy)>641.7: 
                print "alignment scan"
            else:
                temperature = dr.tools.get_nexus_meta("/ls340/Channel0Temp")
                sx = dr.tools.get_nexus_meta("/sx/sx")
                
                pol = dr.tools.get_nexus_meta("/pol/value") 
                temp = "%s,%s,%.2f, %.2f,%.2f" %(scanNo, pol, energy, sx, temperature)
                lRef.append(temp.split(","))
#==========================================================================================================================
                
output = "C:\\All my tools\\java-mars\\pyworkspace\\dataAnalysis\\Experiment\\old\\NSMO\\June2019\\data\\"

meta = ["/sx/sx","/ls340/Channel0Temp","/th/th"]
#print lEscan,lBadScan
for i, escan in enumerate (lEscan[:]):
    print escan[0]
    if (float(escan[0]) in lBadScan):
        print "Passing escan"
    elif float(escan[2])<540:
        pass
    elif escan[1] == "pc":
        dr.xas_pair_processing([int(escan[0])], folder,output, meta,pol1= "idu_circ_pos", 
                               pol2 = "idu_circ_neg", showPlot = False, linFit = False,
                               xasStartAverage= [1,20], xasEndAverage = [-11,-1])
"""    elif escan[1] == "lh":
        dr.xas_pair_processing([int(escan[0])], folder,output, meta,pol1= "idu_lin_hor", 
                       pol2 = "idu_lin_ver", showPlot = False, linFit = False,
                       xasStartAverage= [1,20], xasEndAverage = [-11,-1])
"""

meta = ["/sx/sx","/ls340/Channel0Temp","/pgm_energy/pgm_energy"]
for i, escan in enumerate (lRef[:]):
    print escan[0]
    
    if int(escan[0]) in lBadScan:
        print "Passing escan"
    elif escan[1] == "pc":
        dr.tools.read_nexus_data(folder,escan[0])
        energy = dr.tools.get_nexus_meta("/pgm_energy/pgm_energy")
        xPc = dr.tools.get_nexus_data("/tth/tth")
        qPc = a2q.cal_qz(xPc, xPc/2.0, energy)
        yPc = dr.tools.get_nexus_data("/rdeta/rnormdet")
        y2Pc = dr.tools.get_nexus_data("/rdeta/rnormfluo")
        yPcN = yPc/yPc[0]
        names = ["xPc", "qPc", "yPc", "y2Pc", "yPcN"]
        try:
            dr.tools.read_nexus_data(folder,int(escan[0])+1)
            xNc = dr.tools.get_nexus_data("/tth/tth")
            qNc = a2q.cal_qz(xPc, xPc/2.0, energy)
            yNc = dr.tools.get_nexus_data("/rdeta/rnormdet")
            y2Nc = dr.tools.get_nexus_data("/rdeta/rnormfluo")
            yPcN = yNc/yNc[0]
            data = [xPc, qPc, yPc, y2Pc, yPcN, xNc, qNc, yNc, y2Nc, yPcN]
            names = names +["xNc", "qNc", "yNc", "y2Nc", "yPcN"]
            
        except:
            pass
        
        """        if energy>950 and energy >950:
            plt.plot(qPc,yPc/yPc[0],  label = energy)
            plt.plot(qNc,yNc/yNc[0])
        """

"""        plt.semilogy()
        plt.legend()
        plt.show()"""


"""def footprintCorrection(v_intensity, v_th,v_beam_size,v_sample_size):
    footPrint = v_beam_size/np.arcsin(v_th)
    print footPrint
    print v_th *180/np.pi
    if footPrint >v_sample_size:
        return v_intensity*v_sample_size/footPrint
    else:
        return v_intensity
for i in np.arange(0.01,np.pi/4.0,np.pi*0.001):
    print footprintCorrection(1, i,0.1,5)
    

"""



        