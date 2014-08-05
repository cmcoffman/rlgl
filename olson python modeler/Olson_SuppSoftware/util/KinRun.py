from Tube import Tube

class KinRun:
    
    def __init__(self,name=None,desc=None,date=None,tubepath=None,statspath=None,\
                    tubenums=[],tubeexcludes=[],\
                    tubes=[],preR=None,preG=None,times=[],\
                    lighttimes=[],rints=[],gints=[],redtube=None,greentube=None,
                    system=None):
        self.name = name
        self.desc = desc
        self.date = date
        self.tubepath = tubepath
        self.statspath = statspath
        self.tubenums = tubenums
        self.tubeexcludes = tubeexcludes
        self.tubes = tubes
        self.times = times
        self.lighttimes = lighttimes
        self.rints = rints
        self.gints = gints
        self.preR = preR
        self.preG = preG
        self.redtube = redtube
        self.greentube = greentube
        self.system = system
    
    def __repr__(self):
        return "{}: {}".format(self.name,self.desc)
    
    ## This function go to the path with the statsfile (and optionally errs file)
    ## and use the data to initialize the tubes
    def load_from_stats(self,errs=True):
        tubeslist = []
        
        self.tubes = tubeslist
        
    ## This function should go to the path with the fcs files and use
    ## the extraction parameters from some extract settings file to 
    ## initialize the tubes (not ready!)
    def loat_from_fcs(self,errs=True):
        pass
    
    def set_name(self,name):
        self.name = name
    
    def set_desc(self,desc):
        self.desc = desc
        
    def set_date(self,date):
        self.date = date
        
    def set_tubepath(self,tubepath):
        self.tubepath = tubepath
    
    def set_statspath(self,statspath):
        self.statspath = statspath
        
    def set_tubenums(self,tubenums):
        self.tubenums = tubenums
        
    def set_tubeexcludes(self,tubeexcludes):
        self.tubeexcludes = tubeexcludes
        
    def set_tubes(self,tubes):
        self.tubes = tubes
        
    def set_pre(self,preR,preG):
        self.preR = preR
        self.preG = preG

    def set_redtube(self,redtube):
        self.redtube = redtube

    def set_greentube(self,greentube):
        self.greentube = greentube
        
    def set_times(self,times):
        self.times = times
        
    def set_lighttimes(self,lighttimes):
        self.lighttimes = lighttimes
    
    def set_gints(self,gints):
        self.gints = gints
        
    def set_rints(self,rints):
        self.rints = rints
        
    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc
        
    def get_date(self):
        return self.date
        
    def get_tubepath(self):
        return self.tubepath
        
    def get_statspath(self):
        return self.statspath
        
    def get_tubenums(self):
        return self.tubenums
        
    def get_tubeexcludes(self):
        return self.tubeexcludes
    
    def get_tubes(self):
        return self.tubes
    
    def get_pre(self):
        return (self.preR,self.preG)

    def get_redtube(self):
        return self.redtube

    def get_greentube(self):
        return self.greentube
        
    def get_times(self):
        return self.times
    
    def get_lighttimes(self):
        return self.lighttimes
    
    def get_rints(self):
        return self.rints
        
    def get_gints(self):
        return self.gints
        
    def get_light_seq(self):
        return zip(self.lighttimes,self.rints,self.gints)
        
    ## More useful get methods
    def get_data(self):
        data = {
            'name': self.name,\
            'd_t': self.times,\
            'd_am': self.get_ameans(),\
            'd_rcv': self.get_rcvs(),\
            'd_counts': None,\
            'd_gated': None,\
            'l_t': self.lighttimes,\
            'l_r': self.rints,\
            'l_g': self.gints,\
            'l_pr': self.preR,
            'l_pg': self.preG}
        return data
    
    def get_ameans(self,errs=False):
        ameans = [tube.get_amean() for tube in self.tubes]
        if not errs:
            return ameans
        else:
            amean_errs = [tube.get_amean_err() for tube in self.tubes]
            return (ameans,amean_errs)
            
    def get_rcvs(self,errs=False):
        rcvs = [tube.get_rcv() for tube in self.tubes]
        if not errs:
            return rcvs
        else:
            rcv_errs = [tube.get_rcv_err() for tube in self.tubes]
            return (rcvs,rcv_errs)

#~ tubeList = [Tube(10,0.1),Tube(20,0.2)]
#~ timeList = [0,30]
#~ lightList = [(0,4095,0),(15,0,4095)]

#~ kr1 = KinRun('rgOn1','turn on to 0.5', tubeList,timeList,lightList)
#~ print kr1
#~ print kr1.get_ameans(errs=True)
#~ print kr1.get_rcvs(errs=True)
#~ print kr1.get_data()