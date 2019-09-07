'''
Created on 20 Aug 2019

@author: wvx67826
'''
from Tools import  Tools  
from Tools.DataReduction.Reduction import Reduction
import matplotlib.pyplot as plt
Rd = Reduction()
Dp = Tools.Output() 

folder = "Z:/2019/cm22968-3/i10-"

lMeta = ["/ls340/Channel0Temp" ]
lData = ["/rdeta/rdet","/rdeta/rfluo", "/rdeta/rmirror"]
plotList = ["/rdeta/rdet norm","/rdeta/rdet corrected"]
lScanNo = [558812, 558813]
cutoffs = [1,10,"REF",0]
outPutFolder = "C://All my tools//java-mars//pyworkspace//Experiments//Experiment//NSM0I06//data//ref//"
plt.figure()


for i,scanNo in enumerate ( range(559112,559173,2)):
    Rd.get_ref(folder, scanNo, lData, lMeta, cutoffs)
    if i == 0: 
        lFinalDataName1st, lFinalData1st , lCpMetaName1st, lCpMeta1st = Rd.get_ref(folder, scanNo, lData, lMeta, cutoffs) 
    else:
        lFinalDataName, lFinalData , lCpMetaName, lCpMeta = Rd.get_ref(folder, scanNo, lData, lMeta, cutoffs) 





f1 =Dp.draw_plot(lFinalData[0],  lFinalData,  lFinalDataName, plotList, lCpMeta, lCpMetaName, logY = True )
fileName = "%s%i_%s%i" %(outPutFolder,scanNo,lCpMetaName[1].split("/")[-1],lCpMeta[1])
f1.savefig("%s.jpg" %(fileName))
    
Rd.write_ascii(fileName+".dat", lFinalDataName, lFinalData, lCpMetaName, lCpMeta)
f1.show()
plt.show()