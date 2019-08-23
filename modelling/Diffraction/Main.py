'''
Created on 7 Aug 2018

@author: wvx67826
'''
import numpy as np
import matplotlib.pyplot as plt
i = complex(0,1)

def th2q(lamda, angle):
    return 4.0*np.pi/lamda*np.sin(angle/180*np.pi)
def q2th(lamda,q):
    return np.arcsin(q*lamda/4.0/np.pi)

def fm(z1,z2,z3,lamda,q,f1,f2):
    return i*f1*np.matrix([[0.0,       z1*np.cos(q2th(lamda,q)-z3*np.sin(q2th(lamda,q)))],
                          [z3*np.sin(q2th(lamda,q)) - z1*np.cos(q2th(lamda,q)),      
                                        -z2*np.sin(2.0*q2th(lamda,q))]])+f2*np.matrix([[z2**2,
                                        -z2*(z1*np.sin(q2th(lamda,q))-z3*np.cos(q2th(lamda,q)))],
                                        [z2*(z1*np.sin(q2th(lamda,q))+z3*np.cos(q2th(lamda,q))),
                                    np.cos(q2th(lamda,q))**2*(z1**2*np.tan(q2th(lamda,q))**2+z3**2)]])
def f0 (lamda, q,scale):
    return scale*np.matrix([[1.0, 0.0],
                    [0.0, np.cos(2.0*q2th(lamda,q))]])

def set_ipol(pol, angle = 0):
    ipol = {"Si"    : np.matrix([[1.0],
                                         [0.0]]),
            "Pi"    : np.matrix([[0.0],
                                         [1.0]]),
            "LC"    : np.matrix([[0.707106781186547],
                                         [0.707106781186547*i]]),
            "RC"    : np.matrix([[0.707106781186547],
                                         [-0.707106781186547*i]]),
            "LA"    : np.matrix([[np.cos(np.deg2rad(angle))],
                                         [np.sin(np.deg2rad(angle))]]),
            }

    return ipol[pol]
def intensity (q,lamda, z,z1,z2,z3,fs,f1,f2):
    temp = np.matrix([[0,0],[0,0]])
    
    for k in range(1):
        for y in z:
            z1rot = z1#*np.sin(2.0*y/20*np.pi+3*np.pi/4.0)
            z2rot = z2#*np.cos(2.0*y/20*np.pi)
            z3rot = z3#*np.cos(2.0*y/20*np.pi)
            temp = temp + np.exp(i*(y)*q)*((f0(lamda,q,fs))+fm(z1rot,z2rot,z3rot,lamda,q,f1,f2))


    return temp


def pol_intensity(intensity, inPol, outPol, inAngle = 0, outAngle = 0):
    mIpol = set_ipol(inPol,inAngle)
    mFinI = np.multiply(intensity,mIpol)
    if outPol == "Si+Pi":
        finI= np.dot(mFinI[0,0]+mFinI[1,0],np.conj(mFinI[0,0]+mFinI[1,0])) + np.dot(
                     mFinI[0,1]+mFinI[1,1],np.conj(mFinI[0,1]+mFinI[1,1]))
        return np.absolute(finI)
    if outPol == "Si":

        finI = np.dot(mFinI[0,0]+mFinI[1,0],np.conj(mFinI[0,0]+mFinI[1,0]))
        return np.absolute(finI)
    if outPol == "Pi":
        
        finI = np.dot(mFinI[0,1]+mFinI[1,1],np.conj(mFinI[0,1]+mFinI[1,1]))
        return np.absolute(finI)
    
    
    if outPol == "LA":
        finI= np.dot((mFinI[0,0]+mFinI[1,0])*np.cos(np.deg2rad(outAngle)),np.conj(mFinI[0,0]+mFinI[1,0])*np.cos(np.deg2rad(outAngle))) + np.dot(
                     (mFinI[0,1]+mFinI[1,1])*np.sin(np.deg2rad(outAngle)),np.conj(mFinI[0,1]+mFinI[1,1])*np.sin(np.deg2rad(outAngle)))
        return np.absolute(finI)
        
        


    

