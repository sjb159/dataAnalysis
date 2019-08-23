'''
Created on 26 Apr 2019

@author: wvx67826
'''
from Tools import Tools
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.animation as animation
ima= Tools.ImageAnalysis()
rd = Tools.ReadWriteData()

folder = "Z:\\2018\\si19469-1\\i10-"#-pixis-files
filename =  475819   # 350k 537521
imlist = []
imcorr = []
imdiff = []
imcrosscorr = []
picture = []
picture2 = []
picture3 = []
rd.read_nexus_data(folder, filename)
#time = rd.get_nexus_data("/t/t")

imfile = rd.get_nexus_image_filename ()

for i, k in enumerate (imfile[0:-1:1]):        
    temp = "//dc" +k#.split('/dls')[1]
    print temp
    im = Image.open(temp)
    imarray = np.array(im)
    imlist.append(imarray[:,500:1500])#imarray[1180:1260,820:940])
    im.close()
    #imcorr.append(ima.corr_r(imlist[0],imlist[0]))

for i, k in enumerate (imlist):
    imcorr.append(ima.corr_r(imlist[0], k))
    imcrosscorr.append( ima.cross_correlation(imlist[0],k))
    imdiff.append( ima.im_dif(imlist[0],k))
    fig1 = plt.figure(1)
    picture.append((plt.imshow(k,vmin=600,vmax= 6000),))
    fig2 = plt.figure(2)
    picture2.append((plt.imshow(imcrosscorr[i]),))
    fig3 = plt.figure(3)
    #plt.colorbar(mappable, cax, ax)
    picture3.append((plt.imshow(imdiff[i]),))
"""    
    plt.imshow(k)
    plt.show()
    plt.imshow(imcrosscorr)
    plt.show()"""

im_ani = animation.ArtistAnimation(fig1, picture, interval=1000, repeat_delay=3000, blit=True)
im_ani.save('537542.mp4')
im_ani2 = animation.ArtistAnimation(fig2, picture2, interval=1000, repeat_delay=3000, blit=True)
im_ani.save('537542cc.mp4')
im_ani3 = animation.ArtistAnimation(fig3, picture3, interval=1000, repeat_delay=3000, blit=True)
im_ani.save('537542cc.mp4')
"""plt.figure(3)
plt.title("R factor")
plt.plot(imcorr)"""
plt.show()
"""
plt.figure(2)
plt.title("cross-correlation")
plt.plot(imcrosscorr)
#plt.imshow(imarray)
#plt.show()
#plt.imshow(newimarray)
"""
plt.show()