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
from numpy import average, cos, sin, deg2rad, pi
from numpy.polynomial.polynomial import polyval, polyfit 
from scipy.optimize import curve_fit
class XasDataProcess():
    def __init__(self):
        pass
    
    def xas_corr(self, data1 , data1lowCutOff = 10, linFit = False,
                  data1highCutOff = 30, data1EndLowCutOff = -10, data1EndHighCutOff = -1):
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
            corBackData = (data1 - average(data1[data1lowCutOff:data1highCutOff]))
            return corBackData /average(corBackData[data1EndLowCutOff:data1EndHighCutOff])
           
    
    def xref_corr(self, data1 , data1lowCutOff = 10, linFit = False,
                  data1highCutOff = 30, data1EndLowCutOff = -10, data1EndHighCutOff = -1):
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
            corBackData = (data1)
            return corBackData /average(corBackData[data1EndLowCutOff:data1EndHighCutOff])

            
    def xmcd(self,data1,data2):
        return data1-data2
    
    def xmcd_ratio(self, data1, data2):
        return (data1-data2)/(data1+data2)    

class AngleToQ():
    def __init__(self):
        pass
    def cal_qz(self, tth, th, energy):
        return 2.0*pi/self.cal_wave(energy)*(sin(deg2rad((tth-th)))+sin(deg2rad(th)))
    def cal_qx(self,tth, th, energy):
        return 2.0*pi/self.cal_wave(energy)*(cos(deg2rad((tth-th)))-cos(deg2rad(th)))
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
    