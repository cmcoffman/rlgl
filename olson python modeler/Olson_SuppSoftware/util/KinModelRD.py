__author__ = 'EvanLab'

from KinModel import KinModel

class KinModelRD(KinModel):

    def __init__(self,name='RD',infile=None):
        if infile:
            self.importmodel(file)
        else:
            self.name = name
            self.abcorr = 0

            self.blank = 9.583

            self.params = [[0.17708205548190167],[0.020346587001329526],[22.1290834840108-self.blank,85.899687844314,1.38573,94.974],[0.0]]
            self.paramerrs = [[0.017707549969742352],[0.000541765932577775],[1.239008,8.32705,0.105767168324937,9.95800369654821],[0.0]]

            self.paramnames = [['kp'],['kg'],['b','a','n','k'],['tau']]

    def kp(self,p0,lsr,lsg):
        return self.params[0][0]

    def kg(self,p0,g0,lsr,lsg):
        return self.params[1][0]

    def ss(self,lsr,lsg):
        b,a,n,k = self.params[2]
        return b + a*k**n / (lsr**n + k**n)

    def tau(self,p0,g0,lsr,lsg):
        return self.params[3][0]

    def interrs(self,rint,gint):
        a2,a1,a0 = [-0.000038236,0.011645,4.8598]
        err = max(a2*rint**2 + a1*rint + a0, 1.5465)
        return err

    def sserrs(self,ss):
        from math import isnan

        b,a,n,k = [float(i) for i in self.params[2]]

        if ss-b <=0: rint = 4095
        elif 1-(ss-b)/a <=0: rint = 0
        else: rint = k*( ( 1-(ss-b)/a ) / ( (ss-b)/a ) )**(1/n)
        if isnan(rint): rint = 0

        a2,a1,a0 = [-0.000038236,0.011645,4.8598]
        err = max(a2*rint**2 + a1*rint + a0, 1.5465)

        return err