lamda = 1.54
q = np.arange(0.2, 3.2, 0.01)
z = np.arange (0, 200., 4)
iMeasure1 = []
iMeasure2 = []
iMeasure3 = []
iMeasure4 = []
iMeasure5 = []
iMeasure6 = []
iMeasure7 = []
iMeasure8 = []
iMeasure9 = []
iMeasure10 = []
iMeasure11 = []
iMeasure12 = []



fm1 = []
fm2 = []

z1 = 1.0
z2 = 0.0
z3 = 0.1

fs = 0.0
f1 = 1.0
f2 = 0

for k in q:
    tempI = intensity(k,lamda, z,z1,z2,z3, fs, f1,f2)
    iMeasure1 = np.append(iMeasure1,pol_intensity(tempI,"Si","Si"))
    iMeasure2 = np.append(iMeasure2,pol_intensity(tempI,"Si","Pi"))
    iMeasure3 = np.append(iMeasure3,pol_intensity(tempI,"Pi","Si"))
    iMeasure4 = np.append(iMeasure4,pol_intensity(tempI,"Pi","Pi"))
    
 
z1 = 0.0
z2 = 1.0
z3 = 0.1
f2 = 0.0

for k in q:
    tempI = intensity(k,lamda, z,z1,z2,z3,fs, f1,f2)
    iMeasure5 = np.append(iMeasure5,pol_intensity(tempI,"Si","Si"))
    iMeasure6 = np.append(iMeasure6,pol_intensity(tempI,"Si","Pi"))
    iMeasure7 = np.append(iMeasure7,pol_intensity(tempI,"Pi","Si"))
    iMeasure8 = np.append(iMeasure8,pol_intensity(tempI,"Pi","Pi"))    

cd = iMeasure1-iMeasure2
polIn = []
polOut = []
angle = np.arange(0,1,0.05)

z1 = 0.0
z2 = 1.0
z3 = 1.0
    
for a,b in enumerate (angle):

    tempI = intensity(1.568*2, lamda, z,z1,z2,z3,fs, f1,b)
    iMeasure9 = np.append(iMeasure9,pol_intensity(tempI,"Si","Si"))
    iMeasure10 = np.append(iMeasure10,pol_intensity(tempI,"Si","Pi"))
    iMeasure11 = np.append(iMeasure11,pol_intensity(tempI,"Pi","Si"))
    iMeasure12 = np.append(iMeasure12,pol_intensity(tempI,"Pi","Pi"))    
    

plt.figure(1)
plt.subplot(221)
plt.plot(q,iMeasure1)
plt.plot(q,iMeasure5)
plt.title("Si-Si")
plt.subplot(222)
plt.plot(q,iMeasure2)
plt.plot(q,iMeasure6)
plt.title("Si-pi")
plt.subplot(223)
plt.plot(q,iMeasure3)
plt.plot(q,iMeasure7)
plt.title("pi-si")
plt.subplot(224)
plt.plot(q,iMeasure4)
plt.plot(q,iMeasure8)
plt.title("pi-pi")

plt.figure(2)
plt.subplot(221)
plt.plot(q,iMeasure1-iMeasure5)
plt.title("Si-Si different")
plt.subplot(222)
plt.plot(q,iMeasure2-iMeasure6)
plt.title("Si-pi different")

plt.subplot(223)
plt.plot(q,iMeasure3-iMeasure7)
plt.title("pi-Si different")
plt.subplot(224)
plt.plot(q,iMeasure4-iMeasure8)
plt.title("Pi-Pi different")

plt.figure(3)
plt.subplot(221)
plt.plot(angle,iMeasure9)

plt.title("Si-Si")
plt.subplot(222)
plt.plot(angle,iMeasure10)

plt.title("Si-pi")
plt.subplot(223)
plt.plot(angle,iMeasure11)

plt.title("pi-si")
plt.subplot(224)
plt.plot(angle,iMeasure12)

plt.title("pi-pi")

plt.show()