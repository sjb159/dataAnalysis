'''
Created on 10 Sep 2019

@author: wvx67826
'''

from Tools import Tools 
from numpy import array, full,vstack,hstack,interp,max,minimum
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from matplotlib import ticker
Rd = Tools.ReadWriteData()

Dp = Tools.Output() 
Dp.add_clipboard_to_figures()

def getXYI(data):

    ref = Rd.get_nexus_data("/rdeta//rnormdet")
    fluo = Rd.get_nexus_data("/rdeta/rnormfluo")
    drain = Rd.get_nexus_data("/rdeta/rdrain")
    energy = Rd.get_nexus_meta("/pgm_energy/pgm_energy")
    sx = full((1,len(ref)),Rd.get_nexus_meta("/sx/sx"))
    sy = Rd.get_nexus_data("/sz/sz") 
    alldata = vstack((sx,sy,ref,fluo,drain ))
    print energy,  Rd.get_nexus_meta("/pol/value"), Rd.get_nexus_meta("/sx/sx")
    return alldata
xyData = array([])
folder = "Z://2020//mm24486-1//i10-"
scanNo = range(590391, 590421, 1)



for i, scan in enumerate (scanNo):
        if i == 0: 
            data   = Rd.read_nexus_data(folder, scan)
            xyData = getXYI(data)

        else:
            data   = Rd.read_nexus_data(folder, scan)
            xyData = hstack((xyData,getXYI(data)))

        
plt.figure(1)
plt.suptitle("X-Y Map %i" %scanNo[0])

plt.subplot(131)
plt.title("%s" %Rd.get_nexus_meta("/pgm_energy/pgm_energy"))
plt.xlabel("sx")
plt.ylabel("sz")
plt.tricontourf(xyData[0], xyData[1] , xyData[2],100,interp = 'linear', cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.subplot(132)
plt.title("%s flou" %Rd.get_nexus_meta("/pgm_energy/pgm_energy"))
plt.xlabel("sx")
plt.ylabel("sz")
plt.tricontourf(xyData[0], xyData[1] , xyData[4],100,interp = 'linear', cmap=plt.get_cmap('jet'))
plt.subplot(133)
plt.title("%s drain" %Rd.get_nexus_meta("/pgm_energy/pgm_energy"))
plt.xlabel("sx")
plt.ylabel("sz")
plt.tricontourf(xyData[0], xyData[1] , xyData[3],100,interp = 'linear', cmap=plt.get_cmap('jet'))
plt.colorbar()
plt.show()