'''
Created on 10 Apr 2019

@author: wvx67826
'''
from UniversalMoke import XrayMoke
import timeit
import numpy as np
import matplotlib.pyplot as plt
i = complex(0,1)
xrMoke = XrayMoke()

##============= Define sample gamma and beta ===============================
n  = np.array([1.0,
               1.0-1.77147e-4+1.21e-4*i,
               1.0+1.537e-4+3.9349e-4*i])

d = np.array([0,
              100,
              200])
q = np.array([0,
              1.68661e-5+1.06361e-4*i,
              0])

aPhi =   np.array([0,
                   90,
                   0])
aPhiS =   np.array([0,
                   90,
                   0])
aGamma = np.array([0,
                   90,
                   0])

aGammaS = np.array([0,
                   90,
                   0])
##=================================================================================
"""To store result"""
angle = np.array([])
intensity1 = np.array([])
intensity2 = np.array([])
intensity3 = np.array([])
intensity4 = np.array([])
intensity5 = np.array([])
intensity6 = np.array([])
intensity7 = np.array([])
intensity8 = np.array([])
intensity9 = np.array([])
intensity1S = np.array([])
intensity2S = np.array([])
intensity3S = np.array([])
intensity4S = np.array([])
intensity5S = np.array([])
intensity6S = np.array([])
intensity7S = np.array([])
intensity8S = np.array([])
intensity9S = np.array([])

"""Define energy"""
waveLen = 12.4/0.777198
"""timer"""
start_time1 = timeit.default_timer()

thetaWanted =np.arange(0.1,90,0.1) 
theta = 90 - thetaWanted 

aGamma  = np.deg2rad(aGamma)
aGammaS  = np.deg2rad(aGammaS)
theta = np.deg2rad(theta)
aPhi = np.deg2rad(aPhi)
aPhiS = np.deg2rad(aPhiS)
for i in theta:
    xrMoke.cal_intensity_mD(n, i, aGamma, aPhi, q, d, waveLen)
    intensity1 = np.append(intensity1,xrMoke.get_intensity("Pi", "Si+Pi"))
    intensity2 = np.append(intensity2,xrMoke.get_intensity("Si", "Si+Pi"))
    intensity3 = np.append(intensity3,xrMoke.get_intensity("Pi", "Si"))
    intensity4 = np.append(intensity4,xrMoke.get_intensity("Pi", "Pi"))
    intensity5 = np.append(intensity5,xrMoke.get_intensity("Si", "Si"))
    intensity6 = np.append(intensity6,xrMoke.get_intensity("Si", "Pi"))
    intensity7 = np.append(intensity7,(xrMoke.get_intensity("LC", "Si+Pi")
                                       -xrMoke.get_intensity("RC", "Si+Pi")))
    intensity8 = np.append(intensity8,xrMoke.get_intensity("LC", "Si+Pi"))
    intensity9 = np.append(intensity9,xrMoke.get_intensity("RC", "Si+Pi"))
    
for i in theta:
    xrMoke.cal_intensity_mD(n, i, aGammaS, aPhiS, q, d, waveLen)
    intensity1S = np.append(intensity1S,xrMoke.get_intensity("Pi", "Si+Pi"))
    intensity2S = np.append(intensity2S,xrMoke.get_intensity("Si", "Si+Pi"))
    intensity3S = np.append(intensity3S,xrMoke.get_intensity("Pi", "Si"))
    intensity4S = np.append(intensity4S,xrMoke.get_intensity("Pi", "Pi"))
    intensity5S = np.append(intensity5S,xrMoke.get_intensity("Si", "Si"))
    intensity6S = np.append(intensity6S,xrMoke.get_intensity("Si", "Pi"))
    intensity7S = np.append(intensity7S,(xrMoke.get_intensity("LC", "Si+Pi")
                                       -xrMoke.get_intensity("RC", "Si+Pi")))
    intensity8 = np.append(intensity8,xrMoke.get_intensity("LC", "Si+Pi"))
    intensity9 = np.append(intensity9,xrMoke.get_intensity("RC", "Si+Pi"))
    
    
elapsed = timeit.default_timer() - start_time1
print elapsed

plt.figure(1)

plt.subplot(221)
plt.semilogy()
plt.plot(thetaWanted, intensity3)
plt.plot(thetaWanted, intensity3S)
plt.title("Pi-Si")

plt.subplot(222)
plt.semilogy()

plt.plot(thetaWanted,  intensity5)
plt.plot(thetaWanted,  intensity5S)
plt.title("Si-Si")

plt.subplot(223)
plt.semilogy()
plt.plot(thetaWanted , intensity4)
plt.plot(thetaWanted , intensity4S)
plt.title("pi-pi")

plt.subplot(224)
plt.semilogy()
plt.plot(thetaWanted , intensity6)
plt.plot(thetaWanted , intensity6S)
plt.plot(thetaWanted, intensity3)
plt.plot(thetaWanted, intensity3S)

plt.title("Si-Pi")

plt.figure(2)
plt.subplot(211)
plt.semilogy()
plt.plot(thetaWanted , intensity2)
plt.plot(thetaWanted , intensity2S)
plt.subplot(212)
plt.semilogy()
plt.plot(thetaWanted , intensity1)
plt.plot(thetaWanted , intensity1S)
plt.show()






