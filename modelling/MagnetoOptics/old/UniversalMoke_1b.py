'''
Created on 16 Aug 2018

@author: wvx67826
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
        #print mFinI
        #raw_input()
        if outPol == "Si+Pi":
            finI =  (mFinI[0,0]+mFinI[0,1]+mFinI[1,0]+mFinI[1,1])
            return np.absolute(np.dot(finI,np.conj(finI)))
        if outPol == "Si":
            finI = mFinI[0,0] + mFinI[1,0]
            return np.absolute(np.dot(finI,np.conj(finI)))
        if outPol == "Pi":
            finI = mFinI[0,1]+mFinI[1,1]    
            return np.absolute(np.dot(finI,np.conj(finI)))
        
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
                                             [-i*0.707106781186547]])
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
    
xrMoke = XrayMoke()


#reflective index N = 1-gamma +iBeta

n  = np.array([1.0, 1.0+3.48600e-3+5.6168e-3*i, 1.0+3.48600e-3+5.6168e-3*i, 1.00-1.65e-3+2.9911e-4*i])
d = np.array([0, 200, 20, 200])
q = np.array([0, 5.31087e-5+1.32985e-4*i, 0, 0])#""
#q = np.array([0, 0, 0, 0])#""
aPhi =   np.array([0, 90., 90.0, 0])
aGamma = np.array([0, 90., 90.,0])

theta =75
theta = np.deg2rad(theta)
aPhi = np.deg2rad(aPhi)
aGamma  = np.deg2rad(aGamma)



angle = np.array([])
intensity1 = np.array([])
intensity2 = np.array([])
intensity3 = np.array([])
intensity4 = np.array([])
intensity5 = np.array([])
intensity6 = np.array([])
waveLen = 12.4/0.777198
start_time1 = timeit.default_timer()
for gamma1 in np.arange (90,0, -0.1):
    
    #aPhi[1] = np.deg2rad(gamma1)
    #aPhi[2] = np.deg2rad(gamma1)
    theta = np.deg2rad(gamma1)
    Qz = 90.-gamma1#4.0*np.pi/waveLen*np.sin(np.deg2rad(90.-gamma1))   
    angle =  np.append(angle,Qz)     
    aGamma = np.array([0, -90, 0,0])
    aGamma  = np.deg2rad(aGamma)
    xrMoke.cal_intensity_mD(n, theta, aGamma, aPhi, q, d, waveLen)
    intensity1 = np.append(intensity1,xrMoke.get_intensity("Si", "Si"))
    #xrMoke.cal_intensity_mD(n, theta, aGamma, aPhi, q, d, waveLen)
    #intensity2 = np.append(intensity2,xrMoke.get_intensity("Si", "Si+Pi"))
    aGamma = np.array([0, 90., 0.,0])
    
    aGamma  = np.deg2rad(aGamma)
    xrMoke.cal_intensity_mD(n, theta, aGamma, aPhi, q, d, waveLen)
    intensity3 = np.append(intensity3,xrMoke.get_intensity("Si", "Pi"))
    #intensity4 = np.append(intensity4,xrMoke.get_intensity("Pi", "Si+Pi"))
    intensity5 = (intensity1- intensity3)/(intensity1 + intensity3)
    
    """intensity5 = np.append(intensity5,(xrMoke.get_intensity("LC", "Si+Pi")
                                       -xrMoke.get_intensity("RC", "Si+Pi")))"""
    """intensity4 = np.append(intensity1,xrMoke.get_intensity("Pi", "Si"))
    intensity5 = np.append(intensity1,xrMoke.get_intensity("LC", "Si+Pi"))
    intensity6 = np.append(intensity1,xrMoke.get_intensity("RC", "Si+Pi"))"""
    
elapsed = timeit.default_timer() - start_time1
print elapsed

plt.figure(1)
plt.semilogy()
plt.plot(angle, intensity1)
"""plt.figure(2)
plt.plot(angle, intensity2)"""
#plt.figure(3)
plt.plot(angle, intensity3)
"""plt.figure(4)
plt.plot(angle, intensity4)"""
plt.figure(5)
plt.plot(angle, intensity5)
#plt.plot(angle, intensity4)
#plt.semilogy()
plt.show()

"""
xrMoke = XrayMoke()
theta = 22
phi = 90
gamma = 90
n1 = 1
n2 = 1.3
theta = np.deg2rad(theta)
gamma = np.deg2rad(gamma)
phi = np.deg2rad(phi)
angle = np.array([])
intensity = np.array([])
for gamma1 in np.arange (89.9, 0.1, -0.1):
    
    theta = np.deg2rad(gamma1)
    angle = np.append(angle,90-gamma1)
    mA1 = xrMoke.a_mag_matrix(n1, theta, gamma = gamma, phi = phi,q = 0)
    mP1 = sp.Matrix([[1],
                    [i],
                    [rc1],
                    [rc2]])
    theta = np.arcsin(n1/n2*np.sin(theta))
    print np.rad2deg(theta)
    mA2 = xrMoke.a_mag_matrix(n2, theta, gamma = gamma,phi = phi, q= 0.0)
    mP2 = sp.Matrix([[tc1],
                    [tc2],
                    [0],
                    [0]])
    
    mA1P1 =  (mA1)*mP1
    mA2P2 = mA2*mP2
    
    k = mA1P1 - mA2P2
    mZero = sp.Matrix([[0],
                       [0],
                       [0],
                       [0]])
    c= k.col_join(mZero)
    answer = sp.solve(c)
    print answer[0][rc1]
    temp = (complex(answer[0][rc1])+complex(answer[0][rc2])/(1+i))
    intensity = np.append(intensity,(np.real(temp *complex.conjugate(temp))))
    print gamma1,answer

plt.figure(1)
plt.plot(angle, intensity)
plt.show()"""