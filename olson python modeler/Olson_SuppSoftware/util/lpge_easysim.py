from KinModelRG import KinModelRG
mRG = KinModelRG()

from KinModelRG_Tet import KinModelRG_Tet
mRGT = KinModelRG_Tet()

from KinModelRD import KinModelRD
mRD = KinModelRD()

from numpy import linspace

from random import gauss

def easysim(kinrun,sys,times=None,N=100,noise=False):
    '''
    Performs a simulation run of a specified system.
    
    Arguments:
        kinrun: Dictionary containing simulation parameters
        sys:    Contains the name of the system to be simulated.
        times:  Array containing times for desired output values.
        N:      Number of time points; only used if time array not specified
        noise:  Whether to add noise to the simulation
    '''
    
    # Import appropriate model
    sys = sys.lower()
    if sys == 'rg':
        km = mRG
    elif sys == 'rgtet':
        km = mRGT
    elif sys == 'rd':
        km = mRD
    else:
        raise ValueError("Type of system not recognized: " + str(sys))
        
    # Define time array if not defined
    if times == None:
        times = linspace(0,kinrun['d_t'][-1]+5,N)
    
    # Extract simulation parameters
    preR = kinrun['l_pr']
    preG = kinrun['l_pg']
    p0 = g0 = km.ss(preR,preG)
    lstimes = kinrun['l_t']
    lsrs = kinrun['l_r']
    lsgs = kinrun['l_g']
        
    # Perform simulation
    if noise:
        ps, gs = km.simnoisy(times,preR,preG,lstimes,lsrs,lsgs)
    else:
        ps, gs = km.sim(times,p0,g0,km.kp,km.kg,km.tau,lstimes,lsrs,lsgs)
        
    return [times,ps,gs]

