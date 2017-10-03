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


scan = range(413061,413087) #413113
RD = ReadData()
Tbox = Tools()
temperature = []
maxVal = []
dSum = []
image = []
cor = []
firstImage = Image.open("Z:/data/2017/cm16783-4/" +str(scan[0]) + "-pixis-files/00001.tif")
dataFile = 'data/Tscan_CP_Rh_image_cor_FeRH(AU)-1.dat'
f = open(dataFile, 'w+')
f.write("Temperature \t Sum \t  Maxval \t R \n")

for i in scan:
    filename = "Z:/data/2017/cm16783-4/i10-" + str(i) +".dat"
    Tbox.read_file(filename)
    """
    temperature = (Tbox.get_data()["Channel1Temp"])
    maxVal = (Tbox.get_data()["maxval"])
    dSum =(Tbox.get_data()["sum"])
    """
    imageFolder = "Z:/data/2017/cm16783-4/" +str(i) +"-pixis-files/"
    tempIFolder = sorted(os.listdir(imageFolder))
    k= 0
    for iFile in tempIFolder:
        iFileName = imageFolder + iFile
        currentImage = Image.open(iFileName)
        #image.append(currentImage)     
        tempCor = Tbox.corr_r(firstImage, currentImage)
        tempT = (Tbox.get_data()["Channel1Temp"][k])
        tempMaxval =(Tbox.get_data()["maxval"][k])
        tempSum =  (Tbox.get_data()["sum"][k])
        temperature.append(tempT )
        maxVal.append(tempMaxval )
        dSum.append(tempSum)
        cor.append(tempCor)
        k = k+1
        f.write("%g" %tempT + "\t %g"  %tempSum+ "\t %g"  %tempMaxval+ "\t %g"  %tempCor + "\n")
    
    print i, tempT, time.asctime()

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