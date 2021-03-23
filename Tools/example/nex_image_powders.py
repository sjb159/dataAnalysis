'''
Created on 16 Sep 2019

@author: wvx67826
'''
from Tools.ReadWriteData import ReadWriteData
from Tools.AreaDetector.ImageAnalysis import ImageAnalysis
import numpy as np
import matplotlib.pyplot as plt
from Tools.Output.Output import Output
op = Output()

op.add_clipboard_to_figures()
ima= ImageAnalysis()
rd = ReadWriteData()

folder = "Z:\\2020\\cm26456-4\\i10-"#-pixis-files
output = "C:\\Users\\wvx67826\\Desktop\\i11_powder_2\\"
start = 617320
end = start +234
print (end)
lfilename =  range(start ,end)   # 612856
tthData = np.array([])
tthSum = np.array([])
averagetthSum = np.array([])
cut = [175,-50]
lowerOverLap = 0
highOverLap = -1
tthRange = 11.5565705#11.5865705
ss = tthRange/2048.0

overlap = int(((tthRange - 10.0)) /ss-cut[0]+cut[1])
print (overlap)



for i,k in enumerate(lfilename):
    try:
        if i ==0:        
            rd.read_nexus_data(folder, k)
            oldtth = rd.get_nexus_meta("/tth/tth")
            tempI =  rd.get_nexus_data("/pimte/data")[0]
            imSum = np.sum(tempI,axis=1)# -np.min(np.sum(tempI,axis=1))
            imAverage =   np.average(tempI,axis=1)# - np.min(np.average(tempI, axis=1))
    
        elif abs(oldtth - rd.get_nexus_meta("/tth/tth")) < 1:
            rd.read_nexus_data(folder, k)
            tempI =  rd.get_nexus_data("/pimte/data")[0]
            imSum = imSum + np.sum(tempI,axis=1) #-np.min(np.sum(tempI,axis=1) ) 
            imAverage =  (imAverage + np.average(tempI, axis=1))#-np.min(np.average(tempI, axis=1)))/2.0     
        
        else:
            lowerth = 90.0-float(oldtth)-tthRange/2.0
            #tthNew = np.arange(lowerth,lowerth+tthRange-ss/2.0,ss)[cut[0]:cut[1]]
            tthSum = np.append(tthSum,np.arange(lowerth,lowerth+tthRange-ss/2.0,ss)[cut[0]:cut[1]])
            
            oldtth = rd.get_nexus_meta("/tth/tth")
            imSum = imSum[cut[0]:cut[1]]
            imAverage = imAverage[cut[0]:cut[1]]
            #imSum = imSum - np.min(imSum)
            if len(tthData)<1:
                tthData = np.append(tthData,imSum)
                averagetthSum  = np.append(averagetthSum,imAverage)
            else:
                
                temp = np.average(tthData[-overlap:highOverLap])/np.average(imSum[lowerOverLap:overlap])
                tthData = np.append(tthData,imSum*temp)
                temp = np.average(averagetthSum [-overlap:highOverLap])/np.average(imAverage[lowerOverLap:overlap])
                averagetthSum  = np.append(averagetthSum ,imAverage *temp)
                
            
            print (len(tthData), len(tthSum), len(averagetthSum))
            tempI =  rd.get_nexus_data("/pimte/data")[0]
            imSum = np.sum(tempI,axis=1) 
            imAverage =   np.average(tempI,axis=1)  
            """           
             plt.figure(1)
            plt.imshow(fullIm)
            plt.figure(2)
            plt.imshow(fullAvIm)
            """
            #plt.show()
        if k == lfilename[-1]:
            lowerth = 90.0-float(oldtth)-tthRange/2.0
            tthSum = np.append(tthSum,np.arange(lowerth,lowerth+tthRange-ss/2.0,ss)[cut[0]:cut[1]])
            
            oldtth = rd.get_nexus_meta("/tth/tth")
            imSum = imSum[cut[0]:cut[1]]
            imAverage = imAverage[cut[0]:cut[1]]
            #imSum = imSum - np.min(imSum)
            if len(tthData)<1:
                tthData = np.append(tthData,imSum)
                averagetthSum =  np.append(averagetthSum,imAverage)
                
            else:
                temp = np.average(tthData[-overlap:])/np.average(imSum[0:overlap])
                tthData = np.append(tthData,imSum*temp)
                temp = np.average(averagetthSum [-overlap:])/np.average(imAverage [0:overlap])
                averagetthSum  = np.append(averagetthSum ,imAverage *temp)
                
            
            print (len(tthData), len(tthSum), len(averagetthSum))
            tempI =  rd.get_nexus_data("/pimte/data")[0]
            imSum = np.sum(tempI,axis=1)
            imAverage =   np.average(tempI,axis=1)
          
    except:
        print ("noooo %i"%k)
            
k = np.vstack([tthSum, tthData, averagetthSum])
meta = int(rd.get_nexus_meta("/pgm_energy/pgm_energy"))
    

plt.figure()
plt.suptitle("Energy = %i" %meta)
plt.subplot(211)
plt.plot(tthSum,tthData)
plt.subplot(212)
plt.plot(tthSum,averagetthSum)

plt.savefig("%s%s_E=%i.jpg" %(output,lfilename[0], meta))


rd.write_ascii("%s%s_E=%i.dat" %(output,lfilename[0], meta), ["tth" "sum", "average counts",], k)


plt.show()

