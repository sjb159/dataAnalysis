'''
Created on 8 Aug 2018

@author: wvx67826

XasDataProcess:

xas_corr(self, data1, data1lowCutOff = 0, data1highCutOff = 15, data1EndLowCutOff = -10, data1EndHighCutOff = -1)
    subtract background (average) before edge and normalise data to 1 after edge.

xmcd(self,data1,data2)
    return data1-data2
    
xmcd_ratio(self, data1, data2):
    return (data1-data2)/(data1+data2)    

AngleToQ:
conver th tth to qz and qx

DataCorrection:

norm_data(self,data1,data2)  
    normalise data 


'''
from numpy import average, cos, sin, deg2rad, pi, interp, max,min,append
from numpy.polynomial.polynomial import polyval, polyfit 
from scipy.optimize import curve_fit

class XasDataProcess():
    def __init__(self):
        pass
    
    def xas_corr(self, data1 , data1lowCutOff = 1, linFit = False,
                  data1highCutOff = 10, data1EndLowCutOff = -12, data1EndHighCutOff = -2):
        """
        data1lowcutOff is the number of lowest intensity point to skip
        
        data1highCutOff is the total number of lowest intensity point to average over
        
        ata1EndLowCutOff = -10, data1EndHighCutOff = -1
        
        are the range of data points that will average over where the rest of the data normlised to.
        """
        
        #This subtract pre-edge and normalise to pro-edge
        k = DataCorrection()
        if (linFit == True):
            dataXStart = range (0, data1highCutOff-data1lowCutOff)
            mc =k.poly_fit(dataXStart, data1[data1lowCutOff:data1highCutOff])
            xStart = range(len(data1))
            cStart=  k.gen_poly(xStart, mc)
            corBackData = data1- cStart  
            return corBackData/average(corBackData[data1EndLowCutOff:data1EndHighCutOff])      
        else:
            tempData1 = list(data1)
            
            tempData1.sort()
            
            
            corBackData = (data1- average(tempData1[data1lowCutOff:data1highCutOff]))
            tempData2 = list(corBackData[data1EndLowCutOff: data1EndHighCutOff])
            tempData2.sort()

            return corBackData /average(tempData2[1:-1])
           
    
    def xref_corr(self, data1 , data1lowCutOff = 1,
                  data1highCutOff = 10, norm = "ref", notUsed = None):
        #This subtract pre-edge and normalise to pro-edge
       
        tempData1 = list(data1)
        tempData1.sort()
        corData = (data1) #- average(tempData1[data1lowCutOff:data1highCutOff]))
        if norm == "REF": 
            return corData /corData[0] 
        elif norm == "MAX": 
            print ("Max")
            return corData/ max(corData)  
        elif norm == None: return corData
        else: 
            "warning: unnormlised data" 
            return corData
        
        
    def xmcd(self,data1,data2):
        return data1-data2
    def xmcd_w_corr(self, x1, x2, data1, data2):
        return self.xmcd(data1, interp(x1, x2, data2))
    def xmcd_ratio(self, data1, data2):
        return (data1-data2)/(data1+data2)    
    def xmcd_ratio_w_corr(self, x1, x2, data1, data2):
        return self.xmcd_ratio(data1,interp(x1,x2, data2))
        

class AngleToQ():
    def __init__(self):
        pass
    def cal_qz(self, tth, th, energy,alpha = 0):
        return 2.0*pi/self.cal_wave(energy)*(sin(deg2rad((tth-th)))+sin(deg2rad(th)))
    def cal_qx(self,tth, th,  energy,alpha = 0):
        return 2.0*pi/self.cal_wave(energy)*(cos(deg2rad(alpha))*cos(deg2rad((tth-th)))-cos(deg2rad(th)))
    def cal_qy(self,tth, th,  energy,alpha = 0):
        return 2.0*pi/self.cal_wave(energy)*(cos(deg2rad((tth-th)))*sin(deg2rad(alpha)))
    def cal_wave(self, energy):
        return 12400.0/energy
    
    
class DataCorrection():
    def __init__(self):
        pass        
    def norm_data(self,data1,data2):
        return data1/data2
    def poly_fit(self,dataX,dataY, deg = 1):
        return polyfit(dataX, dataY, deg)
    def gen_poly(self, x, mc):
        return polyval(x, mc)
    def drain_ref(self,theta, absLen, eeLen, c):
        return (absLen/sin(theta))/((absLen/sin(theta))+1.0/eeLen) + c
    def fit_drain_ref(self,dataX,dataY):
        return curve_fit(self.drain_ref,dataX,dataY)
    #take x-y data and two region fit the region with straight line and subtract it
    def sub_Straight_Line(self,dataX,dataY,fitRegion):
        dataY = dataY - min(dataY)
        dataXStart = dataX[fitRegion[0]:fitRegion[1]] 
        dataXStart = append(dataXStart,dataX[fitRegion[2]:fitRegion[3]])
        dataYStart = dataY[fitRegion[0]:fitRegion[1]] 
        dataYStart = append(dataYStart,dataY[fitRegion[2]:fitRegion[3]])
        mc =self.poly_fit(dataXStart, dataYStart)
        xStart = dataX
        cStart=  self.gen_poly(xStart, mc)
        return dataY- cStart  
    
    
    
    
    