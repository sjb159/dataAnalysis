'''
Created on 16 Aug 2019

@author: wvx67826

'''
from Tools.DataReduction.Reduction import Reduction
from Tools.Tools import Output
import matplotlib.pyplot as plt


Rd = Reduction()
Dp = Output() 

folder = "Z:/2019/cm22968-3/i10-"

lMeta = ["/itc2/itc2","/magj1x/magj1x", "/magj1yins/magj1yins", "/magj1yins/magj1yins" ]
lData = ["/drain/drain","/fluo1/fluo1", "/macr16/data"]
plotList = ["/drain/drain norm","/drain/drain corrected","/fluo1/fluo1 norm", "/fluo1/fluo1 corrected","xmcd /drain/drain corrected", "xmcd /fluo1/fluo1 corrected"]
plotList =None
lScanNo = [558830, 558831]
cutoffs = [1,7,-12,-8]

lFinalDataName, lFinalData , lCpMetaName, lCpMeta, lCnMetaName, lCnMeta = Rd.get_xmcd(folder, lScanNo, lData, lMeta,cutoffs) 
f1 = Dp.draw_plot(lFinalData[0],  lFinalData,  lFinalDataName, plotList, lCpMeta, lCnMetaName )


lScanNo = [558814, 558815]
lFinalDataName, lFinalData , lMetaName, lMeta = Rd.get_xas(folder, lScanNo[0], lData, lMeta)
f2 = Dp.draw_plot(lFinalData[0],  lFinalData,  lFinalDataName, plotList, lMeta, lMetaName )

temp = "name"
Rd.write_ascii(temp, lFinalDataName, lFinalData, lCnMetaName, lCnMeta)
plt.figure()
f2.savefig("test.jpg")
f1.savefig("test1.jpg")
f2.show()
f1.show()
plt.show()
junk = raw_input("what you Waiting for ????? Christmas???")

plt.close()

