'''
Created on 10 Aug 2018

@author: wvx67826
'''
from Tools import Tools
import matplotlib.pyplot as plt
class I10DataReduction():
    def __init__(self):
        self.tools = Tools()
    def xas_pair_processing( self, data, folder, outFileName = "No output", metaOutFileName =[""],  nextPol = 1,showPlot = False, pol1= "circ_pos", pol2 = "circ_neg", mirrorDrain = "16",
                            detectors =[17,18,19],  xasEndAverage = [-120,-105]):
        for edata in data:
            
            result = []        
            dataName = []
            self.tools.read_nexus_data(folder, edata)
            result.append(self.tools.get_nexus_data("/egy_g_idu_%s_energy/pgm_energy" %pol1))
            dataName = dataName + ["%s energy" %pol1]
            result.append(self.tools.get_nexus_data("/mcsr%s_g/data" %mirrorDrain))
            
            dataName = dataName +["%s det%s" %(pol1, mirrorDrain)]
            for k in detectors:
                result.append(self.tools.norm_data(self.tools.get_nexus_data("/mcsr"+str(k) + "_g/data"),
                                              self.tools.get_nexus_data("/mcsr%s_g/data" %mirrorDrain)))
                dataName = dataName +["%s norm det%.i " %(pol1,k)]
                
                result.append(self.tools.xas_corr(result[-1], data1EndLowCutOff = xasEndAverage[0],
                                              data1EndHighCutOff = xasEndAverage[1]))
                dataName = dataName +["%s corr det%.i " %(pol1,k)]
        
            self.tools.read_nexus_data(folder, edata+1)
            
            result.append(self.tools.get_nexus_data("/egy_g_idu_%s_energy/pgm_energy" %pol2))
            dataName = dataName +["%s energy" %pol2]
            
            result.append(self.tools.get_nexus_data("/mcsr%s_g/data" %mirrorDrain))
            dataName = dataName +["%s det%s" %(pol2,mirrorDrain)]
            
            for k in detectors:
                result.append(self.tools.norm_data(self.tools.get_nexus_data("/mcsr"+str(k) + "_g/data"),
                                              self.tools.get_nexus_data("/mcsr%s_g/data" %mirrorDrain)))
                dataName = dataName +["%s norm det%i " %(pol2,k)]
                
                result.append(self.tools.xas_corr(result[-1], data1EndLowCutOff = xasEndAverage[0],
                                              data1EndHighCutOff = xasEndAverage[1]))
                dataName = dataName +["%s corr det%i " %(pol2,k)]
                
            for k in range(0,len(detectors)):
                result.append( self.tools.xmcd(result[3+k*2], result[5+len(detectors)*2+k*2]))
                dataName = dataName +["xmcd det%.i " %(detectors[k])]
                result.append( self.tools.xmcd_ratio(result[3+k*2], result[5+len(detectors)*2+k*2]))
                dataName = dataName +["xmcd ratio det%.i " %(detectors[k])]
            
            if showPlot:
                self.__plot_xmcd_data(result,detectors)
                
            
            if outFileName != "No output":
                if metaOutFileName [0] != "":
                    fName = outFileName +"escan_%s%s.dat" %(edata,self.meta_name_string(metaOutFileName))
                else:
                    fName = outFileName +"escan_%s.dat" %edata 
                self.tools.write_ascii(fName,dataName,result)
            
    
    def meta_name_string(self, meta_name):
        full_meta_name = ""
        for i in meta_name:
            full_meta_name = full_meta_name + "_%s_%.3g_" %(i, self.tools.get_nexus_meta(i))
        return full_meta_name
            
    def __plot_xmcd_data(self,data, detectors):
        for i in range(len(detectors)) :
            plt.figure(1)
            subplotset = "13%s" %(i+1)
            plt.subplot(subplotset)
            plt.ylabel("Det%s" %detectors[i])
            plt.plot(data[0],data[3+i*2])
            plt.plot(data[2+len(detectors)*2],data[5+len(detectors)*2+i*2])
            plt.figure(2)
            subplotset = "13%s" %(i+1)
            plt.subplot(subplotset)
            plt.ylabel("XMCD%s" %detectors[i])
            plt.plot(data[0],data[len(data)-len(detectors)*2+i*2])
        plt.show()
    
        
        
        
