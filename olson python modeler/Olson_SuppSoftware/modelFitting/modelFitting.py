import sys
sys.path.append('../util/')

from KinModel import KinModel
from KinRun import KinRun
from Tube import Tube

import xlrd

# import_data method
#Imports data from a formatted excel file given the name of the time-course
#Returns a KinRun object containing parsed data and light program
def import_data(tc_name):
    #Parse tc_name to determine system
    if tc_name[0:5] == 'RGTet':
        ls = 'rgtet'
    elif tc_name[0:2] == 'RG':
        ls = 'rg'
    elif tc_name[0:2] == 'RD':
        ls = 'rd'
        
    #Construct path to data file
    path = './data/{}'.format(ls)+'/'+tc_name+'.xls'
    
    #Open data file
    book = xlrd.open_workbook(path)
    sh = book.sheet_by_index(0)
    
    #Parse measured data: (time, GFP)
    row = 2
    d_t = []
    d_g = []
    while sh.cell_value(row,0) not in ['']:
        d_t.append(sh.cell_value(row,0))
        d_g.append(sh.cell_value(row,1))
        row+=1
    
    #Parse light program (time, red, green)
    row = 2
    l_t = []
    l_r = []
    l_g = []
    while sh.cell_value(row,7) not in ['']:
        l_t.append(sh.cell_value(row,7))
        l_r.append(sh.cell_value(row,9))
        l_g.append(sh.cell_value(row,8))
        row+=1
        
    #Make and return a KinRun containing the parsed data and program
    kr = KinRun()
    kr.name = tc_name
    
    kr.times = d_t
    kr.tubes = [Tube(amean=g) for g in d_g]
    
    kr.lighttimes = l_t
    kr.rints = l_r
    kr.gints = l_g
    
    #Unfortunately, the excel files don't contain preconditioning intensities.
    # However, we can figure them out based on the tc_name
    onrun = offrun = False
    if tc_name[2:4] == 'On':
        onrun = True
    if tc_name[2:5] == 'Off':
        offrun = True
        
    num1 = int(tc_name[-3])
    num2 = int(tc_name[-1])
    
    if ls in ['rg','rgtet']:
        p_r = 4095
        if offrun:
            if num1 == 2:
                p_g = 4095
            elif num1 == 3:
                if num2 == 1:
                    p_g = 90
                if num2 == 2:
                    p_g = 140
                if num2 == 3:
                    p_g = 255
                if num2 == 4:
                    p_g = 1023
        else:
            p_g = 0
    if ls in ['rd']:
        p_g = 0
        if offrun:
            p_r = 0
        else:
            p_r = 4095
            
    kr.preR = p_r
    kr.preG = p_g
    
    return kr

###############################
#### FIT SETUP BEGINS HERE ####
###############################

# Set sys to 'rg', 'rd', or 'rgtet'
#This sets the model and the error mode used by the fit
#errs maps the error using the sstf-scatter by sstf->error
#interrs maps the error using the sstf-scatter by intensity->error
#These error modes were chosen empirically based on observation
ls = 'rd'

if ls == 'rg':
    from KinModelRG import KinModelRG
    model = KinModelRG()
    units = 'errs'
elif ls == 'rgtet':
    from KinModelRG import KinModelRG
    model = KinModelRG()
    units = 'errs'
elif ls == 'rd':
    from KinModelRD import KinModelRD
    model = KinModelRD()
    units = 'interrs'

# Define the LTA runs associated with fitting each system with the following
#format: (LTA_run_name, num_time_courses) where num_time_courses is the number
#of time courses performed in each LTA run.
rgruns = (
            ('RGOffKinCal2',4),
            ('RGOffKinCal3',4),
            ('RGOnKinCal4',4),
            ('RGOnKinCal5',4),
            ('RGProgAccel1p1',4),
            ('RGProgAccel1p2',4),
            ('RGProgArb1p1',1),
            ('RGProgArb1p2',1)
        )
        
rgtetruns = (
            ('RGTetArb2p2_fl1',1),
        )

rdruns = (
            ('RDOffKinCal2',4),
            ('RDOffKinCal3',4),
            ('RDOnKinCal1',4),
            ('RDOnKinCal2',4)
        )
        
# Load data and assemble the data into a nested list, with each interior list 
#containing time-courses from within a single LTA run
if ls == 'rg':
    runs = rgruns
elif ls == 'rgtet':
    runs = rgtetruns
elif ls == 'rd':
    runs = rdruns

runlist = []
for i,run in enumerate(runs):
    run_name, num_runs = run
    runlist.append([])
    
    for j in range(num_runs):
        time_course_name = run_name + 'p{}'.format(j+1)
        runlist[i].append(import_data(time_course_name))

# Prepare a model instance to store individual values for each time-course
#The modelists has the same nested format as the runlist
modellist = []
for i,run in enumerate(runlist):
    modellist.append([])
    
    for time_course in run:
        if ls == 'rg':
            modellist[i].append(KinModelRG(name='fitto_'+time_course.get_name()))
        elif ls == 'rgtet':
            modellist[i].append(KinModelRG(name='fitto_'+time_course.get_name()))
        elif ls == 'rd':
            modellist[i].append(KinModelRD(name='fitto_'+time_course.get_name()))

# paramstofit contains three tuples. Parameters in the first tuple are global - 
#they will be fit as a single parameter across all time-courses. Parameters in 
#the second tuple are local to each LTA run, and those in the third tuple will
#be fit locally to each time-course.
# The parameter names should match those used in the KinModelRD, KinModelRG, and
#KinModelRG_Tet classes.
if ls == 'rg':
    paramstofit = (('kg','kpl','kpm','kpo','kpk'),('tau','a','b'),())
elif ls == 'rgtet':
    paramstofit = (('kg',),(),())
elif ls == 'rd':
    paramstofit = (('kg','kp','n','k'),('a','b'),())

# Perform fit
res,modellists,fullparamlist,num_tubes = model.fit(runlist,modellist,paramstofit,units=units)

# Write result to console
paraminfo = zip(fullparamlist,res['x'])
dof = float(num_tubes - len(fullparamlist))
var = res['fun']/dof

print 'Residual: {}'.format(res['fun'])
print 'DOF: {}'.format(dof)
print 'Res/DOF: {}'.format(res['fun']/dof)

print 'Params: {}'.format(paraminfo)

# Plot data and fits
import matplotlib.pyplot as plt

ni = len(modellists)
nj = max([len(modellist) for modellist in modellists])
nj = max(nj,2)

fig, axes = plt.subplots(nrows=ni,ncols=nj)

fig.set_size_inches(nj*5,ni*2,forward=True)

if ni == 1 or nj == 1: axes = [axes]

for i,modellist in enumerate(modellists):
    for j,model in enumerate(modellist):
        model.plot(runlist[i][j],axes[i][j],units='stdevs')
plt.tight_layout()
plt.show()
