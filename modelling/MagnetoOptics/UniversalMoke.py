'''
Created on 16 Aug 2018

@author: wvx67826

Try to correct polarization
'''
"""
Class to calculate boundary matrix A and A magnetic with arbitrary moment direction 

"""

import timeit
import numpy as np
import matplotlib.pyplot as plt
i = complex(0,1)

class XrayMoke():
    def __init__(self):
        self.mIpol = np.array([])
                              
        self.mIntensity = np.matrix([])
        
    def a_matrix(self, alphaZ, n):
        
        return np.matrix([[       1,         0,         1,       0],
                          [       0,    alphaZ,         0, -alphaZ],
                          [       0,        -n,         0,      -n],
                          [alphaZ*n,         0, -alphaZ*n,       0]])
#A conversion matrix move        
    def a_mag_matrix(self, n ,theta, gamma = 0, phi = 0, q = 0.0): 
        alphaY= self.__alpha_y(theta)
        alphaZ = self.__alpha_z(theta)
        gi = self.__g_i(theta, gamma, phi)
        gr = self.__g_r(theta, gamma, phi)
        return np.matrix([[       1,         0,         1,       0],
                          
                          [ -i/2.0*alphaY**2.0*q*(gi/alphaZ-2.0*np.cos(phi)
                                +2.0*alphaZ/alphaY*np.sin(gamma)*np.sin(phi)),
                            
                            alphaZ+i*alphaY*np.cos(gamma)*np.sin(phi)*q,
                            
                            i/2.0*alphaY**2.0*q*(gr/alphaZ+2.0*np.cos(phi)
                                +2.0*alphaZ/alphaY*np.sin(gamma)*np.sin(phi)),
                            
                            -alphaZ+i*alphaY*np.cos(gamma)*np.sin(phi)*q          ],
                          
                          [  i/2.0*gi*q*n,        -n,        i/2.0*gr*q*n,      -n],
                          
                          [alphaZ*n,    i/2.0*gi*q*n/alphaZ,  -alphaZ*n,       -i/2.0*gr*q*n/alphaZ]])

