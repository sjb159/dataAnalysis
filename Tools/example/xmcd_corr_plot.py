'''
Created on 13 Sep 2019

@author: wvx67826
'''
'''
Created on 16 Aug 2019

@author: wvx67826

'''
from Tools.DataReduction.Reduction import Reduction
from Tools.Tools import Output
import matplotlib.pyplot as plt


Rd = Reduction()
Dp = Output() 

folder = "Z:\\2019\\mm19994-1\\i10-"

lMeta = ["/itc2/itc2" ]
lData = ["/mcsr17_g/data","/mcsr18_g/data", "/mcsr16_g/data"]
plotList = ["/mcsr17_g/data corrected", "/mcsr18_g/data corrected", "xmcd /mcsr17_g/data corrected", "xmcd /mcsr18_g/data corrected" ]
lScanNo = [570702, 570703]
cutoffs = [1,7,-20,-10]




lFinalDataName, lFinalData , lCpMetaName, lCpMeta, lCnMetaName, lCnMeta = Rd.get_xmcd(folder, lScanNo, lData, lMeta,cutoffs) 
f1 = Dp.draw_plot([lFinalData[0],lFinalData[8]],  lFinalData,  lFinalDataName, plotList, lCpMeta, lCnMetaName )


temp = "name"
Rd.write_ascii(temp, lFinalDataName, lFinalData, lCnMetaName, lCnMeta)
plt.figure()
f1.savefig("test1.jpg")
f1.show()
plt.show()
plt.close()

