'''
Created on 19 Sep 2017

@author: wvx67826
'''
import scipy as sp

class AngleToQ():
    def __init__(self):
        pass
    def cal_qz(self, tth, th, energy):
        return 2.0*sp.pi/self.cal_wave(energy)*(sp.sin(sp.deg2rad((tth-th)))+sp.sin(sp.deg2rad(th)))
    def cal_qx(self,tth, th, energy):
        return 2.0*sp.pi/self.cal_wave(energy)*(sp.cos(sp.deg2rad((tth-th)))-sp.cos(sp.deg2rad(th)))
    def cal_wave(self, energy):
        return 12400.0/energy