'''
Created on 15 Aug 2019

@author: wvx67826



'''
from Tools.ReadWriteData import ReadWriteData
from Tools.DataReduction.DataCorrection import XasDataProcess
from numpy import vstack, hstack
class Reduction(ReadWriteData, XasDataProcess):
    def __init__(self):
        ReadWriteData.__init__(self)
        XasDataProcess.__init__(self)
        
    def scans_info(self, folder, scanNo, lInfo = ["/pgm_energy/pgm_energy"]):
        """
        provide scan number together with user requested meta data

        
        """
        scans_info_list = [scanNo]
        
        self.read_nexus_data(folder, scanNo)
        scanType = self.get_scan_type()
        scans_info_list.append(scanType)
        for i in lInfo:
            scans_info_list.append(self.get_nexus_meta(i)) 
        
        return scans_info_list

    def get_reduced_data(self, folder, scanNo, lScanableName, lMetaName):
        """
        return the requested meta and data in a list
        
        
        return lMeta, lData
        """
        lData = []
        lMeta = []
        
        self.read_nexus_data(folder, scanNo)
        
        for i in lScanableName:
            lData.append(self.get_nexus_data(i))
        for i in lMetaName:
            lMeta.append(self.get_nexus_meta(i))
                             
        return lMeta, lData
    
    
    def get_ref(self,folder, scanNo, lScanableName = None, lMetaName = None, cutoffs = [2,10,"REF",None]):
        """
        Get all none energy data and either normised to first data point with:
        REF or maximum with MAX and None
        """
        scanType = self.scans_info(folder, scanNo)[1]
        return self.__corr_xas_data__(folder, scanNo, lScanableName, lMetaName, scanType, cutoffs)
 
    def get_xas(self,folder, scanNo, lScanableName = None, lMetaName = None, cutoffs = [2,7,-7,-2]):
        
        scanType = self.scans_info(folder, scanNo)[1]
        if "energy" in scanType:
            return self.__corr_xas_data__(folder, scanNo, lScanableName, lMetaName, scanType, cutoffs)
        else: print "Not energy scan"
        # return lDataName, lData, lMetaName, lMeta
    
    def get_xmcd(self, folder, lScanPair, lScanableName = None, lMetaName = None, cutoffs = [2,7,-7,-2]):
        
        for scan in lScanPair:
            scanType = self.scans_info(folder, scan)[1]
            if "pos" in scanType:
                lCpDataName, lCpData, lCpMetaName, lCpMeta = self.__corr_xas_data__(folder, scan, lScanableName, lMetaName, scanType, cutoffs)
            elif "neg" in scanType:
                lCnDataName, lCnData, lCnMetaName, lCnMeta = self.__corr_xas_data__(folder, scan, lScanableName, lMetaName, scanType, cutoffs)
            else: print "not circular energy scan"
        lResult = []
        lResultName = []
        for i,j in enumerate(lCpDataName[len(lScanableName)+1:]):
            
            lResult.append( self.xmcd_w_corr(lCpData[0], lCnData[0], lCpData[i + len(lScanableName)+1], lCnData[i + len(lScanableName)+1]))
            lResultName.append("xmcd %s" %j)
        
        
        lFinalDataName = hstack((lCpDataName, lCnDataName, lResultName))
        lFinalData     = vstack((lCpData, lCnData, lResult))
       
        return lFinalDataName, lFinalData , lCpMetaName, lCpMeta, lCnMetaName, lCnMeta
        
        
    def __corr_xas_data__(self,folder, scan, lScanableName, lMetaName, scanType, cutoffs):
        lDataName = list(lScanableName)
        lDataName.insert(0, "/%s/%s" %(scanType,scanType))
        lMeta, lData = self.get_reduced_data(folder, scan, lDataName , lMetaName)
        monitor = lData[-1]
        for i,j in enumerate (lScanableName[:-1]):
            lData.append(lData[i+1]/monitor)
            lDataName.append("%s norm" %j)
            # the only different beteen the two is xref normalise to the first data point.
            if "energy" in scanType:
                lData.append(self.xas_corr(lData[-1], data1lowCutOff = cutoffs[0],
                                                  data1highCutOff = cutoffs[1],
                                                   data1EndLowCutOff = cutoffs[2],
                                                    data1EndHighCutOff = cutoffs[3]))
            else:
                lData.append(self.xref_corr(lData[-1] , data1lowCutOff = cutoffs[0],
                                             data1highCutOff = cutoffs[1], norm = cutoffs[2],
                                             notUsed = cutoffs[3]))

            lDataName.append("%s corrected" %j)
        ltempMeta = list(lMeta)
        ltempMetaName = list(lMetaName)
        ltempMeta.insert(0, scan)
        ltempMetaName.insert(0, "scanNo")
        return   lDataName, lData, ltempMetaName, ltempMeta
