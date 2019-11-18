'''
Created on 17 Sep 2019

@author: wvx67826
'''
from Tools import Tools
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
ima= Tools.ImageAnalysis()
rd = Tools.ReadWriteData()

folder = "Z:\\2019\\nr24677-1\\i10-"#-pixis-files
output = "C:\All my tools\java-mars\pyworkspace\Experiments\Experiment\old\powder\\data\\"
lfilename =  range(562155,562168 )   # 563001
tthData = np.array([])
tthSum = np.array([])
tthAvData = np.array([])
cut = [100,-100]
tthRange = 11.5865705
ss = tthRange/2048.0
overlap = int(((tthRange - 10.0)) /ss-cut[0]*2)

for i,k in enumerate(lfilename):
    rd.read_nexus_data(folder, k)   
    imfile = rd.get_nexus_image_filename (subBranch = "/pimtetiff/image_data")
    oldtth = rd.get_nexus_meta("/tth/tth")
    for i, k in enumerate (imfile[0:-1:1]):        
        temp = "//dc" +k#.split('/dls')[1]
        #print temp
        im = Image.open(temp)
        imarray = np.array(im)
        if (90-oldtth)>65:
            imarray = imarray/5.0
        imarray = imarray -np.min(imarray)
        if i ==0 :
            partTthData = np.sum(imarray , axis = 1)
            partTthAvData = np.average(imarray , axis = 1)
        else:
            partTthData =  (partTthData + np.sum(imarray , axis = 1))/2.0
            partTthAvData =  (partTthAvData + np.average(imarray , axis = 1))/2.0
        im.close()
    
    lowerth = 90.0-float(oldtth)-tthRange/2.0
    tthSum = np.append(tthSum,np.arange(lowerth,lowerth+tthRange-ss/2.0,ss)[cut[0]:cut[1]])
    imSum = partTthData[cut[0]:cut[1]]
    imAv = partTthAvData[cut[0]:cut[1]]
    #imSum = imSum - np.min(imSum)
    if len(tthData)<1:
        tthData = np.append(tthData,imSum)
        tthAvData = np.append(tthAvData, imAv)
    else:
        temp = np.average(tthData[-overlap:])/np.average(imSum[0:overlap])
        tthData = np.append(tthData,imSum*temp)
        temp = np.average(tthAvData[-overlap:])/np.average(imAv[0:overlap])
        tthAvData = np.append(tthAvData,imAv*temp)        
    print len(tthData), len(tthSum), len(tthAvData)    
    
k = np.vstack([tthSum, tthData, tthAvData])
meta = int(rd.get_nexus_meta("/pgm_energy/pgm_energy"))
    

plt.figure()
plt.subplot(211)
plt.plot(tthSum,tthData)
plt.subplot(212)
plt.plot(tthSum,tthAvData)
plt.savefig("%s%s_E=%i.jpg" %(output,lfilename[0], meta))
plt.show()

rd.write_ascii("%s%s_E=%i.dat" %(output,lfilename[0], meta), ["tth", "sum", "average"], k)


    