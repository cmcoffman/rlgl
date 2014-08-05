flowAnalysis.py contains methods for performing extraction, trimming, gating, and calculation of statistics from .fcs files.

extractScript.py contains a script for batch processing a directory with .fcs files. It depends on the methods in flowAnalysis.py.

Note: As the flowAnalysis.py is currently written, the matplotlib library is required. This dependency could be removed with a little work. 

When running extractScript.py:

Input:
Sample data has been provided (in the sampleData folder), and the script is current set to analyze it.

Output:
(1) A .dat file (tab delimited) containing the statistics generated for each tube including:
num: an index for each file
amean: the arithmetic mean of the FL1 of the population
rcv: the robust CV of the FL1 of the population (calculated as 0.75 * IQR / median)
counts: the number of cells after gating
%gated: the percent of cells remaining after the gate

(2) Histogram plots of the FL1 channel for each tube (in the 'plt' subfolder)