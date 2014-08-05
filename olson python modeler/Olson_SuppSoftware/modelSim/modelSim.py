import sys
sys.path.append('../util/')

from lpge_easysim import easysim
import matplotlib.pyplot as plt
import numpy as np

# Set sys to 'rg', 'rd', or 'rgtet'
ls = 'rgtet'

# If noise = True, the simulation will be performed using model parameters
#which have individually been perturbed from their fit values by sampling
#a gaussian distribution centered at the best fit value with a s.d. equal to
#the standard error of the fit parameter
noise = False

#t_end is the end time for the simulation, and N_t is the number of time ponts
#to be calculated
t_end = 720
N_t = 181

times = np.linspace(0,t_end,N_t)

# p_r and p_g are the preconditioning red and green light intensities
# l_t are the time points at which the light intensities change
# l_r and l_g are the light intensities corresponding to each time in l_t
p_r = 4095
p_g = 0
l_t = [0,90,360,540]
l_r = [4095,4095,4095,4095]
l_g = [4095,0,4095,0]

# Use the appropriate model
if ls == 'rg':
    from KinModelRG import KinModelRG
    model = KinModelRG()
elif ls == 'rgtet':
    from KinModelRG_Tet import KinModelRG_Tet
    model = KinModelRG_Tet()
elif ls == 'rd':
    from KinModelRD import KinModelRD
    model = KinModelRD()

# Set up a kinrun dictionary for easysim
kinrun = {  'l_pr': p_r, \
            'l_pg': p_g, \
            'l_t': l_t, \
            'l_r': l_r, \
            'l_g': l_g
         }

# Run the simulation using easysim
ts, ps, gs = easysim(kinrun,ls,times,noise=noise)

# ts are the time points for the simulation
# ps are the gfp production rates corresponding to each time in ts
# gs are the fluorescence values corresponding to each time in ts

# Turn the output lists into numpy arrays for ease-of-use
ts = np.array(ts)
ps = np.array(ps)
gs = np.array(gs)
l_r = np.array(l_r)
l_g = np.array(l_g)

# Plot ps, gs, and light input converted to fluorescence through the
#steady-state transfer function
# production rates are red
# gfp fluorescence is black
# light intensity converted to fluorescence through sstf is green
plt.plot(ts,ps,'r-')
plt.plot(ts,gs,'k-')
plt.step(l_t,model.ss(l_r,l_g),'g-',drawstyle="steps-post")
plt.legend(['Production rate', 'GFP', 'Light input in F. units'])
plt.xlabel('Time (min)')

plt.show()