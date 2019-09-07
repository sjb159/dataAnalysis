'''
Created on 27 Sep 2017

@author: wvx67826

Tool box for various calculations

    
'''
from ReadWriteData import *
from Output.Output import *
from AreaDetector.ImageAnalysis import *
from DataReduction.DataCorrection import *


class Tools(AngleToQ, ReadWriteData, XasDataProcess,DataCorrection,ImageAnalysis, Output):
    def __init__(self):
        AngleToQ.__init__(self)
        ReadWriteData.__init__(self)
        XasDataProcess.__init__(self)
        DataCorrection.__init__(self)
        ImageAnalysis.__init__(self)
        Output.__init__(self)
