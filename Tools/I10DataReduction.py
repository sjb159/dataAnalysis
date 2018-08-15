'''
Created on 10 Aug 2018

@author: wvx67826

A few function to correct I10 data, plot and save them to file.


xas_pair_processing( self, data, folder, outFileName = "No output", metaOutFileName =[""], 
                            nextPol = 1,showPlot = False, linFit = False, pol1= "circ_pos", pol2 = "circ_neg", mirrorDrain = "16",
                            detectors =[17,18,19], xasStartAverage = [10,40], xasEndAverage = [-120,-105]):


'''
from Tools import Tools
import matplotlib.pyplot as plt
from numpy import interp
class I10DataReduction():
    def __init__(self):
        self.tools = Tools()
    def xas_pair_processing( self, data, folder, outFileName = "No output", metaOutFileName =[""], 
                            nextPol = 1, showPlot = False, linFit = False, pol1= "idu_circ_pos", pol2 = "idu_circ_neg", mirrorDrain = "16",
                            detectors =[17,18,19], xasStartAverage = [10,40], xasEndAverage = [-120,-105]):
        
        for edata in data:
            result = []        
            dataName = []
            detType = "xas"
#reversing the order of loading the data if the first scan is circ neg or lin ver
            if pol1 =="idu_circ_neg" or pol1 == "idu_lin_ver":
                pol = "/egy_g_%s_energy/pgm_energy" %pol2
                temp = self.__loadCorrectedData(edata+nextPol, folder,pol,mirrorDrain, detectors, detType,
                                                linFit, xasStartAverage,xasEndAverage)
                result = temp[0]
                dataName = (temp[1])
                pol = "/egy_g_idu_%s_energy/pgm_energy" %pol1
                temp = self.__loadCorrectedData(edata, folder, pol, mirrorDrain, detectors,  detType,
                                    linFit, xasStartAverage,xasEndAverage)
                result = result + temp[0]
                dataName = dataName + temp[1]
                x2 = temp[0][0]

            else: 
                pol = "/egy_g_%s_energy/pgm_energy" %pol1
                temp = self.__loadCorrectedData(edata, folder,pol,mirrorDrain, detectors, detType,
                                                linFit, xasStartAverage,xasEndAverage)
                result = temp[0]
                dataName = (temp[1])
                pol = "/egy_g_%s_energy/pgm_energy" %pol2
                temp = self.__loadCorrectedData(edata+nextPol, folder, pol, mirrorDrain, detectors,  detType,
                                    linFit, xasStartAverage,xasEndAverage)
                result = result + temp[0]
                dataName = dataName + temp[1]
                x2 = temp[0][0]

            for k in range(0,len(detectors)):
                result.append( self.tools.xmcd(result[3+k*2], interp(result[0], x2, result[5+len(detectors)*2+k*2])))
                dataName = dataName +["xmcd det%.i " %(detectors[k])]
                result.append( self.tools.xmcd_ratio(result[3+k*2], interp(result[0], x2, result[5+len(detectors)*2+k*2])))
                dataName = dataName +["xmcd ratio det%.i " %(detectors[k])]
            
            if showPlot:
                self.__plot_data(result,detectors,detType)
                
            if outFileName != "No output":
                self.__saveData(metaOutFileName, edata,outFileName, dataName, result)

            
    def refl_pair_processing( self, data, folder, outFileName = "No output", metaOutFileName =[""], 
                            pol1 = "idu_circ_pos", nextPol = 1,showPlot = False, linFit = False, axis= "th", mirrorDrain = "16",
                            detectors =["refl","18","19"], xasStartAverage = [-50,-1], xasEndAverage = [0,-1]):
        for edata in data:
            result = []        
            dataName = []  
            detType = "refl" 
            pol ="/%s/%s" %(axis, axis)          
