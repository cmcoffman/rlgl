lightProgramGenerator.py is a script for generating a light input program for driving the rg, rd, and rgtet models to follow different reference time-courses.

The user specifies
(1) the system to be used
(2) the reference signal the response of the system should follow
(3) the time points that the light program should change intensity

The algorithm script outputs
(1) an animation during optimization depicting
	(a) reference signal (green dash)
	(b) light input converted through sstf (red dash)
	(c) gfp production rate p(t) (blue line)
	(d) gfp fluorescence g(t) (green line)
(2) a file containing the light program in a format ready to use on the LTA. The file specifies the time points and red/green intensities at each time point.

Options for fine control over the algorithm's operation are documented in the script.

Notes:
(1) The animation will stop updating if the animation window loses focus. At that point it will no longer update until the algorithm has finished.
(2) The algorithm has finished when both the animation and console have stopped updating. Once the plot is closed, the output file will be written.