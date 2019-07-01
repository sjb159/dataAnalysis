'''
Created on 13 Feb 2019

@author: wvx67826
'''

import os
from Tools import Tools

dr = Tools.ReadWriteData()

def convertData(filename):
    
    filen = folder+ "i10-"
    if filename[0:4] == "i10-":
        filename = filename[4:-4] #cutting the file name to fit the read nexus
    #print filen
    dr.read_nexus_data(filen,filename)
    fulloutputname = "%s%s.dat" %(output,filename)
    dr.nexus2ascii(fulloutputname)
    try:
        dr.read_nexus_data(filen,filename)
        fulloutputname = "%s%s.dat" %(output,filename)
        dr.nexus2ascii(fulloutputname)
        print filename
    except:
        print "failed %s" %filename

folder = "C:\Users\\wvx67826\\Desktop\\test data\\New folder\\"
output = "C:\\Users\\wvx67826\\Desktop\\test data\\"
#scanNo = range (525683,525690)
scanNo = folder

if isinstance(scanNo, (list,)):
    for filename in scanNo:
        convertData(str(filename) )

if scanNo == folder:
    for filename in sorted(os.listdir(scanNo)):
        tempFilename = "%s%s.dat" %(output,filename[4:-4])  
        exist = os.path.isfile(tempFilename)
        
        if exist and os.path.getmtime(tempFilename)>os.path.getmtime(folder+"%s" %filename):
            print tempFilename
            pass #' do nothing'
        else:
            if filename[-4:] == ".nxs": #filter out everything that is not data
                convertData(filename) 




