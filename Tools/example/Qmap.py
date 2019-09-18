'''
Created on 10 Sep 2019

@author: wvx67826
'''

from Tools.Tools import ReadWriteData
from Tools.Tools import AngleToQ
from numpy import array, full,vstack,hstack,interp,max,minimum
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from matplotlib import ticker
Rd = ReadWriteData()
A2Q = AngleToQ()


def getQandIntensity(data):
    
    th  = Rd.get_nexus_data("/th/th")
    ref = Rd.get_nexus_data("/rdeta/rnormdet")
    ref = abs(ref-min(ref)+1e-7)/max(ref)
    fluo = Rd.get_nexus_data("/rdeta/rnormfluo")
    energy = Rd.get_nexus_meta("/pgm_energy/pgm_energy")
    tth = full((1,len(ref)),Rd.get_nexus_meta("/tth/tth"))
    qz = A2Q.cal_qz(tth, th, energy, 0) 
    qx = A2Q.cal_qx(tth, th, energy, 0) 
    allData = vstack((qz,qx,ref,fluo))
    print energy,  Rd.get_nexus_meta("/pol/value"), Rd.get_nexus_meta("/tth/tth")
    return allData
pcData = array([])
ncData = array([])
folder = "Z://2019//mm21411-1//i10-"
scanNo = range(561392, 561419, 2)
#scanNo = range(561420, 561447, 2)
#scanNo = range(561448, 561475, 2)
#scanNo = range(561476, 561503, 2)


for i, scan in enumerate (scanNo):
        if i == 0: 
            data   = Rd.read_nexus_data(folder, scan)
            pcData = getQandIntensity(data)
            data   = Rd.read_nexus_data(folder, scan+1)
            ncData = getQandIntensity(data)
        else:
            data   = Rd.read_nexus_data(folder, scan)
            pcData = hstack((pcData,getQandIntensity(data)))
            data   = Rd.read_nexus_data(folder, scan+1)
            ncData = hstack((ncData,getQandIntensity(data)))
        
plt.figure(1)
plt.suptitle("Pos Field 28mT to 0 mT E = 852")
xmcd= ncData[2] #interp(pcData[1],ncData[1], ncData[2])
#xmcd = interp(pcData[0],ncData[0], xmcd)
#xmcd = interp(pcData[1],ncData[1], xmcd)
plt.subplot(221)
plt.title("PC")
plt.xlabel("Qz")
plt.ylabel("Qx")
plt.tricontourf(pcData[0], pcData[1] , pcData[2],30,interp = 'linear',locator=ticker.LogLocator(), cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.subplot(222)
plt.title("NC")
plt.xlabel("Qz")
plt.ylabel("Qx")
plt.tricontourf(ncData[0], ncData[1] , ncData[2],30,interp = 'linear',locator=ticker.LogLocator(), cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.subplot(223)
plt.title("XMCD")
plt.xlabel("Qz")
plt.ylabel("Qx")
plt.tricontourf(pcData[0], pcData[1] , pcData[2]-xmcd,30,interp = 'linear', cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.subplot(224)
plt.title("XMCD ratio")
plt.xlabel("Qz")
plt.ylabel("Qx")
plt.tricontourf(pcData[0], pcData[1] , (pcData[2]-xmcd)/(pcData[2]+xmcd),30,interp = 'linear', cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.show()


