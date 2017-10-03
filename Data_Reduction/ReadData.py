'''
Created on 19 Jul 2017

@author: wvx67826
'''
from astropy.io import ascii
import numpy as np
import re
from astropy.wcs.docstrings import row


class ReadData():
    def __init__(self):
        self.metadata = []
        self.data = []
    
    def read_file(self, filename):
        with  open(filename,'r') as f:
            meta = True
            tMeta = []
            tData = []
            for line in f:
                tMeta.append(line)
                if not meta:
                    tData.append(line) 
                if " &END" in line:
                    meta = False
            self.metadata = tMeta
            self.data = tData
    def get_meta_value(self, metaName):
        for line in self.metadata:
            if metaName in line:
                return line.split("=",1)[1]
    def get_data(self):
        
        return np.genfromtxt(self.data, names = True, delimiter = "\t")
        #return ascii.read(self.data)
