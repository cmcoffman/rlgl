## This class should store useful methods that are utilized by any of our
## simple kinetic models (e.g. pStep,gStep, etc.)

from numpy import exp

class KinCore:
    
    def __init__(self):
        pass

    # Returns light signals at times given a sequence lst, lsr, and lsg
    # All parameters must be iterable!
    # ls parameters must be ordered!
    # NOT WORKING
    def lsinterp(self,times, lstimes, lsrs, lsgs):
        ret = [[],[]]
        for time in times:
            i=0
            while time < lstimes[i]:
                i=i+1
            ret[0].append(lsrs[i])
            ret[1].append(lsgs[i])
        return ret

    # Return step function response of production rate from p0 to ss at time t.
    # This is pure step-response (no tau!)
    def pStep(self,t,p0,kp,lsr,lsg): 
        
        ssc = self.ss(lsr,lsg)
        kpc = self.kp(p0,lsr,lsg)
        
        return ssc + (p0-ssc) * exp(-kpc*t)
        
    # Return step function response of gene product from p0,g0 to gss
    def gStep(self,t,p0,g0,kp,kg,lsr,lsg):
        
        ssc = self.ss(lsr,lsg)
        kpc = self.kp(p0,lsr,lsg)
        kgc = self.kg(p0,g0,lsr,lsg)
        
        ## Sometimes kp and kg will become equal - handle this by using the appropriate limit
        try:
            pterm = (ssc-p0) * kgc/(kpc-kgc) * (exp(-kgc*t) - exp(-kpc*t))
        except ZeroDivisionError:
            pterm = (ssc-p0) * exp(-kgc*t) * kgc * t
            
        gterm = (ssc-g0) * exp(-kgc*t)
        
        return ssc - pterm - gterm
                
    # This could probably be improved a bit by looping through control points intsead...
    def sim(self,times,p0,g0,kp,kg,tau,lstimes,lsrs,lsgs):

        ret = [[],[]]
        
        li = 0
        
        ## Determine the tau for the first light point (assuming preconditioning has occurred)
        tauc_next = tau(p0,g0,lsrs[0],lsgs[0])
        tauc = tauc_next

        in_early = True
        in_first = True
        for t in times:
            
            ## Deal with the early time-points
            if t < lstimes[0]+tauc_next and in_early:
                
                ret[0].append(p0)
                ret[1].append(g0)
                
            elif len(lstimes) > 1:
                in_early = False
                
                ## tau for the first control signal is calculated explicitly
                if li == 0:
                    
                    p = self.pStep(lstimes[1]-lstimes[0]-tauc,p0,kp,lsrs[0],lsgs[0])
                    g = self.gStep(lstimes[1]-lstimes[0]-tauc,p0,g0,kp,kg,lsrs[0],lsgs[0])
                    if in_first:
                        tauc = tauc_next
                        tauc_next = tau(p,g,lsrs[1],lsgs[1])
                        in_first = False
                
                ## Iterate through light points until you reach the next time point desired
                while li+1 < len(lstimes) and t >= lstimes[li+1] + tauc_next:
                    
                    g0 = self.gStep(lstimes[li+1]+tauc_next-lstimes[li]-tauc,p0,g0,kp,kg,lsrs[li],lsgs[li])
                    p0 = self.pStep(lstimes[li+1]+tauc_next-lstimes[li]-tauc,p0,kp,lsrs[li],lsgs[li])
                    li = li + 1
                    tauc = tauc_next
                    
                    ## Determine the tau for the next light point unless we're at the last one.
                    if li+1 < len(lstimes):
                        p = self.pStep(lstimes[li+1]-lstimes[li]-tauc,p0,kp,lsrs[li],lsgs[li])
                        g = self.gStep(lstimes[li+1]-lstimes[li]-tauc,p0,g0,kp,kg,lsrs[li],lsgs[li])
                        tauc_next = tau(p,g,lsrs[li+1],lsgs[li+1])
                        
                ret[0].append(self.pStep(t-lstimes[li]-tauc,p0,kp,lsrs[li],lsgs[li]))
                ret[1].append(self.gStep(t-lstimes[li]-tauc,p0,g0,kp,kg,lsrs[li],lsgs[li]))
            
            else:
                
                ret[0].append(self.pStep(t-lstimes[0]-tauc,p0,kp,lsrs[0],lsgs[0]))
                ret[1].append(self.gStep(t-lstimes[0]-tauc,p0,g0,kp,kg,lsrs[0],lsgs[0]))
                
        return ret
       
#~ p0=18
#~ g0=18

#~ def kp(p0,lsr,lsg):
#    ~ return 0.06
#~ def kg(p0,g0,lsr,lsg):
    #~ return 0.018
#~ def ss(lsr,lsg):
    #~ b = 18
    #~ a = 62
    #~ n = 2.5
    #~ k = 140
    #~ return b + a * lsg**n / (lsg**n + k**n)
#~ def tau(p,g,lsr,lsg):
    #~ #return 10
    #~ return 5.0 if ss(lsr,lsg) > p else 2.0
    
#~ lstimes = [0,60,120,180,240,300]

#~ lsrs = [4095,4095,4095,4095,4095,4095]
#~ lsgs = [4095,0,4095,0,4095,0]

#~ times = range(420)

#~ kc = KinCore()

#~ import matplotlib.pyplot as plt

#~ x=times
#~ y1,y2= kc.sim(times,p0,g0,kp,kg,tau,lstimes,lsrs,lsgs)
#~ y3 = [i*62.0/4095.0 + 18.0 for i in kc.lsinterp(times,lstimes,lsrs,lsgs)[1]]
#~ print kc.lsinterp(times,lstimes,lsrs,lsgs)[1]

#~ p1 = plt.plot(x,y1,'b-',x,y2,'r-',x,y3,'g-')
#~ plt.show()