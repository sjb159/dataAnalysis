'''
Created on 13 Feb 2019

@author: wvx67826

convert everything in nexus to ascii e.g. back to the old format
'''

import time, os, re
from Tools import Tools
dr = Tools.ReadWriteData()
folder = "Z:\\2019\\cm22968-3\\"
output = "C:\Users\wvx67826\Desktop\LSMO\\FeNiZiOx\\"

scanNo = folder
scanNo  = range(558855,558857)
dr.convert_nexus_ascii(scanNo, folder, output) # scanNo takes either a list or a folder if it is folder it will run everything inside the folder


# This part is an infinite loop to keep checking for the latest scan
newScanNo = None
lastScanNo = None
timeOut = 0
while timeOut < 24*3600:
    if newScanNo == lastScanNo:
        print lastScanNo
        lastScanNo = int(re.split("-|.hdf" ,sorted(os.listdir(folder))[-5])[1])
        time.sleep(66.6666666)
        timeOut = timeOut+66.66666666
        newScanNo = int(re.split("-|.hdf" ,sorted(os.listdir(folder))[-5])[1])
    else:
        dr.convertNexus2Ascii(range(newScanNo,lastScanNo-2,-1), folder, output)
        lastScanNo = newScanNo
        timeOut = 0

    
    