#reversing the order of loading the data if the first scan is circ neg or lin ver
            if (pol1 =="idu_circ_neg" or pol1 == "idu_lin_ver"):
                temp = self.__loadCorrectedData(edata, folder,pol,mirrorDrain, detectors,detType,
                                                linFit, xasStartAverage,xasEndAverage)
                result = temp[0]
                dataName = (temp[1])
                temp = self.__loadCorrectedData(edata+nextPol, folder, pol,mirrorDrain, detectors,detType,
                                    linFit, xasStartAverage,xasEndAverage)
                result = result + temp[0]
                dataName = dataName + temp[1]
                x2 = temp[0][0]
            else:
                temp = self.__loadCorrectedData(edata+nextPol, folder,pol,mirrorDrain, detectors,detType,
                                                linFit, xasStartAverage,xasEndAverage)
                result = temp[0]
                dataName = (temp[1])
                temp = self.__loadCorrectedData(edata, folder, pol,mirrorDrain, detectors,detType,
                                    linFit, xasStartAverage,xasEndAverage)
                result = result + temp[0]
                dataName = dataName + temp[1]
                x2 = temp[0][0]
        
        
            for k in range(0,len(detectors)):
                
                result.append(self.tools.xmcd(result[3+k*2], interp(result[0], x2, result[5+len(detectors)*2+k*2])))
                dataName = dataName +["xmcd det%s " %(detectors[k])]
                result.append(self.tools.xmcd_ratio(result[3+k*2], interp(result[0], x2, result[5+len(detectors)*2+k*2])))
                dataName = dataName +["xmcd ratio det%s " %(detectors[k])]
            if showPlot:
                self.__plot_data(result,detectors,detType)
                
            if outFileName != "No output":
                self.__saveData(metaOutFileName, edata,outFileName, dataName, result)

            
        
    def meta_name_string(self, meta_name):
        full_meta_name = ""
        for i in meta_name:
            full_meta_name = full_meta_name + "_%s_%.4g_" %(i, self.tools.get_nexus_meta(i))
        return full_meta_name
            
    def __plot_data(self,data, detectors, detectorType):
        for i in range(len(detectors)) :
            plt.figure(1)
            subplotset = "13%s" %(i+1)
            plt.ylabel("Det%s" %detectors[i])
            plt.subplot(subplotset)
            if detectorType == "refl":
                plt.semilogy(data[0],data[3+i*2])
            else:
                plt.plot(data[0],data[3+i*2])
            plt.plot(data[2+len(detectors)*2],data[5+len(detectors)*2+i*2])
            plt.figure(2)
            subplotset = "13%s" %(i+1)
            plt.subplot(subplotset)
            plt.ylabel("XMCD%s" %detectors[i])
            plt.plot(data[0],data[len(data)-len(detectors)*2+i*2])
        plt.show()
    def __saveData(self, metaOutFileName, edata,outFileName, dataName, result):
            if metaOutFileName [0] != "":
                fName = outFileName +"escan_%s%s.dat" %(edata,self.meta_name_string(metaOutFileName))
            else:
                fName = outFileName +"escan_%s.dat" %edata 
            self.tools.write_ascii(fName,dataName,result)
        
    def __loadCorrectedData(self, data, folder,pol1,mirrorDrain, detectors, detType, linFit, xasStartAverage,xasEndAverage):
        result = []        
        dataName = []
        self.tools.read_nexus_data(folder, data)
        x1 = self.tools.get_nexus_data("%s" %pol1)
        result.append(x1)
        dataName = dataName + ["%s" %pol1]
        result.append(self.tools.get_nexus_data(self.__detectorType(detType, mirrorDrain)))
        
        dataName = dataName +["%s det%s" %(pol1, mirrorDrain)]
        for k in detectors:
            result.append(self.tools.norm_data(self.tools.get_nexus_data(self.__detectorType(detType, k)),
                                          self.tools.get_nexus_data(self.__detectorType(detType, mirrorDrain))))
            dataName = dataName +["%s norm det%s " %(pol1,k)]
            
            result.append(self.tools.xas_corr(result[-1],linFit = linFit, data1lowCutOff = xasStartAverage[0],
                                              data1highCutOff = xasStartAverage[1],
                                              data1EndLowCutOff = xasEndAverage[0],
                                              data1EndHighCutOff = xasEndAverage[1]))
            dataName = dataName +["%s corr det%s " %(pol1,k)]
    
        return  result, dataName
    def __detectorType(self, detType, channel):
        if channel == "refl":
            return "/refl/refl"
        if detType == "xas":
            return "/mcsr%s_g/data" %channel
        if detType == "refl":
            return "/macr%s/data" %channel
        
