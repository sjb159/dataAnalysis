'''
Created on 27 Sep 2017

@author: wvx67826

Tool box for various calculations

    
'''
from ReadWriteData import ReadWriteData
from DataReduction.DataCorrection import *
from AreaDetector.ImageAnalysis import *
class Tools(AngleToQ, ReadWriteData, XasDataProcess,DataCorrection,ImageAnalysis):
    def __init__(self):
        AngleToQ.__init__(self)
        ReadWriteData.__init__(self)
        XasDataProcess.__init__(self)
        DataCorrection.__init__(self)
        ImageAnalysis.__init__(self)