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
                                        -z2*np.sin(2.0*q2th(lamda,q))]])
def f0 (lamda, q,scale):
    return scale*np.matrix([[1.0, 0.0],
                    [0.0, np.cos(2.0*q2th(lamda,q))]])


def intensity (q,lamda, z,z1,z2,z3):
    temp = complex (0,0)
    for y in z:
        z1rot = z1*np.sin(y/20*np.pi)
        z2rot = z2*np.cos(y/20*np.pi)
        z3rot = z3*np.cos(y/20*np.pi)
        temp = temp + np.exp(i*y*q)*((f0(lamda,q,1.0))+fm(z1rot,z2rot,z3rot,lamda,q,1.0,0.1))
        #print temp[0]
    return np.real(np.conj(temp[0,1])*temp[0,1])

lamda = 1.54
q = np.arange(0, 4, 0.01)
z = np.arange (0, 120., 4)
z1 = 1
z2 = 1
z3 = 1
iMeasure = []
for k in q:
    iMeasure.append(intensity(k,lamda, z,z1,z2,z3))
    
plt.figure(1)
plt.plot(q,iMeasure)
plt.show()