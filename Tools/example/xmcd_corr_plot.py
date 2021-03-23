'''
Created on 13 Sep 2019

@author: wvx67826
'''
'''
Created on 16 Aug 2019

@author: wvx67826

'''
from Tools.DataReduction.Reduction import Reduction
from Tools.Output.Output import Output
import matplotlib.pyplot as plt
import numpy as np


Rd = Reduction()
Dp = Output() 
Dp.add_clipboard_to_figures()


def whichSample(x,z):
    if z >-0.5 and z<0.6:
        if x >-7.1 and x<-6:
            return "ZnFe2Ox"
        if x >-10.7 and x<-8:
            return "NiZnFeOx"
        if x >-15 and x<-11:
            return "NiZnFe4Ox"
    if z < -1.0:
        if x >-8 and x < -6: 
            return "Ce-R"
        if x <-10.1:
            return "Ce_p"
    if z >1:
        if x <-7.1 and x>-9:
            return "Cu_Ce_R" 
        if x <-9.1 and x>-11:
            return "Cu_Ce_p" 
        if x <-12:
            return "Cu_ce_c"  
            
folder = "Z:\\2020\\cm26456-1\\i10-"
output = "C:\All my tools\java-mars\pyworkspace\Experiments\Experiment\LYSMO\powder\\"
lMeta = ["/sx/sx", "/sz/sz", "/emecy2/emecy2"]
lData = ["/mcsr17_g/data","/mcsr18_g/data", "/mcsr19_g/data", "/mcsr16_g/data"]
plotList = ["/mcsr17_g/data corrected", "/mcsr18_g/data corrected", "xmcd /mcsr17_g/data corrected", "xmcd /mcsr18_g/data corrected",
            "/mcsr19_g/data corrected", "xmcd /mcsr19_g/data corrected"]

for scanNo in range (597913,597915,2):#597978
    plt.figure()
    lScanNo = [scanNo, scanNo+1]
    cutoffs = [10,20,-20,-10]
    
    lFinalDataName, lFinalData , lCpMetaName, lCpMeta, lCnMetaName, lCnMeta = Rd.get_xmcd_old(folder, lScanNo, lData, lMeta,cutoffs) 
   
    lCpMeta = np.append(lCpMeta, 0.1)
    sampleName = whichSample(lCpMeta[1],lCpMeta[2])
    tempName = "/%s/%s" %(sampleName,sampleName)
    lCpMetaName = np.append(lCpMetaName, tempName)
    
    temp = int(((len(lFinalData)-3)/2))-1
    print(temp)
    f1 = Dp.draw_plot([lFinalData[0],lFinalData[temp]],  lFinalData,  lFinalDataName, plotList )
    f1.show()
    
    """    if lCnMeta[3]<1:
        fileName = output + "%s_%s_HMax.dat" %(sampleName,lCpMeta[0])
    elif lCnMeta[3]>17:
        fileName = output + "%s_Hmin.dat" %(sampleName,lCpMeta[0])"""
    #Rd.write_ascii(fileName, lFinalDataName, lFinalData, lCnMetaName, lCnMeta)
    
    #fileName =  fileName[:fileName.find(sampleName)] + "\\fig\\"+ fileName[fileName.find(sampleName):]
    #f1.savefig("%s.jpg" %(fileName[:-4]))
    #print lFinalDataName
    #plt.close()
#temp = "name"
#


