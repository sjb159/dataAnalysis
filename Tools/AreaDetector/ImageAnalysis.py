'''
Created on 8 Aug 2018

@author: wvx67826


corr_r() 
    I the R factor for correction between 2 array

'''
from numpy import sum,mean,sqrt
class ImageAnalysis():
    def __init__(self):
        pass
    
    def corr_r(self, im1, im2):
        aIm1 = mean(im1)
        bIm2 = mean(im2)
        
        c_vect = (im1-aIm1)*(im2-bIm2)
        d_vect = (im1-aIm1)**2
        e_vect = (im2-bIm2)**2
        return sum(c_vect)/float(sqrt(sum(d_vect)*sum(e_vect)))
        
