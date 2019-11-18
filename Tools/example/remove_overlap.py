'''
Created on 30 Oct 2019

@author: wvx67826
'''
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
from Tools import Tools
import os
rwd = Tools.ReadWriteData()
folder = "C:\All my tools\java-mars\pyworkspace\Experiments\Experiment\old\powder\Paper Uploads\\"
filename = sorted(os.listdir(folder))
for k in filename:
    fullpath = folder +k
    print fullpath
    data = ascii.read("%s%s"%(folder, k))
    newTthSum = np.array([])
    newAverage = np.array([])
    newCounts = np.array([])
     
    tthsum = np.array(data["tth"])[::-1]
    average = np.array(data["sum"])[::-1]
    counts  = np.array(data["counts"])[::-1]
    
    for i, j in enumerate(tthsum):
        if i == 0:
            oldtth = j
            newTthSum = np.append(newTthSum,j)
            newAverage = np.append(newAverage, average[i])
            newCounts = np.append(newCounts, counts[i])
    
        elif oldtth > j:
            oldtth = j
            newTthSum = np.append(newTthSum,j)
            newAverage = np.append(newAverage, average[i])
            newCounts = np.append(newCounts, counts[i])
    name = ["Tth","Average","Counts"]
    output = np.vstack([newTthSum[::-1],newAverage[::-1],newCounts[::-1]])
    outputfolder = folder +"rmOver"+k
    rwd.write_ascii(outputfolder, name, output)
    print output
    plt.plot(output[0],output[1])
    plt.show()