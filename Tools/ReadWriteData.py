'''
Created on 19 Jul 2017

@author: wvx67826

Read and write data. 

For ascii format:
Read_file(filename)
    
get_meta_value(self, metaName):

def get_data(self):
return ascii formate data

Nexus format:

read_nexus_data(self,folder, filename):

get_nexus_meta(self, subBranch, nData = 0, mainBranch ="/entry1/before_scan"):
retrun nexus meta data 

get_nexus_data(self, subBranch, nData = 0, mainBranch ="/entry1/instrument" ):

get_scan_type(self, subBranch = "/scan_command", nData = 0, mainBranch ="/entry1" ):
get list of data 

write_ascii(self, filename, names, data)
    write data to file
    file name = output file name
    names are the name list for the column data
    list of data 
    example:
        result = []
        result.append(energy)
        result.append(xas1)
        result.append(xas2)
        result.append(xmcd)
        result.append(xmcd_ratio)
        k = ["energy", "Cp", "cn","xmcd","xmcd_ratio"]
        tools.write_ascii("test.dat",k,result)

'''
import numpy as np
import h5py    # HDF5 support
from PIL import Image

class ReadWriteData():
    def __init__(self):
        self.metadata = []
        self.data = []
        self.nexusData = []
        
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

    def read_nexus_data(self,folder, filename):
        self.nexusData = h5py.File(str(folder)+ str(filename) + '.nxs',  "r")
        return self.nexusData
    
    def get_nexus_meta(self, subBranch, nData = 0, mainBranch ="/entry1/before_scan"):
        subBranch = "/"+subBranch+"/"+subBranch
        if nData == 0:
            nData = self.nexusData
        return nData[mainBranch + subBranch].value
    
    def get_nexus_data(self, subBranch, nData = 0, mainBranch ="/entry1/instrument" ):
        if nData == 0:
            nData = self.nexusData       
        return nData[mainBranch + subBranch].value
    def get_scan_type(self, subBranch = "/scan_command", nData = 0, mainBranch ="/entry1" ):
        if nData == 0:
            nData = self.nexusData
        temp = nData[mainBranch + subBranch].value.split()[1]          
        return temp

    def write_ascii(self, filename, names, data):
        f = open(filename, 'w+')
        for i in names:
            f.write("%s \t" %i)
        f.write("\n" )
        for j in range (0,len(data[0])):
            for k in range (0,len(data)):
                f.write("%.8g \t" %data[k][j])
               
            f.write("\n" )
        f.close()
    
    def get_nexus_tiff(self, subBranch = "/pixistiff/image_data", nData = 0, mainBranch ="/entry1" ):
        if nData == 0:
            nData = self.nexusData
        temp = "//data" +nData[mainBranch + subBranch].value[0].split('/dls')[1]
        im = Image.open(temp)
        return im
        