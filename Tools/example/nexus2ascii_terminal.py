'''
Created on 13 Feb 2019

@author: wvx67826

convert everything in nexus to ascii e.g. back to the old format
'''

import time,os,sys, re
sys.path.append("/home/wvx67826/Desktop/dataAnalysis-master/")
from Tools import Tools
dr = Tools.ReadWriteData()
folder = sys.argv[1]
output = sys.argv[2]
print sys.argv[1], sys.argv[2]
scanNo = folder
dr.convertNexus2Ascii(scanNo, folder, output) # scanNo takes either a list or a folder if it is folder it will run everything inside the folder


# This part is an infinit loop to keep checking for the latest scan
newScanNo = None
lastScanNo = None
timeOut = 0
while timeOut < 24*3600:
    if newScanNo == lastScanNo:
        lastScanNo = int(re.split("-|.hdf" ,sorted(os.listdir(folder))[-5])[1])
        time.sleep(66.6666666)
        timeOut = timeOut+66.66666666
        newScanNo = int(re.split("-|.hdf" ,sorted(os.listdir(folder))[-5])[1])
    else:
        dr.convertNexus2Ascii(range(newScanNo,lastScanNo-2,-1), folder, output)
        lastScanNo = newScanNo
        timeOut = 0

    
    
