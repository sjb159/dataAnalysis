'''
Created on 27 Sep 2017

@author: wvx67826

Tool box for various calculations

corr_r() 
    I the R factor for correction between 2 array

norm_data(self,data1,data2)  
    normalise data 

xas_corr(self, data1, data1lowCutOff = 0, data1highCutOff = 15, data1EndLowCutOff = -10, data1EndHighCutOff = -1)
    subtract background (average) before edge and normalise data to 1 after edge.

xmcd(self,data1,data2)
    return data1-data2
    
xmcd_ratio(self, data1, data2):
    return (data1-data2)/(data1+data2)    
    
write_ascii(self, filename, names, data)
    write data to file
    file name = output file name
    names are the name list for the column data
    list of data 
    example:
        result = []
        result.append(energy)
        result.append(xas1)
        result.append(xas2)
        result.append(xmcd)
        result.append(xmcd_ratio)
        k = ["energy", "Cp", "cn","xmcd","xmcd_ratio"]
        tools.write_ascii("test.dat",k,result)
    
'''
from ReadWriteData import ReadWriteData
from DataReduction.DataCorrection import *
import numpy as np

class Tools(AngleToQ, ReadWriteData, XasDataProcess,DataCorrection):
    def __init__(self):
        AngleToQ.__init__(self)
        ReadWriteData.__init__(self)
        XasDataProcess.__init__(self)
        DataCorrection.__init__(self)


#correlation coefficient calculation
    def corr_r(self, im1, im2):
        aIm1 = np.mean(im1)
        bIm2 = np.mean(im2)
        
        c_vect = (im1-aIm1)*(im2-bIm2)
        d_vect = (im1-aIm1)**2
        e_vect = (im2-bIm2)**2
        return np.sum(c_vect)/float(np.sqrt(np.sum(d_vect)*np.sum(e_vect)))
    
