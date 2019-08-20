'''
Created on 27 Sep 2017

@author: wvx67826

Tool box for various calculations

    
'''
from ReadWriteData import *
from DataReduction.DataCorrection import *
from AreaDetector.ImageAnalysis import *
from DataReduction.Reduction import *
from Output.Output import *
class Tools(AngleToQ, ReadWriteData, XasDataProcess,DataCorrection,ImageAnalysis, Reduction, Output):
    def __init__(self):
        AngleToQ.__init__(self)
        ReadWriteData.__init__(self)
        XasDataProcess.__init__(self)
        DataCorrection.__init__(self)
        ImageAnalysis.__init__(self)
        Reduction.__init_(self)
        Output.__init__(self)