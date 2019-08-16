'''
Created on 16 Aug 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
class Output():
    def __init__(self):
        pass
    
    def draw_plot(self, x, lY, lYName, lYNameUse = None, lMeta = None, lMetaName=None):
        if lYNameUse == None: lYNameUse = lYName
        p1 = plt.figure()
        if (lMetaName != None and lMeta != None):
            title = ""
            for i,j in enumerate (lMetaName):
                title = title + "%s=%.2f " %(j.split("/")[-1], lMeta[i])
            plt.suptitle(title)
        
        noOfPlot = len(lYNameUse)
        for i, j in enumerate(lYNameUse):
            plt.subplot(round(noOfPlot/2.0),2, i +1)
            plt.title(j)
            lNameUsed = [k for k,checkName in enumerate(lYName) if checkName == j]
            for l in lNameUsed:
                
                plt.plot(x ,lY[l])
                        
        return p1
        