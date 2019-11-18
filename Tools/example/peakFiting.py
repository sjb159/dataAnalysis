'''
Created on 1 Oct 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
import numpy as np
from Tools import Tools
import matplotlib.pyplot as plt
from astropy.table.operations import hstack

def line(x,mc):
    return mc[0]*x+0.009#+mc[1]+0.09

dr = Tools.ReadWriteData()
dc = Tools.DataCorrection()

folder = "S://Science//I10//LYSMO//data//"


#lscan = [186287,186309,186325,186341,186360,186378,186400,186422,186443,186465,186481]
lscan = [186315,186331,186366,186384,186406,186428,186449,186471,186487]

plt.figure()
for i in lscan:
    print i
    dr.read_file("%s%s.dat" %(folder,i))
    temperature  = dr.get_meta_value("temp2")
    tempData = dr.get_data()
    temptemperature = []
    th = tempData["value"]
    intensity = tempData ["ifioft"]
    #intensity = tempData ["ca62sr"]
    plt.plot(th,intensity,label = temperature )

plt.legend()
plt.show()