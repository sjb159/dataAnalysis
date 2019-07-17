'''
Created on 13 Feb 2019

@author: wvx67826
'''

import time
from Tools import Tools
dr = Tools.ReadWriteData()
folder = "Z:\\2019\\mm22157-1\\"
#folder = "C:\\Users\\wvx67826\\Desktop\\test data\\New folder\\"
output = "Z:\\2019\\mm22157-1\\processing\\"
#output ="C:\\Users\\wvx67826\\Desktop\\test data\\"

#scanNo = range (544874,544875)
scanNo = folder

while True:
    dr.convertNexus2Ascii(scanNo, folder, output)
    time.sleep(36.6666666666)
    