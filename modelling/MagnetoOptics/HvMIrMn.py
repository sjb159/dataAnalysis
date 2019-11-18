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
               1.0+3.31060E-03+2.05586E-03*i,
               1.0+1.37849E-03+1.45084E-03*i,
               1.0+1.37849E-03+1.45084E-03*i,
               1.0+6.95156E-04+1.42226E-04*i,
               1.0+7.53183E-04+9.51189E-05*i])

d = np.array([0,
              30.0,
              40.0,
              20.0,
              20.0,
              200])

q = np.array([0.0,
              0.0,
              1.68661e-3+1.06361e-4*i,
              1.68661e-3+1.06361e-4*i,
              0.0,
              0.0])
aPhi =   np.array([0.0, 0.0, 70.0, 90,0, 0.0, 0.0])
aGamma = np.array([0.0, 0.0, 90.0, 90,0, 0.0, 0.0])
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

"""Define energy"""
waveLen = 12.4/0.777198
"""timer"""
start_time1 = timeit.default_timer()

"""define moment direction and how it changes"""


angle = np.arange(-100,100,1.0)
angle = np.append(angle, np.arange(100,-100,-1.0))

#spin = [45,-45] #right angle to beam
spin = [0.0, 180.0, 0] #right angle to beam

#spin = [90,180] #parallel 
hy = np.full((1,119),spin[0])
hy = np.append(hy, spin[1])
hy = np.append(hy, np.full((1,199),spin[1]))
hy = np.append(hy, spin[0])
hy = np.append(hy, np.full((1,80),spin[0]))

thetaWanted =24.5
theta = 90 - thetaWanted 

filename = "Pt_Cu_gamma_ra_fix%.f-fix%.f-%.f_th%.f.dat" %(aGamma[1],aGamma[2],aGamma[3],theta)
f = open("TestData/"+filename, "w+")

aGamma  = np.deg2rad(aGamma)
theta = np.deg2rad(theta)
aPhi = np.deg2rad(aPhi)
#for gamma1 in np.arange (90,450, 1.0):
"""do the hvm loop"""
for gamma1 in hy:    
    #aPhi[1] = np.deg2rad(gamma1)
    #aPhi[2] = np.deg2rad(gamma1)
    aGamma[2] = np.deg2rad(gamma1)
    #aGamma[4] = np.deg2rad(gamma1)
    """    if gamma1 ==spin[0]:
        aPhi[3] = np.deg2rad(14)
    if gamma1 == spin[1]:
        aPhi[3] =  np.deg2rad(14)
    if gamma1 == spin[2]:
        aPhi[3] = np.deg2rad(-14)
    """
    #aGamma[2] = np.deg2rad(gamma1)
    #aGamma[3] = -np.deg2rad(gamma1)
    ##aGamma[2] = np.deg2rad(gamma1)
    Qz = gamma1-90#4.0*np.pi/waveLen*np.sin(np.deg2rad(90.-gamma1))   
      
    #aGamma = np.array([0, 90,0])
    #aGamma  = np.deg2rad(aGamma)
    xrMoke.cal_intensity_mD(n, theta, aGamma, aPhi, q, d, waveLen)
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
    
elapsed = timeit.default_timer() - start_time1
print elapsed
f.write("field, Pi-full, Si-full,Pi-Si, Pi-Pi, Si-Si, Si,-Pi, XMCD, LC,RC \n")
for n in range (0,len(angle)):                
    f.write("%.8g , %.8g , %.8g, %.8g , %.8g , %.8g,, %.8g , %.8g , %.8g , %.8g \n"
             %(angle[n],intensity1[n],intensity2[n],intensity3[n],
               intensity4[n],intensity5[n],intensity6[n],intensity7[n],intensity8[n]
               ,intensity9[n]))

plt.figure(1)
plt.subplot(221)
#plt.semilogy()
plt.title("Pi")
plt.plot(angle, intensity3)
#plt.figure(2)
plt.subplot(222)
plt.title("Si")
plt.plot(angle, intensity5)
#plt.figure(3)
"""plt.title("Pi-Si")
plt.plot(angle, intensity3)
plt.figure(4)
plt.title("Pi-Pi")
plt.plot(angle, intensity4)
plt.figure(5)
plt.title("Si-Si")
plt.plot(angle, intensity5)
plt.figure(6)
plt.title("Si-Pi")
plt.plot(angle, intensity6)
"""
#plt.figure(7)
plt.subplot(223)
plt.title("XMCD")
plt.plot(angle, intensity7)
#plt.figure(8)
plt.subplot(224)
plt.title("LC &RC")
plt.plot(angle, intensity8)
plt.plot(angle, intensity9)
plt.show()
