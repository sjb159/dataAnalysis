'''
Created on 13 Feb 2019

@author: wvx67826

convert everything in nexus to ascii e.g. back to the old format
'''

import time, os, re
from Tools.ReadWriteData import ReadWriteData
dr = ReadWriteData()
folder = "D:\\Dropbox_RHUL\\Dropbox (Royal Holloway)\\Nano-Electronics Group RHUL\\Beamtime\\Resonant X-ray Scattering (05_2021)\\03_Data from I10\\Data_nxs\\"
output = "E:\\data\\"

scanNo = folder
#scanNo  = range(637224,637227,1)
dr.convert_nexus_ascii(scanNo, folder, output) # scanNo takes either a list or a folder if it is folder it will run everything inside the folder


# This part is an infinite loop to keep checking for the latest scan
newScanNo = None
lastScanNo = None
timeOut = 0
while timeOut < 24*3600:
    if newScanNo == lastScanNo:
        lastScanNo = int(re.split("-|.nxs" ,sorted(os.listdir(folder))[-5])[1])
        print (lastScanNo)
        time.sleep(66.6666666)
        timeOut = timeOut+66.66666666
        newScanNo = int(re.split("-|.nxs" ,sorted(os.listdir(folder))[-5])[1])
    else:
        dr.convert_nexus_ascii(range(newScanNo,lastScanNo-2,-1), folder, output)
        lastScanNo = newScanNo
        timeOut = 0

