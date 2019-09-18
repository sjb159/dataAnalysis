'''
Created on 16 Sep 2019

@author: wvx67826
'''
from Tools import Tools
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.animation as animation
ima= Tools.ImageAnalysis()
rd = Tools.ReadWriteData()

folder = "Z:\\2019\\nr24677-1\\i10-"#-pixis-files
output = "C:\All my tools\java-mars\pyworkspace\Experiments\Experiment\powder\data\\"
lfilename =  range(566066,566546)   # 563001
tthData = np.array([])
tthSum = np.array([])
newtthSum = np.array([])
cut = [75,-75]

for i,k in enumerate(lfilename):
    try:
        if i ==0:        
            rd.read_nexus_data(folder, k)
            oldtth = rd.get_nexus_meta("/tth/tth")
            imSum =  np.average(rd.get_nexus_data("/pimte/data")[0], axis = 1)
            
        elif (oldtth - rd.get_nexus_meta("/tth/tth")) < 1:
            rd.read_nexus_data(folder, k)
            imSum = (imSum + np.average(rd.get_nexus_data("/pimte/data")[0], axis = 1))/2.0
        else:
            
            lowerth = 90.0-float(oldtth)-11.5692705/2.0
            tthSum = np.append(tthSum,np.arange(lowerth,lowerth+11.5692705-0.00564905786,0.00564905786)[cut[0]:cut[1]])
            
            oldtth = rd.get_nexus_meta("/tth/tth")
            imSum = imSum[cut[0]:cut[1]]
            #imSum = imSum - np.min(imSum)
            if len(tthData)<1:
                tthData = np.append(tthData,imSum)
            else:
                temp = np.average(tthData[-126:])/np.average(imSum[0:126])
                print temp
                tthData = np.append(tthData,imSum*temp)
                
            print len(tthData), len(tthSum)
            imSum = np.average(rd.get_nexus_data("/pimte/data")[0], axis = 1)
    except:
        print k
        
k = np.vstack([tthSum, tthData])
meta = int(rd.get_nexus_meta("/pgm_energy/pgm_energy"))
    

plt.figure()
plt.plot(tthSum,tthData)
plt.savefig("%s%s_E=%i.jpg" %(output,lfilename[0], meta))
plt.show()

rd.write_ascii("%s%s_E=%i.dat" %(output,lfilename[0], meta), ["tth", "counts"], k)

