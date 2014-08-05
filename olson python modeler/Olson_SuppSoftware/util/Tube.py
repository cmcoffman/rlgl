
class Tube:
    
    ## 1/21/13 EO
    ## Currently a very basic implementation of the data associated with a single tube run through the flow
    ## including only amean and rcv, with optional uncertainties
    ## Later would like to have more stats loaded in, as well as
    ## the option to have fcs data directly loaded up into this structure
    
    def __init__(self,amean=None,amean_err=None,rcv=None,rcv_err=None):
        self.amean = amean
        self.rcv = rcv
        self.amean_err = amean_err
        self.rcv_err = rcv_err
    
    def set_amean(self,amean,amean_err=None):
        self.amean=amean
        if not amean_err == None: self.amean_err = amean_err
    
    def set_rcv(self,rcv,rcv_err=None):
        self.rcv = rcv
        if not rcv_err == None: self.rcv_err = rcv_err
        
    def get_amean(self):
        return self.amean
    
    def get_amean_err(self):
        return self.amean_err
        
    def get_rcv(self):
        return self.rcv
        
    def get_rcv_err(self):
        return self.rcv_err
    
    def get_stats(self):
        return [self.amean,self.rcv]
        
    def get_stats_errs(self):
        return [self.amean_err,self.rcv_err]
    
#~ t1 = Tube(20,0.3)
#~ t2 = Tube()
#~ t2.set_amean(10,2)
#~ t2.set_rcv(0.2,0.05)

#~ print t1.get_stats()
#~ print t1.get_stats_errs()
#~ print t2.get_stats()
#~ print t2.get_stats_errs()