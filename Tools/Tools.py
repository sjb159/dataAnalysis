'''
Created on 27 Sep 2017

@author: wvx67826

Tool box for various calculations

corr_r()  I the R factor for correction between 2 array

'''
from Data_Reduction.AngleToQ import AngleToQ
from Data_Reduction.ReadData import ReadData
from PIL import Image
import numpy as np

class Tools(AngleToQ,ReadData):
    def __init__(self):
        AngleToQ.__init__(self)
        ReadData.__init__(self)


#correlation coefficient calculation
    def corr_r(self, im1, im2):
        aIm1 = np.mean(im1)
        bIm2 = np.mean(im2)
         
        c_vect = (im1-aIm1)*(im2-bIm2)
        d_vect = (im1-aIm1)**2
        e_vect = (im2-bIm2)**2
        return np.sum(c_vect)/float(np.sqrt(np.sum(d_vect)*np.sum(e_vect)))