#This script uses the flowAnalysis library to batch-process 64 .fcs files
#acquired for an experiment using the LTA

#Input: .fcs files in a single directory
#Output: a tab-delimited .stats file with statistical parameters for each .fcs file

import flowAnalysis as fa
import numpy as np


####USER-SPECIFIED FILE I/O PARAMETERS####

#.fcs files should be located in 'data_dir' in the format: Data.nnn, where
# nnn begins at data_min and ends at data_max (i.e. Data.001 to Data.064).
data_dir = "./sampleData"
data_min = 1
data_max = 4

# outfile_name is the prefix given to the output .stats file
outfile_name = 'SampleData_output'

# hisogtam plots can be generated for each tube. A folder labelled 'plt' should
# be in the same directory as this script for these histogram plots.
hist_plots = True


####FCS EXTRACTION####

outfile_stats = outfile_name+'_stats.dat'

filenums = np.arange(data_min,data_max+1)
stats_list = []

#loop through file_list
for num in filenums:
    print "Extracting file {}".format(num)
    data_file = 'Data.{:03d}'.format(num)

    #read fcs
    data_path = data_dir+'/'+data_file
    extracted = fa.extract_fcs(data_path, verbose = False)
    
    #filter events (trimming, min/max values for channels)
    filtered = fa.filter_events(extracted,fsc_min=400,fl1_min=32)
    
    #gate events (types = 'ellipse', 'circle', 'rectangle')
    gated = fa.gate_events(filtered, gate_type = 'ellipse', gate_params = (64,32,28))
    
    #transform events from logamp values (0-1023) to linear values (1-10000)
    transformed = fa.transform_events(gated)
    
    #reshape the event list by channel instead of event
    channels = fa.events_to_channels(transformed)
    
    #get stats on the fl1 channel and append to stats list
    fl1 = channels[2]
    fl1stats = fa.stats(fl1)
    fl1stats['num'] = num
    fl1stats['counts'] = len(gated)
    fl1stats['%gated'] = len(gated)/float(len(extracted[0]))
    stats_list.append(fl1stats)
    
    if hist_plots:
        import matplotlib.pyplot as plt
        fa.hist_plot(fl1,"plt/"+outfile_name+"_t{}".format(num),xmin=10**0,xmax=10**4, label='FL1 value')

#write stats to file
stats_keys = ['num','amean','rcv','counts','%gated']
o = open(outfile_stats,'w')
for key in stats_keys:
    o.write('#{}\t'.format(key))
o.write('\n')
for stat_dict in stats_list:
    for key in stats_keys:
        o.write('{:.5e}\t'.format(stat_dict[key]))
    o.write('\n')
o.close()
   