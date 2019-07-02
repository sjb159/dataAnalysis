'''
Created on 13 Feb 2019

@author: wvx67826
'''

import os
from Tools import Tools
dr = Tools.ReadWriteData()
folder = "Z:\\2019\\cm22968-3\\"
output = "C:\\Users\\wvx67826\\Desktop\\test data\\"
#scanNo = range (547000,547035)
scanNo = folder

dr.convertNexus2Ascii(scanNo, folder, output)
