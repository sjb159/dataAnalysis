'''
Created on 23 Aug 2019

@author: wvx67826
'''
from Tools.Tools import ReadWriteData
import matplotlib.pylab as plt
import matplotlib.image as mpimg
import numpy as np
import time

start = time.time()

Rd = ReadWriteData()

folder = "Z:\\2019\\cm22968-3\\i10-"
scanNo = "559008"

Rd.read_nexus_data(folder, scanNo)
arImage = Rd.get_nexus_data("/pimte/data")
k = Rd.get_nexus_data("/hkl_ccd/k")
print time.time()-start

for i,im in enumerate(arImage):
    plt.figure()
    
    plt.imshow(im, vmin=200, vmax=1000, label = k[i])
    plt.title(k[i])
    plt.colorbar()
    plt.show()