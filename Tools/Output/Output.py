'''
Created on 16 Aug 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics


class Output():
    def __init__(self):
        pass
    
    def draw_plot(self, x, lY, lYName, lYNameUse = None, lMeta = None, lMetaName=None, logY = False):
    
        if lYNameUse == None: lYNameUse = lYName
        myDpi = 100
        screenWidth = GetSystemMetrics(0)
        screenHeight = GetSystemMetrics(1)

        fig = plt.figure(figsize=(screenWidth/myDpi, screenHeight/myDpi), dpi=myDpi)
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
            for m,l in enumerate(lNameUsed):
                plt.plot(x[m] ,lY[l])
                if logY:
                    plt.semilogy()
        plt.draw()
        #fig =  plt.gcf()    
        plt.close()
        return fig
        