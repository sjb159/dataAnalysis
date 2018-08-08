'''
Created on 8 Aug 2018

@author: wvx67826
'''
from numpy import average, cos, sin, deg2rad, pi
class XasDataProcess():
    def __init__(self):
        pass
    
    def xas_corr(self, data1, data1lowCutOff = 0, data1highCutOff = 15, data1EndLowCutOff = -10, data1EndHighCutOff = -1):
        #This subtract pre-edge and normalise to pro-edge
        return (data1 - average(data1[data1lowCutOff:data1highCutOff]))/average(data1[data1EndLowCutOff:data1EndHighCutOff])
    
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
