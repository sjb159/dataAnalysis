'''
Created on 8 Aug 2018

@author: wvx67826


corr_r() 
    I the R factor for correction between 2 array

'''
from numpy import sum,mean,sqrt,fft,max
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
    def cross_correlation(self,im1,im2):
        image_product = fft.fft2(im1) * fft.fft2(im2).conj()
        cc_image = fft.fftshift(fft.ifft2(image_product))
        return cc_image.real
    def im_dif(self,im1,im2):
        return im1/max(im1)-im2/max(im2)
