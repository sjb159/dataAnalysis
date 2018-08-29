'''
Created on 16 Aug 2018

@author: wvx67826
'''
"""
Class to calculate boundary matrix A and A magnetic with arbitrary moment direction 

"""

import timeit
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
i = complex(0,1)
tc1, rc2, tc2, rc1 = sp.symbols("tc1, rc2, tc2, rc1", complex=True)
class XrayMoke():
    def __init__(self):
        
        self.n = []
        self.q = []
        self.d = []
        self.mPf = sp.Matrix([[tc1],
                              [tc2],
                              [0],
                              [0]])
        self.mPi = sp.Matrix([[1],
                              [0],
                              [rc1],
                              [rc2]])
        self.theta = 0
        self.gamma = 0
        self.phi = 0
        
    def a_matrix(self, alphaZ, n):
        
        return sp.Matrix([[       1,         0,         1,       0],
                          [       0,    alphaZ,         0, -alphaZ],
                          [       0,        -n,         0,      -n],
                          [alphaZ*n,         0, -alphaZ*n,       0]])
#A conversion matrix move        
    def a_mag_matrix(self, n ,theta, gamma = 0, phi = 0, q = 0.0): 
        alphaY= self.__alpha_y(theta)
        alphaZ = self.__alpha_z(theta)
        gi = self.__g_i(theta, gamma, phi)
        gr = self.__g_r(theta, gamma, phi)
        return sp.Matrix([[       1,         0,         1,       0],
                          
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
        
        return sp.Matrix([[          u, u*deltaI,        0,         0],
                          [   -u*deltaI,       u,        0,         0],
                          [           0,       0,    1.0/u,  deltaR/u],
                          [           0,       0, deltaR/u,     1.0/u]])
        
    def m_a_d_inva(self,n, d, waveLen, theta, gamma, phi, q):
        mA = self.a_mag_matrix(n, theta, gamma, phi, q)
        minvA = mA**-1
        mD = self.propagation_matrix(n, d, waveLen, theta, gamma, phi, q)
        return mA*mD*minvA
    
    def sum_m_a_d_inva(self,k, n, theta, gamma, phi, q, d, waveLen):
        
        if k == 0:
            theta = np.arcsin(n[0]/n[k]*np.sin(theta))
            self.mAPi = self.a_mag_matrix(n[k], theta, gamma, phi, q[k])*self.mPi
            return self.sum_m_a_d_inva(k+1, n, theta, gamma, phi, q, d, waveLen)
        if k == len(n)-1:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return self.a_mag_matrix(n[k], theta1, gamma, phi, q[k])
        
        else:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return self.m_a_d_inva(n[k], d[k], waveLen, theta1, gamma, phi, q[k])*self.sum_m_a_d_inva(
                                         k+1, n, theta, gamma, phi, q, d, waveLen)
            
    def get_Intensity(self, n, theta, gamma, phi, q, d, waveLen):
        temp = self.sum_m_a_d_inva(0, n, theta, gamma, phi, q, d, waveLen)*self.mPf
        temp  = self.mAPi-temp
        return temp
    def get_m_m(self,k, n, theta, gamma, phi, q, d, waveLen):
        if k == 0:
            theta = np.arcsin(n[0]/n[k]*np.sin(theta))
            temp = self.a_mag_matrix(n[k], theta, gamma, phi, q[k])
            return temp**-1*self.sum_m_a_d_inva(k+1, n, theta, gamma, phi, q, d, waveLen)
        if k == len(n)-1:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return self.a_mag_matrix(n[k], theta1, gamma, phi, q[k])
        
        else:
            theta1 = np.arcsin((n[k-1]/n[k])*np.sin(theta))
            return self.m_a_d_inva(n[k], d[k], waveLen, theta1, gamma, phi, q[k])*self.sum_m_a_d_inva(
                                         k+1, n, theta, gamma, phi, q, d, waveLen)
        
                
    def set_ipol(self,pol = [1,0]):
        self.mPi[0] = pol [0]
        self.mPi[1] = pol [1]

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
xrMoke.set_ipol([1,-i])

#reflective index N = 1-gamma +iBeta

n  = np.array([1.0,1.0-2.38e-5+3.46e-6*i,1.00-2.448e-5+5.5e-7*i])
d = np.array([0,100,200])
q = np.array([0,0,0])
theta = 20
phi = 90
gamma = 90
theta = np.deg2rad(theta)
phi = np.deg2rad(phi)
gamma  = np.deg2rad(gamma)
angle = np.array([])
intensity = np.array([])
waveLen = 1.54
for gamma1 in np.arange (90,88, -0.1):
    start_time1 = timeit.default_timer()
    theta = np.deg2rad(gamma1)
    Qz = 4.0*np.pi/waveLen*np.sin(np.deg2rad(90.-gamma1))
    angle = np.append(angle,Qz)
    
    #k= xrMoke.get_Intensity(n, theta, gamma, phi, q, d, waveLen)
    
    
    mZero = sp.Matrix([[0],
                       [0],
                       [0],
                       [0]])
    
    mM = xrMoke.get_m_m(0, n, theta, gamma, phi, q, d, waveLen)
    #mM= sp.Matrix([[0,1,2],[3,4,5],[6,7,8],[10,11,12]])
    
    mG = mM[0:2,0:2]
    mGInv = mG**-1
    mI = mM[2:4,0:2]
    mIGInv = mI*mGInv
    Igg = mIGInv*np.conj(mIGInv)
    intensity = np.append(intensity, np.absolute(complex(Igg[0,0])+complex(Igg[0,1]+complex(Igg[1,0])+complex(Igg[1,1]))))
    print np.absolute(complex(Igg[0,0]))
    """
    c= k.col_join(mZero)
    start_time2 = timeit.default_timer()
    answer = sp.solve(c)
    print answer


    temp = (complex(answer[0][rc1])+complex(answer[0][rc2]))/(1+i)
    intensity = np.append(intensity,(np.real(temp *complex.conjugate(temp))))
   
    elapsed2 = timeit.default_timer() - start_time2"""
    elapsed = timeit.default_timer() - start_time1
    print gamma1, elapsed#, elapsed2 
plt.figure(1)
plt.plot(angle, intensity)
plt.semilogy()
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