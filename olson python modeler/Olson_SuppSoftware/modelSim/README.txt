modelSim.py is a script for simulating the response to different light imputs of the Cph8/OmpR (rd), CcaS/CcaR (rg), or CcaS/CcaR + TetR (rgtet) systems.

The light program is a series of step functions with time points and red/green light intensities specified for each point.

The simulation takes the user-defined light program and determines the response of the specified system. The response of both p(t), the gfp production rate, and g(t), the gfp fluorescence, are computed.

A plot is produced showing:

p(t) in red
g(t) in black
and the light input converted to fluorescence through the steady-state transfer function of the system in green