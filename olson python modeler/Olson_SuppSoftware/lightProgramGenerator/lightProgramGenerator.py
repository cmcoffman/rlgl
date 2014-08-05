import sys
sys.path.append('../util/')

import numpy as np

# Set sys to 'rg', 'rd', or 'rgtet'
ls = 'rg'

if ls == 'rg':
    from KinModelRG import KinModelRG
    m1 = KinModelRG()
elif ls == 'rgtet':
    from KinModelRG_Tet import KinModelRG_Tet
    m1 = KinModelRG_Tet()
elif ls == 'rd':
    from KinModelRD import KinModelRD
    m1 = KinModelRD()

# Specify the reference signal (some examples are provided)
# types are 'accel','linear','sine', and 'arb'
# num can be used to easily generate variations of each type of signal
# saveFile tells the program to save the optimized light program
type = 'arb'
num=1
saveFile = False

a = m1.getparam('a')
b = m1.getparam('b')
def gReferenceSingle(t):
    if type == 'accel':
        return b+0.15*num*a
    elif type == 'linear':
        return b + num*0.2*a*t/180.0
    elif type == 'sine':
        if t<450: return b+0.5*a - 0.4*a*np.cos(2*np.pi*t/360)
        else: return b+a*0.5 + 0.2*a*np.sin(2*np.pi*(t-450)/180)
    elif type == 'arb':
        if t < 150: return b + 0.7*a*t/150
        elif t < 210: return b+0.7*a
        elif t < 300: return b+0.7*a-0.2*a*(t-210)/90
        elif t < 360: return b+0.5*a
        elif t < 660: return b+0.5*a-0.3*a*np.sin(2*np.pi*(t-360)/300)
        else: return b+0.5*a

def gReference(tList):
    return [gReferenceSingle(t) for t in tList]

#The range for the time-course simulations is [0,tEnd], where tEnd is in minutes.
#tProg specifies the time points that should step-changes should occur in the 
# optimized light program
if type == 'accel' or type == 'linear':
    tEnd = 240
    tProg = [6*i for i in range(17)]
if type == 'sine' or type == 'arb':
    tEnd = 720
    tProg = [10*i for i in range(71)]




#ls_init specifies the the initial guess light-program fed into the algorithm
# it will be used as green intensities for rg and rgtet (red inten = 4095)
# and it will be used as red intensities for rd (green inten = 0)
ls_init = [132 for i in range(len(tProg))]

#p_r and p_g are the preconditioning light intensities
p_r = 4095
p_g = 0
p0 = g0 = m1.ss(p_r,p_g)

# Perform the optimization
# The optimization of each itensity is performed from the begining of the step
#being optimized to the end of the next step plus an additional time horizon
# tHorizon specifies the additional time horizon used
# dt is the time step used during the integration of the error between
#simulation and reference
# tol is the relative difference in error between two full rounds of program
#optimization that will trigger the optimization to stop
# max_iter is the maximum number of iterations allowed
# Note: the program will stop when either tol or max_iter have been reached
# plot is used to show a plot animating the algorithm's progress
tHorizon = 20
dt = 1
tol = 1e-3
max_iter = 5
checkExtremes = False
if ls in ['rg','rgtet']:
    ls_opt = m1.program_lsgs(gReference,p0=p0,g0=g0,tEnd=tEnd,tHorizon=tHorizon,tProg=tProg,lsgs_init=ls_init,dt=dt,tol=tol,max_iter=max_iter,plot=True)
elif ls in ['rd']:
    ls_opt = m1.program_lsrs(gReference,p0=p0,g0=g0,tEnd=tEnd,tHorizon=tHorizon,tProg=tProg,lsrs_init=ls_init,dt=dt,tol=tol,max_iter=max_iter,plot=True)

#print the result to console
print ls_opt

#save the result in a format ready to read by the LTA
outfile = '{}_{}{}.dat'.format(ls,type,num)
if saveFile:
    o = open(outfile,'w')
    if ls in ['rg','rgtet']:
        o.write('int numPoints'+str(num)+' = {};\n'.format(len(tProg)))
        o.write('long times'+str(num)+'[] = {')
        for time in tProg[:-1]: o.write('{:d},'.format(time))
        o.write('{:d}}};'.format(tProg[-1]))
        o.write('\nint red'+str(num)+'[] = {')
        for lsr in ls_opt[:-1]: o.write('{:d},'.format(4095))
        o.write('{:d}}};'.format(4095))
        o.write('\nint green'+str(num)+'[] = {')
        for lsg in ls_opt[:-1]: o.write('{:d},'.format(lsg))
        o.write('{:d}}};'.format(ls_opt[-1]))
    elif ls in ['rd']:
        o.write('int numPoints'+str(num)+' = {};\n'.format(len(tProg)))
        o.write('long times'+str(num)+'[] = {')
        for time in tProg[:-1]: o.write('{:d},'.format(time))
        o.write('{:d}}};'.format(tProg[-1]))
        o.write('\nint red'+str(num)+'[] = {')
        for lsr in ls_opt[:-1]: o.write('{:d},'.format(lsr))
        o.write('{:d}}};'.format(ls_opt[-1]))
        o.write('\nint green'+str(num)+'[] = {')
        for lsg in ls_opt[:-1]: o.write('{:d},'.format(0))
        o.write('{:d}}};'.format(0))
    o.close()