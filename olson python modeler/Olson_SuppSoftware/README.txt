Four workflows are provided by this code. See the README.txt documents within each workflow's folder for more information.

(1) The 'flowAnalysis' folder contains code for performing data extraction and processing for .fcs files from a flow cytometer.

(2) The 'modelSim' folder contains a script for generating time-course simulations for the RG, RD, and RGTet models for different light program inputs.

(3) The 'modelFitting' folder contains scripts for parameterizing models to gene expression data measured from different light program inputs.

(4) The 'lightProgramGenerator' folder contains a script for generating light input programs for driving the RG, RD, and RGTet models to follow different reference time-courses.

Notes: 

(1) The 'util' folder contains the core code that is utilized by the scripts for workflows (2)-(4). The 'flowAnalysis' folder is self-contained.

(2) There are many places in which improvements could be made, and if the user feels inclined, the authors welcome changes and optimizations. Three particular areas are (A) use of recognized coding standards and best practices (PEP 8), (B) there could be more custom data structures (and more use of existing ones) to handle the data going into and coming out of the programs, and (C) improvements could be made in the speed of the intensity optimization process at each step-change during light program generation.

(3) This code was written for Python 2.7, and relies on the matplotlib, numpy, scipy, and xlrd libraries.