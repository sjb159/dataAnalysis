'''
Created on 26 Sep 2017

@author: wvx67826
'''
from PIL import Image
import matplotlib.pyplot as plt
from Tools.Tools import Tools
import os
from Data_Reduction.ReadData import ReadData
import time
from multiprocessing import Process, Lock,freeze_support
def get_result(Tbox, firstImage, currentImage,k, lo):
    lo.acquire()
    try:
        tempCor = Tbox.corr_r(firstImage, currentImage)
        tempT = (Tbox.get_data()["Channel1Temp"][k])
        tempMaxval =(Tbox.get_data()["maxval"][k])
        tempSum =  (Tbox.get_data()["sum"][k])
        temperature.append(tempT )
        maxVal.append(tempMaxval )
        dSum.append(tempSum)
        cor.append(tempCor)
    finally:
        lo.release()
        


scan = range(412921,413022) #413113
RD = ReadData()
Tbox = Tools()
temperature = []
maxVal = []
dSum = []
image = []
cor = []
p = 0
firstImage = Image.open("Z:/data/2017/cm16783-4/" +str(scan[0]) + "-pixis-files/00001.tif")
dataFile = 'data/Tscan_CP_image_cor_FeRH(AU).dat'
f = open(dataFile, 'w+')
f.write("Temperature \t Sum \t  Maxval \t R \n")

for i in scan:
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    Tbox.read_file(filename)
    imageFolder = "Z:/data/2017/cm16783-4/" +str(i) +"-pixis-files/"
    tempIFolder = sorted(os.listdir(imageFolder))
    k= 0
    for iFile in tempIFolder:
        iFileName = imageFolder + iFile
        currentImage = Image.open(iFileName)
        #image.append(currentImage)     
        lock = Lock()
        freeze_support()
        p =Process(target=get_result, args=(Tbox, firstImage,currentImage, k, lock)).start()
        k = k+1
        
        
    #f.write("%g" %tempT + "\t %g"  %tempSum+ "\t %g"  %tempMaxval+ "\t %g"  %tempCor + "\n")
    p.join()
    print i, time.asctime()

f.close()
plt.figure(1)
plt.subplot(221)
plt.title('T V S')
plt.plot(temperature,dSum)
plt.subplot(222)
plt.title('T V Max ')
plt.plot(temperature,maxVal)
plt.subplot(223)
plt.title('T vs R')
plt.plot(temperature, cor)

plt.show()

    
#plt.imshow(cor)

#plt.show()