#calculate the propagation matrix        
    def propagation_matrix(self, n, d, waveLen ,theta, gamma = 0, phi = 0, q =0):
        u = self.__u(n, d, waveLen, theta, phi)
        deltaI = self.__deltaI(n, d, waveLen, theta, gamma, phi, q)
        deltaR = self.__deltaR(n, d, waveLen, theta, gamma, phi, q)
        
        return np.matrix([[          u, u*deltaI,        0,         0],
                          [   -u*deltaI,       u,        0,         0],
                          [           0,       0,    1.0/u,  deltaR/u],
                          [           0,       0, deltaR/u,     1.0/u]])
        
    def m_a_d_inva(self,n, d, waveLen, theta, gamma, phi, q):
        mA = self.a_mag_matrix(n, theta, gamma, phi, q)
        minvA =np.linalg.inv(mA)
        mD = self.propagation_matrix(n, d, waveLen, theta, gamma, phi, q)
        return np.dot(np.dot(mA,mD),minvA)
    
    def sum_m_a_d_inva(self,k, n, theta, gamma, phi, q, d, waveLen):
        
        if k == 0:
            theta = np.arcsin(n[0]/n[k]*np.sin(theta))
            self.mAPi = self.a_mag_matrix(n[k], theta, gamma[k], phi[k], q[k])*self.mPi
            return self.sum_m_a_d_inva(k+1, n, theta, gamma, phi, q, d, waveLen)
        if k == len(n)-1:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return self.a_mag_matrix(n[k], theta1, gamma[k], phi[k], q[k])
        
        else:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return np.dot(self.m_a_d_inva(n[k], d[k], waveLen, theta1, gamma[k], phi[k], q[k]),self.sum_m_a_d_inva(
                                         k+1, n, theta1, gamma, phi, q, d, waveLen))
            
    def cal_intensity_mD(self, n, theta, gamma, phi, q, d, waveLen):
        mM = self.get_m_m(0, n, theta, gamma, phi, q, d, waveLen)
        mG = mM[0:2,0:2]
        mGInv = np.linalg.inv(mG)
        mI = mM[2:4,0:2]
        mIGInv = np.dot(mI,mGInv)
        mIntensity =mIGInv# np.dot(mIGInv,np.conj(mIGInv))
        self.mIntensity = mIntensity
        return mIntensity
    
    def get_intensity(self, inPol, outPol):
        self.set_ipol(inPol)
        mFinI = np.multiply(self.mIntensity, self.mIpol)
        if outPol == "Si+Pi":
            """finI = np.dot(mFinI[0,0],np.conj(mFinI[0,0]))+np.dot(mFinI[0,1],np.conj(mFinI[0,1]))+ np.dot(
                          mFinI[1,0],np.conj(mFinI[1,0]))+np.dot(mFinI[1,1],np.conj(mFinI[1,1]))"""
            """finI = np.dot(mFinI[0,0]+mFinI[0,1],np.conj(mFinI[0,0]+mFinI[1,0]))+np.dot(
                          mFinI[0,1]+mFinI[1,1],np.conj(mFinI[0,1]+mFinI[1,1]))"""
            finI= np.dot(mFinI[0,0]+mFinI[1,0],np.conj(mFinI[0,0]+mFinI[1,0])) + np.dot(
                         mFinI[0,1]+mFinI[1,1],np.conj(mFinI[0,1]+mFinI[1,1]))
            return np.absolute(finI)
        if outPol == "Si":
            #finI = np.dot(mFinI[0,0],np.conj(mFinI[0,0]))+np.dot(mFinI[1,0],np.conj(mFinI[1,0]))
            #finI = mFinI[0,0]+mFinI[1,0]
            finI = np.dot(mFinI[0,0]+mFinI[1,0],np.conj(mFinI[0,0]+mFinI[1,0]))
            return np.absolute(finI)# np.absolute(np.dot(finI,np.conj(finI)))
        if outPol == "Pi":
            #finI = np.dot(mFinI[0,1],np.conj(mFinI[0,1]))+np.dot(mFinI[1,1],np.conj(mFinI[1,1]))
            finI = np.dot(mFinI[0,1]+mFinI[1,1],np.conj(mFinI[0,1]+mFinI[1,1]))
            #finI = (mFinI[0,1]+mFinI[1,1])  
            return np.absolute(finI)#np.absolute(np.dot(finI,np.conj(finI)))
        
    def get_m_m(self,k, n, theta, gamma, phi, q, d, waveLen):
        if k == 0:
            theta = np.arcsin((n[0]+q[0])/(n[k]+q[k])*np.sin(theta))
            #theta = np.arcsin(n[0]/n[k]*np.sin(theta))
            temp = self.a_mag_matrix(n[k], theta, gamma[k], phi[k], q[k])
            return np.dot(np.linalg.inv(temp),self.get_m_m(k+1, n, theta, gamma, phi, q, d, waveLen))
        if k == len(n)-1:
            theta1 = np.arcsin(((n[k-1]+q[k-1])/(n[k]+q[k]))*np.sin(theta))
            #theta1 = np.arcsin(n[k-1]/n[k]*np.sin(theta))
            return self.a_mag_matrix(n[k], theta1, gamma[k], phi[k], q[k])
        
        else:
            theta1 = np.arcsin(((n[k-1]+q[k-1])/(n[k]+q[k]))*np.sin(theta))
            #theta1 = np.arcsin(n[k-1]/n[k]*np.sin(theta))
            return self.m_a_d_inva(n[k], d[k], waveLen, theta1, gamma[k], phi[k], q[k])*self.get_m_m(
                                         k+1, n, theta1, gamma, phi, q, d, waveLen)
        
            
    def set_ipol(self,pol):
        ipol = {"Si"         : np.matrix([[1.0],
                                             [0.0]]),
                "Pi"            : np.matrix([[0.0],
                                             [1.0]]),
                "LC"     : np.matrix([[0.707106781186547],
                                             [0.707106781186547*i]]),
                "RC"    : np.matrix([[0.707106781186547],
                                             [-0.707106781186547*i]])
                }
        self.mIpol = ipol[pol] 
        return self.mIpol 
    

    def set_opol(self,pol = "S&P"):
        self.set_opol(pol)
        
    def __g_i(self, theta, gamma, phi):
        return np.cos(phi)*self.__alpha_z(theta) + self.__alpha_y(theta)*np.sin(gamma)*np.sin(phi)
    def __g_r(self, theta, gamma, phi):
        return -np.cos(phi)*self.__alpha_z(theta) + self.__alpha_y(theta)*np.sin(gamma)*np.sin(phi)
    def __alpha_z(self, theta):
        return np.cos(theta)
    def __alpha_y(self, theta):
        return np.sin(theta)
    def __u(self, n, d, waveLen, theta, phi):
        return np.exp(-i*2.0*np.pi/waveLen*n*self.__alpha_z(theta)*d )
    def __deltaI(self,n, d, waveLen, theta, gamma, phi, q):
        return np.pi/waveLen*n*d*q/self.__alpha_z(theta)*self.__g_i(theta, gamma, phi)
    def __deltaR(self,n, d, waveLen, theta, gamma, phi, q):
        return np.pi/waveLen*n*d*q/self.__alpha_z(theta)*self.__g_r(theta, gamma, phi)       
