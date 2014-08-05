modelFitting.py is a script used for parameterizing gene expression models by fitting them to multiple data sets simultaneously. The calibration data used to make the predictive models for each system is included in the data subfolder. The script is set to allow the user to specify the system to be fit (rg, rd, or rgtet). The script will then recapitulate the fit that was used to parameterize the predictive models. After the fit is completed, a plot of the data plus the fit is shown.

Parameters can be flagged to fit in three ways:

(1) A parameter can be global, and will be used across all data sets
(2) A parameter can be localized to one LTA run, which might comprise several different time courses
(3) A parameter can be localized to each time course

Documentation within the script should enable the user to incorporate different excel datasets for fitting if they choose (data sets shown in every figure in the main text are available for download). Furthermore, the user should be able to define a different set of parameters to fit if they choose.

Input:
(1) Excel data files in the 'data' subfolder
(2) Configuration options in the modelFitting.py script

Output:
(1) The best-fit parameters are printed to the console
(2) A plot is generated showing the data and the resulting fit

Note: The 'rg' system takes a while to run - perhaps 10-30 minutes depending on your machine