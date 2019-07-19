'''
Created on 13 Feb 2019

@author: wvx67826

convert everything in nexus to ascii e.g. back to the old format
'''

import time,os
from Tools import Tools
dr = Tools.ReadWriteData()
folder = "Z:\\2019\\mm22157-1\\"
output = "Z:\\2019\\mm22157-1\\processing\\"

scanNo = folder
dr.convertNexus2Ascii(scanNo, folder, output) # scanNo takes either a list or a folder if it is folder it will run everything inside the folder


# This part is an infinit loop to keep checking for the latest scan
newScanNo = 0
lastScanNo = 0
timeOut = 0
while timeOut < 24*3600:
    if newScanNo == lastScanNo:
        lastScanNo = int(sorted(os.listdir(folder))[-5][4:-4])
        time.sleep(66.6666666)
        timeOut = timeOut+66.66666666
        newScanNo = int(sorted(os.listdir(folder))[-5][4:-4])
    else:
        dr.convertNexus2Ascii(range(newScanNo,lastScanNo-2,-1), folder, output)
        lastScanNo = newScanNo
        timeOut = 0

    
    