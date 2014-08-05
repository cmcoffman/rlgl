__author__ = 'EvanLab'
from KinModel import KinModel

class KinModelRG_Tet(KinModel):

    def __init__(self,name='RG',infile=None):
        if infile:
            self.importmodel(file)
        else:
            self.name = name

            self.params = [[0.027176485499667852,172.358415985129,0.9927395430750245,0.070095893692439],[0.012652691435245379],[20.19,69.70,2.821,135.0],[4.60457911403]] ## ssTF from 131119_n
            self.paramerrs = [[0.0057394341335320785, 34.84024917478996, 0.31422996890502647, 0.009693043791651472],[0.00071364528296360486],[0.9958,3.0235,0.277,5.7518],[0.82431]]

            self.paramnames = [['kpl','kpk','kpm','kpo'],['kg'],['b','a','n','k'],['tau']]
            self.abcorr = 0.540811

    def kp(self,p0,lsr,lsg):
        kpl, kpk, kpm, kpo = self.params[0]
        if self.ss(lsr,lsg) < p0:
            return kpo
        else:
            return kpl if lsg < kpk else kpl + (kpm-kpl)/(4095.0-kpk)*(lsg-kpk)

    def kg(self,p0,g0,lsr,lsg):
        return self.params[1][0]

    def ss(self,lsr,lsg):
        b,a,n,k = self.params[2]
        return b + 0.00002060*a*lsg + a*lsg**n / (lsg**n + k**n)

    def tau(self,p0,g0,lsr,lsg):
        return self.params[3][0]

    def sserrs(self,ss):
        a2,a1,a0 = [-7.76e-4,8.17e-2,-7.13e-1]
        return a2*ss**2 + a1*ss**1 + a0

