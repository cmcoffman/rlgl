from KinCore import KinCore
from KinRun import KinRun
from Tube import Tube

class KinModel(KinCore):
    
    def __init__(self,name='default'):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def kp(self,p0,lsr,lsg):
        kpl, kpk, kpm = self.params[0]
        return kpl if lsg < kpk else kpl + kpm*(lsg-kpk)
    
    def kg(self,p0,g0,lsr,lsg):
        return self.params[1][0]
    
    def ss(self,lsr,lsg):
        b,a,n,k,m = self.params[2]
        return b + m*lsg + a*lsg**n / (lsg**n + k**n)

    def tau(self,p0,g0,lsr,lsg):
        tup = self.params[3][0]
        tdown = self.params[3][1]
        return tup if self.ss(lsr,lsg) > g0 else tdown

    def sserrs(self,ss):
        return 0
    
    def setname(self,name):
        self.name = name

    def setabcorr(self,val):
        self.abcorr = val

    def getabcorr(self):
        return self.abcorr
    
    def setparams(self,kpps,kgps,ssps,taups):
        self.params[0] = [float(kpp) for kpp in kpps]
        self.params[1] = [float(kgp) for kgp in kgps]
        self.params[2] = [float(ssp) for ssp in ssps]
        self.params[3] = [float(taup) for taup in taups]
        return
        
    def seterrs(self,kpes,kges,sses,taues):
        self.paramerrs = [[],[],[],[]]
        self.paramerrs[0] = [float(kpe) for kpe in kpes]
        self.paramerrs[1] = [float(kge) for kge in kges]
        self.paramerrs[2] = [float(sse) for sse in sses]
        self.paramerrs[3] = [float(taue) for taue in taues]
        return
        
    def setparamnames(self,kpns,kgns,ssns,tauns):
        self.paramnames[0] = [kpn for kpn in kpns]
        self.paramnames[1] = [kgn for kgn in kgns]
        self.paramnames[2] = [ssn for ssn in ssns]
        self.paramnames[3] = [taun for taun in tauns]

    def setparam(self,name,value):
        for i,list in enumerate(self.paramnames):
            if name in list: self.params[i][list.index(name)]=value

    def getparam(self,name):
        for i,list in enumerate(self.paramnames):
            if name in list: return self.params[i][list.index(name)]

    def setparamerr(self,name,value):
        for i,list in enumerate(self.paramnames):
            if name in list: self.paramerrs[i][list.index(name)]=value

    def getparamerr(self,name):
        for i,list in enumerate(self.paramnames):
            if name in list: return self.paramerrs[i][list.index(name)]
        
    def getname(self):
        return self.name
    
    def getparams(self):
        return self.params
        
    def geterrs(self):
        return self.paramerrs
        
    def getparamnames(self):
        return self.paramnames
    
    def error(self,kinrunlist,units='afus'):
        
        sumsq = 0
        
        for run in kinrunlist:
            
            times = run.get_times()
            preR, preG = run.get_pre()
            p0 = g0 = self.ss(preR,preG)
            lstimes = run.get_lighttimes()
            lsrs = run.get_rints()
            lsgs = run.get_gints()
            
            tubes = run.get_tubes()
            
            gmodel = self.sim(times,p0,g0,self.kp,self.kg,self.tau,lstimes,lsrs,lsgs)[1]
            
            for i in range(len(times)):
                if units == 'afus':
                    sumsq = sumsq + (gmodel[i] - tubes[i].get_amean())**2
                elif units == 'bss':
                    sumsq = sumsq + ((gmodel[i] - tubes[i].get_amean())/tubes[i].get_amean_errs())**2
                elif units == 'errs':
                    sumsq += 1/(self.sserrs(tubes[i].get_amean()))**2 * (gmodel[i] - tubes[i].get_amean())**2
                elif units == 'interrs':
                    j=0
                    while j<len(lstimes)-1 and lstimes[j] < times[i]: j+=1
                    sumsq += 1/(self.interrs(lsrs[j],lsgs[j]))**2 * (gmodel[i] - tubes[i].get_amean())**2
        
        return sumsq
    
    # Minimize self.error by optimizing parameters in params
    def fit(self,kinrunlists,kinmodellists,paramslist,units='errs',fit_errs=False):

        # Make sure paramslist is right
        if len(paramslist) != 3:
            raise ValueError('paramslist argument must contain three lists of parameters specifying how they should be used in the multifit: (all,group,single)')

        # Need an expanded param names slist for the fit function to use
        # Also fill up the default guess list
        fullparamnameslist = []
        guess = []

        # Start with params that are used across all kinruns
        for param in paramslist[0]:
            fullparamnameslist.append(param+'_a')
            guess.append(self.getparam(param))

        # Now the params that are used across groups
        for param in paramslist[1]:
            i=0
            for kinrunlist in kinrunlists:
                fullparamnameslist.append(param+'_g'+str(i))
                guess.append(self.getparam(param))
                i=i+1

        # Finally the params that are separate for each kinrun
        for param in paramslist[2]:
            i=0
            for kinrunlist in kinrunlists:
                for kinrun in kinrunlist:
                    fullparamnameslist.append(param+'_s'+str(i))
                    guess.append(self.getparam(param))
                    i=i+1
        print "Performing fit with {} parameters: {}".format(len(fullparamnameslist),fullparamnameslist)

        # Need to have an error function which explicitly depends on params only
        def errfunc(params):
            # Unpack params into params list for each model according to fullparamnameslist
            for i,fullparamname in enumerate(fullparamnameslist):
                paramname,type = fullparamname.split('_')
                if type[0] == 'a':
                    for kinmodellist in kinmodellists:
                        for kinmodel in kinmodellist:
                            kinmodel.setparam(paramname,params[i])
                elif type[0] == 'g':
                    num = int(type[1:])
                    for kinmodel in kinmodellists[num]:
                        kinmodel.setparam(paramname,params[i])
                elif type[0] == 's':
                    num = int(type[1:])
                    for kinmodellist in kinmodellists:
                        if num < len(kinmodellist):
                            kinmodellist[num].setparam(paramname,params[i])
                        else:
                            num = num - len(kinmodellist)
                else:
                    raise ValueError('Unknown parameter type specification: {}'.format(type))

            num_tubes = 0
            rss = 0
            for i,kinmodellist in enumerate(kinmodellists):
                for j,kinmodel in enumerate(kinmodellist):
                    num_tubes += len(kinrunlists[i][j].get_tubes())
                    rss += kinmodel.error([kinrunlists[i][j]],units)
            return rss

        from scipy.optimize import minimize

        methods=['Nelder-Mead','Powell','CG','BFGS','Newton-CG','Anneal','L-BFGS-B','TNC','COBYLA','SLSQP']

        res = minimize(errfunc,guess,method=methods[3],options={'maxiter': 1e5,'maxfev': 1e5,'disp': True})

        p0 = res['x']

        lastkps = []
        num_tubes = 0
        for i,kinmodellist in enumerate(kinmodellists):
            for j,kinmodel in enumerate(kinmodellist):
                lastkps.append(kinmodel.getparam('kp'))
                num_tubes += len(kinrunlists[i][j].get_tubes())

        if fit_errs:
            import numdifftools as nd

            hess = nd.Hessian(errfunc)
            return [res,kinmodellists,fullparamnameslist,hess(p0),num_tubes]
        else:
            return [res,kinmodellists,fullparamnameslist,num_tubes]

    def program_lsgs(self,gReference,p0=0,g0=0,tEnd=360,tProg=None,tHorizon=40,lsgs_init=None,dt=1,tol=1e-8,max_iter=5,checkExtremes=False,plot=False,movie=False):

        from numpy import linspace

        if tProg == None:
            tProg = [t for t in range(tEnd+1) if t%10 == 0]
        if lsgs_init == None:
            from random import randint
            lsgs_init = [randint(0,4096) for i in range(len(tProg))]

        if len(tProg)!=len(lsgs_init):
            print 'Initial control point array sizes do not match'
            return 0
        else: numC = len(tProg)

        if movie:
            mov_iter=0

        lsrs = [4095 for i in range(len(tProg))]
        lsgs_values = [i for i in range(300) if i%3==0]
        for i in range(300,4095,50): lsgs_values.append(i)
        lsgs_values.append(4095)
        n_lsgs = len(lsgs_values)

        def closest(target, collection):
            return min((abs(target - i), i) for i in collection)[1]

        lsgs = [closest(lsg,lsgs_values) for lsg in lsgs_init]

        def gErrInt(gReference,tProg,tEnd,lsgs,p0,g0,dt=1):

            tStart = 0

            N = (tEnd-tStart)/(dt/2.0)
            if N%2 == 0:
                N += 1
            dt = 1.0*(tEnd-tStart)/N

            tList = linspace(tStart,tEnd,N)
            gS = self.sim(tList,p0,g0,self.kp,self.kg,self.tau,tProg,lsrs,lsgs)[1]
            gD = gReference(tList)

            tListSkip = linspace(tStart,tEndi,(N+1)/2)
            error = 0
            for i in range(len(tListSkip)-1):
                d1 = (gS[2*i] - gD[2*i])**2
                d2 = (gS[2*i+1] - gD[2*i+1])**2
                d3 = (gS[2*i+2] - gD[2*i+2])**2
                error += dt * 1/6. * (d1 + 4*d2 + d3)

            return error

        def f(lsg):
            lsgs_temp = list(lsgs)
            lsgs_temp[tProg.index(t)] = lsg
            return gErrInt(gReference,tProg,tEndi,lsgs_temp,p0,g0,dt)

        iter = 0
        prevErr = 1.0e10
        currErr = 1.0e10
        withinTol = False

        if plot or movie:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            fig.show()

            def gC(tList,tProg,lsgs,scaled=False):
                gCon = [0]*tList
                iC = 0
                tNext = tProg[iC]

                for i,t in enumerate(tList):
                    if t >= tNext:
                        if iC < len(tProg)-1:
                            iC += 1
                            tNext = tProg[iC]
                        else:
                            iC += 1
                            tNext = 1000
                    gCon[i] = lsgs[iC-1]

                if scaled: return [self.ss(4095,gCon[i]) for i in range(len(gCon))]
                else: return gCon

        while not withinTol and iter != max_iter:

            for i,t in enumerate(tProg):

                if i == len(tProg)-1:
                    tEndi = tEnd
                else:
                    tEndi = tProg[i+1] + tHorizon
                    if tEndi > tEnd: tEndi=tEnd

                currErr = f(lsgs[i])
                iStartErr = currErr
                cS = lsgs[i]

                goUp = False
                goDown = False
                wentUp = False
                wentDown = False
                if lsgs[i] == 0:
                    testErr = f(lsgs_values[1])
                    if testErr < currErr: goUp = True
                if lsgs[i] == 4095:
                    testErr = f(lsgs_values[-2])
                    if testErr < currErr: goDown = True
                else:
                    currC = lsgs_values.index(lsgs[i])
                    testU = f(lsgs_values[currC+1])
                    testD = f(lsgs_values[currC-1])
                    if testU < testD:
                        goUp = True
                        testErr = testU
                    elif testD < testU:
                        goDown = True
                        testErr = testD

                while goUp:
                    wentUp = True
                    currC = lsgs_values.index(lsgs[i])
                    testErr = f(lsgs_values[currC+1])
                    if currErr < testErr: goUp = False
                    else:
                        lsgs[i]=lsgs_values[currC+1]
                        currErr = testErr
                        if currC+1 == n_lsgs-1: goUp = False
                while goDown:
                    wentDown = True
                    currC = lsgs_values.index(lsgs[i])
                    testErr = f(lsgs_values[currC-1])
                    if currErr < testErr: goDown = False
                    else:
                        lsgs[i]=lsgs_values[currC-1]
                        currErr = testErr
                        if currC-1 == 0: goDown = False

                # check that the extreme cases are not better
                if checkExtremes:
                    if wentUp and lsgs[i] != 1:
                        if f(1) < currErr:
                            print 'Extreme of 1 chosen'
                            lsgs[i] = 1.0
                    if wentDown and lsgs[i] != 0:
                        if f(0) < currErr:
                            print 'Extreme of 0 chosen'
                            lsgs[i] = 0.0

                if i < len(tProg)-1:
                    pass

                print '------------------------------------'
                print 'iter: {:d}\ttS: {:1g}'.format(iter+1,t)
                print 'cS: {:g}\tcE: {:g}\tstartErr: {:g}\tfinishErr: {:g}'.format(cS,lsgs[i],iStartErr,currErr)

                if plot:
                    times = linspace(0,tEnd,tEnd/dt)
                    pOptPlt,gOptPlt = self.sim(times,p0,g0,self.kp,self.kg,self.tau,tProg,lsrs,lsgs)
                    gDesPlt = gReference(times)
                    gConPlt = gC(times,tProg,lsgs,scaled=True)
                    plt.clf()
                    plt.plot(times,gDesPlt,'g--',label="Ref. signal")
                    plt.plot(times,pOptPlt,'b-',label="p(t)")
                    plt.plot(times,gOptPlt,'g-',label="g(t)")
                    plt.plot(times,gConPlt,'r--',label="Light program")
                    plt.legend()
                    plt.ylim([0,90])
                    fig.canvas.draw()
                if movie:
                    times = linspace(0,tEnd,tEnd/dt)
                    pOptPlt,gOptPlt = self.sim(times,p0,g0,self.kp,self.kg,self.tau,tProg,lsrs,lsgs)
                    gDesPlt = gReference(times)
                    gConPlt = gC(times,tProg,lsgs,scaled=True)
                    plt.clf()
                    plt.plot(times,gDesPlt,'g--',times,pOptPlt,'b-',times,gOptPlt,'g-', times,gConPlt,'r--')
                    plt.ylim([0,90])
                    plt.savefig('./movie/'+'mov{}'.format(mov_iter))
                    mov_iter += 1

            currErr = gErrInt(gReference,tProg,tEndi,lsgs,p0,g0,dt)
            relChange = abs(currErr-prevErr)/currErr
            print 'currErr: {:g}\t relChange: {:g}'.format(currErr,relChange)

            if relChange < tol or currErr == 0: withinTol = True
            prevErr = currErr
            iter += 1

        if plot:
            plt.show()

        if iter > max_iter:
            print "Max iterations: {} was reached".format(max_iter)

        return lsgs

    def program_lsrs(self,gReference,p0=0,g0=0,tEnd=360,tProg=None,tHorizon=40,lsrs_init=None,dt=1,tol=1e-8,max_iter=5,checkExtremes=False,plot=False):

        from numpy import linspace

        if tProg == None:
            tProg = [t for t in range(tEnd+1) if t%10 == 0]
        if lsrs_init == None:
            from random import randint
            lsrs_init = [randint(0,4096) for i in range(len(tProg))]

        if len(tProg)!=len(lsrs_init):
            print 'Initial control point array sizes do not match'
            return 0
        else: numC = len(tProg)

        lsgs = [0 for i in range(len(tProg))]
        lsrs_values = [i for i in range(500) if i%5==0]
        for i in range(500,4095,100): lsrs_values.append(i)
        lsrs_values.append(4095)
        n_lsrs = len(lsrs_values)

        def closest(target, collection):
            return min((abs(target - i), i) for i in collection)[1]

        lsrs = [closest(lsr,lsrs_values) for lsr in lsrs_init]

        def gErrInt(gReference,tProg,tEnd,lsrs,p0,g0,dt=1):

            tStart = 0

            N = (tEnd-tStart)/(dt/2.0)
            if N%2 == 0:
                N += 1
            dt = 1.0*(tEnd-tStart)/N

            tList = linspace(tStart,tEnd,N)
            gS = self.sim(tList,p0,g0,self.kp,self.kg,self.tau,tProg,lsrs,lsgs)[1]
            gD = gReference(tList)

            tListSkip = linspace(tStart,tEndi,(N+1)/2)
            error = 0
            for i in range(len(tListSkip)-1):
                d1 = (gS[2*i] - gD[2*i])**2
                d2 = (gS[2*i+1] - gD[2*i+1])**2
                d3 = (gS[2*i+2] - gD[2*i+2])**2
                error += dt * 1/6. * (d1 + 4*d2 + d3)

            return error

        def f(lsr):
            lsrs_temp = list(lsrs)
            lsrs_temp[tProg.index(t)] = lsr
            return gErrInt(gReference,tProg,tEndi,lsrs_temp,p0,g0,dt)

        iter = 0
        prevErr = 1.0e10
        currErr = 1.0e10
        withinTol = False

        if plot:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            fig.show()

            def gC(tList,tProg,lsrs,scaled=False):
                gCon = [0]*tList
                iC = 0
                tNext = tProg[iC]

                for i,t in enumerate(tList):
                    if t >= tNext:
                        if iC < len(tProg)-1:
                            iC += 1
                            tNext = tProg[iC]
                        else:
                            iC += 1
                            tNext = 1000
                    gCon[i] = lsrs[iC-1]

                if scaled: return [self.ss(gCon[i],0) for i in range(len(gCon))]
                else: return gCon

        while not withinTol and iter != max_iter:

            for i,t in enumerate(tProg):

                if i == len(tProg)-1:
                    tEndi = tEnd
                else:
                    tEndi = tProg[i+1] + tHorizon
                    if tEndi > tEnd: tEndi=tEnd

                currErr = f(lsrs[i])
                iStartErr = currErr
                cS = lsrs[i]

                goUp = False
                goDown = False
                wentUp = False
                wentDown = False
                if lsrs[i] == 0:
                    testErr = f(lsrs_values[1])
                    if testErr < currErr: goUp = True
                if lsrs[i] == 4095:
                    testErr = f(lsrs_values[-2])
                    if testErr < currErr: goDown = True
                else:
                    currC = lsrs_values.index(lsrs[i])
                    testU = f(lsrs_values[currC+1])
                    testD = f(lsrs_values[currC-1])
                    if testU < testD:
                        goUp = True
                        testErr = testU
                    elif testD < testU:
                        goDown = True
                        testErr = testD

                while goUp:
                    wentUp = True
                    currC = lsrs_values.index(lsrs[i])
                    testErr = f(lsrs_values[currC+1])
                    if currErr < testErr: goUp = False
                    else:
                        lsrs[i]=lsrs_values[currC+1]
                        currErr = testErr
                        if currC+1 == n_lsrs-1: goUp = False
                while goDown:
                    wentDown = True
                    currC = lsrs_values.index(lsrs[i])
                    testErr = f(lsrs_values[currC-1])
                    if currErr < testErr: goDown = False
                    else:
                        lsrs[i]=lsrs_values[currC-1]
                        currErr = testErr
                        if currC-1 == 0: goDown = False

                # check that the extreme cases are not better
                if checkExtremes:
                    if wentUp and lsrs[i] != 1:
                        if f(1) < currErr:
                            print 'Extreme of 1 chosen'
                            lsrs[i] = 1.0
                    if wentDown and lsrs[i] != 0:
                        if f(0) < currErr:
                            print 'Extreme of 0 chosen'
                            lsrs[i] = 0.0

                if i < len(tProg)-1:
                    pass

                print '------------------------------------'
                print 'iter: {:d}\ttS: {:1g}'.format(iter+1,t)
                print 'cS: {:g}\tcE: {:g}\tstartErr: {:g}\tfinishErr: {:g}'.format(cS,lsrs[i],iStartErr,currErr)

                if plot:
                    times = linspace(0,tEnd,tEnd/dt)
                    pOptPlt,gOptPlt = self.sim(times,p0,g0,self.kp,self.kg,self.tau,tProg,lsrs,lsgs)
                    gDesPlt = gReference(times)
                    gConPlt = gC(times,tProg,lsrs,scaled=True)
                    plt.clf()
                    plt.plot(times,gDesPlt,'g--',label="Ref. signal")
                    plt.plot(times,pOptPlt,'b-',label="p(t)")
                    plt.plot(times,gOptPlt,'g-',label="g(t)")
                    plt.plot(times,gConPlt,'r--',label="Light program")
                    plt.legend()
                    plt.ylim([0,120])
                    fig.canvas.draw()

            currErr = gErrInt(gReference,tProg,tEndi,lsrs,p0,g0,dt)
            relChange = abs(currErr-prevErr)/currErr
            print 'currErr: {:g}\t relChange: {:g}'.format(currErr,relChange)

            if relChange < tol or currErr == 0: withinTol = True
            prevErr = currErr
            iter += 1

        if plot:
            plt.show()

        if iter > max_iter:
            print "Max iterations: {} was reached".format(max_iter)

        return lsrs

    def simnoisy(self,times,pr,pg,lstimes,lsrs,lsgs):

        km = self.__class__()
        pnameslists = self.getparamnames()
        ps = self.getparams()
        perrs = self.geterrs()


        from random import gauss

        for i,pnamelist in enumerate(pnameslists):
            for j, name in enumerate(pnamelist):
                val = max(0,gauss(ps[i][j],perrs[i][j]))
                km.setparam(name,val)

        #Since we know the correlation between b and a..

        b = self.getparam('b')
        a = self.getparam('a')
        berr = self.getparamerr('b')
        aerr = self.getparamerr('a')
        p = self.getabcorr()
        z1 = gauss(0,1)
        z2 = gauss(0,1)
        km.setparam('b',b + berr * z1)
        km.setparam('a',a + aerr * (z1*p + z2*(1-p**2)**0.5))

        p0 = g0 = km.ss(pr,pg)

        return km.sim(times,p0,g0,km.kp,km.kg,km.tau,lstimes,lsrs,lsgs)

    def plot(self,run,ax,dataOnly=False,simOnly=False,units = 'interrs'):
        import matplotlib.pyplot as plt

        lstimes = run.get_lighttimes()
        lsrs = run.get_rints()
        lsgs = run.get_gints()
        pr,pg = run.get_pre()
        p0 = g0 = self.ss(pr,pg)

        xd = run.get_times()
        yd = run.get_ameans()

        if units == 'interrs':
            rints = []
            gints = []
            for t in xd:
                j=0
                while j<len(lstimes)-1 and lstimes[j] < t: j+=1
                rints.append(lsrs[j])
                gints.append(lsgs[j])
            ye = [self.interrs(rint,gint) for rint,gint in zip(rints,gints)]
        elif units == 'stdevs':
            ye = [self.sserrs(i) for i in yd]

        x = range(int(xd[-1]+1))
        y1,y2= self.sim(x,p0,g0,self.kp,self.kg,self.tau,lstimes,lsrs,lsgs)

        if dataOnly:
            ax.errorbar(xd,yd,yerr=ye,fmt=None,ecolor='r')
            dof = float(len(run.get_tubes()) - len(self.getparams()))
            err = self.error([run])/dof
            from numpy import sqrt
            ax.set_title('{} - {}'.format(self.getname(),sqrt(err)))
        elif simOnly:
            ax.plot(x,y1,'g-',x,y2,'r-')
        else:
            ax.errorbar(xd,yd,yerr=ye,fmt=None,ecolor='r')
            dof = float(len(run.get_tubes()) - len(self.getparams()))
            err = self.error([run])/dof
            from numpy import sqrt
            ax.set_title('{}'.format(self.getname()))
            ax.plot(x,y1,'g-',x,y2,'r-')

        ax.set_xlim(0,run.get_times()[-1])
        ax.set_ylim(0,120)
