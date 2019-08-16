'''
Created on 16 Aug 2019

@author: wvx67826



'''
from Tools import  Tools  
import matplotlib.pyplot as plt
Rd = Tools.Reduction()
Dp = Tools.Output()

folder = "Z:/2019/cm22968-3/i10-"

lMeta = ["/itc2/itc2","/magj1x/magj1x", "/magj1yins/magj1yins" ]
lData = ["/drain/drain","/fluo1/fluo1", "/macr16/data"]
lScanNo = [558812, 558813]

lFinalDataName, lFinalData , lCpMetaName, lCpMeta, lCnMetaName, lCnMeta =Rd.get_xmcd(folder, lScanNo, lData, lMeta)

plotList = ["/drain/drain norm","/drain/drain corrected","/fluo1/fluo1 norm", "xmcd /drain/drain corrected", "xmcd /fluo1/fluo1 corrected"]
plotList = None
plt.show(Dp.draw_plot(lFinalData[0],  lFinalData,  lFinalDataName, plotList, lCpMeta, lCnMetaName ))
#plt.show(dpdraw_plot( lFinalData[0],  lFinalData,  lFinalDataName, plotList, lCpMeta, lCnMetaName ))

temp = "name"
Rd.write_ascii(temp, lFinalDataName, lFinalData, lCnMetaName, lCnMeta)


junk = input("what you Waiting for ????? Christmas")

