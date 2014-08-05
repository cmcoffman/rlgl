# flowAnalysis.py
    
from pylab import *
    
def extract_fcs(input_path, verbose = False):
    """
    Attempts to parse an FCS (flow cytometry standard) file. 
    
    Thanks and attribution for the extract_fcs() method:
    
    Andrew Pangborn
    Computer Engineering
    Kate Gleason College of Engineering
    Rochester Institute of Technology
    Rochester, New York
    
    Method found at:
    http://apangborn.com/projects/fcs-extract-python-script/

    Parameters: input_path
        filename: path to the FCS file

    Returns: (events,vars)
    	vars: a dictionary with the KEY/VALUE pairs found in the HEADER
        this includes the standard '$ABC' style FCS variable as well as any 
        custom variables added to the header by the machine or operator

        events: an [N x D] matrix of the data (as a Python list of lists)
        i.e. events[99][2] would be the value at the 3rd dimension
        of the 100th event
    """
    from StringIO import StringIO
    import struct
    
    fcs_file_name = input_path
    
    fcs = open(fcs_file_name,'rb')
    header = fcs.read(58)
    version = header[0:6].strip()
    text_start = int(header[10:18].strip())
    text_end = int(header[18:26].strip())
    data_start = int(header[26:34].strip())
    data_end = int(header[34:42].strip())
    analysis_start = int(header[42:50].strip())
    analysis_end = int(header[50:58].strip())

    if verbose: print "Parsing TEXT segment"
    # read TEXT portion
    fcs.seek(text_start)
    delimeter = fcs.read(1)
    # First byte of the text portion defines the delimeter
    if verbose: print "delimeter:",delimeter
    text = fcs.read(text_end-text_start+1)

    #Variables in TEXT poriton are stored "key/value/key/value/key/value"
    keyvalarray = text.split(delimeter)
    fcs_vars = {}
    fcs_var_list = []
    # Iterate over every 2 consecutive elements of the array
    for k,v in zip(keyvalarray[::2],keyvalarray[1::2]):
        fcs_vars[k] = v
        fcs_var_list.append((k,v)) # Keep a list around so we can print them in order

    #from pprint import pprint; pprint(fcs_var_list)
    if data_start == 0 and data_end == 0:
        data_start = int(fcs_vars['$DATASTART'])
        data_end = int(fcs_vars['$DATAEND'])

    num_dims = int(fcs_vars['$PAR'])
    if verbose: print "Number of dimensions:",num_dims

    num_events = int(fcs_vars['$TOT'])
    if verbose: print "Number of events:",num_events

    # Read DATA portion
    fcs.seek(data_start)
    #print "# of Data bytes",data_end-data_start+1
    data = fcs.read(data_end-data_start+1)

    # Determine data format
    datatype = fcs_vars['$DATATYPE']
    if datatype == 'F':
        datatype = 'f' # set proper data mode for struct module
        if verbose: print "Data stored as single-precision (32-bit) floating point numbers"
    elif datatype == 'D':
        datatype = 'd' # set proper data mode for struct module
        if verbose: print "Data stored as double-precision (64-bit) floating point numbers"
    elif datatype == 'I':
        datatype = 'H' # set proper data mode for struct module
        if verbose: print "Data stored as unsigned binary integers"
    else:
        assert False,"Error: Unrecognized $DATATYPE '%s'" % datatype
    
    # Determine endianess
    endian = fcs_vars['$BYTEORD']
    if endian == "4,3,2,1":
        endian = ">" # set proper data mode for struct module
        if verbose: print "Big endian data format"
    elif endian == "1,2,3,4":
        if verbose: print "Little endian data format"
        endian = "<" # set proper data mode for struct module
    else:
        assert False,"Error: This script can only read data encoded with $BYTEORD = 1,2,3,4 or 4,3,2,1"

    # Put data in StringIO so we can read bytes like a file    
    data = StringIO(data)

    if verbose: print "Parsing DATA segment"
    # Create format string based on endianeness and the specified data type
    format = endian + str(num_dims) + datatype
    datasize = struct.calcsize(format)
    if verbose: print "Data format:",format
    if verbose: print "Data size:",datasize
    events = []
    # Read and unpack all the events from the data
    for e in range(num_events):
        event = struct.unpack(format,data.read(datasize))
        events.append(event)
    
    fcs.close()
    return events, fcs_vars
    
def filter_events(event_data, \
                front_trim = 250, back_trim = 100, fsc_min = 1, fsc_max = 1022, \
                ssc_min = 1, ssc_max = 1022, fl1_min = 0, fl1_max = 1022, \
                fl2_min = 0, fl2_max = 1022, fl3_min = 0, fl3_max = 1022):
    #
    #Accepts a list of events and channel names and filters the list based on the specified
    #parameters. front_trim removes early events, back_trim removes late events. The channel_min
    #args specify low and high thresholds (defaults are set to remove undefined 0 and 1023 values).
    #
    event_list, data_vars = event_data
    num_dims = len(event_list[0])
    channel_keys = ['$P3N', '$P4N', '$P5N']
    channels = [data_vars[key] for key in data_vars if key in channel_keys]
    event_list = event_list[front_trim:-1*back_trim]
    
    event_list = [event for event in event_list if event[0] >= fsc_min and event[0] <= fsc_max]    
    event_list = [event for event in event_list if event[1] >= ssc_min and event[1] <= ssc_max]
    if(num_dims == 5 or num_dims == 6):
        event_list = [event for event in event_list if event[2] >= fl1_min and event[2] <= fl1_max]
        event_list = [event for event in event_list if event[3] >= fl2_min and event[3] <= fl2_max]
        event_list = [event for event in event_list if event[4] >= fl3_min and event[4] <= fl3_max]
    if(num_dims == 4):
        if ('FL1-H' not in channels):
            event_list = [event for event in event_list if event[2] >= fl2_min and event[2] <= fl2_max]
            event_list = [event for event in event_list if event[3] >= fl3_min and event[3] <= fl3_max]
        if ('FL2-H' not in channels):
            event_list = [event for event in event_list if event[2] >= fl1_min and event[2] <= fl1_max]
            event_list = [event for event in event_list if event[3] >= fl3_min and event[3] <= fl3_max]
        if ('FL3-H' not in channels):
            event_list = [event for event in event_list if event[2] >= fl1_min and event[2] <= fl1_max]
            event_list = [event for event in event_list if event[3] >= fl2_min and event[3] <= fl2_max]
    if(num_dims == 3):
        if ('FL1-H' in channels):
            event_list = [event for event in event_list if event[2] >= fl1_min and event[2] <= fl1_max]
        if ('FL2-H' in channels):
            event_list = [event for event in event_list if event[2] >= fl2_min and event[2] <= fl2_max]
        if ('FL3-H' in channels):
            event_list = [event for event in event_list if event[2] >= fl3_min and event[2] <= fl3_max]
    
    return event_list

def gate_events(events, gate_type = None, gate_center = None, gate_params = None):
    #
    #Accepts a list of events and a gating scheme name with associated parameters.
    #Filters the events in the list according to the gate.
    
    import numpy
    from numpy import median, sqrt, cos, sin
    
    if gate_type == None:
        return events
    
    if gate_center == None:
        #use FSC/SSC medians
        gate_center = numpy.median([event[0] for event in events]), numpy.median([event[1] for event in events])
    x0,y0 = gate_center
    
    if gate_type == 'circle':
        radius = gate_params
        gated_events = []
        for event in events:
            x,y = event[0:2]
            dist = sqrt((x-x0)**2 + (y-y0)**2)
            if (dist <= radius): gated_events.append(event)
    if gate_type == 'ellipse':
        xlen, ylen, theta = gate_params
        gated_events = []
        for event in events:
            x,y = event[0:2]
            xt = x0 + (x-x0)*cos(theta) + (y-y0)*sin(theta)
            yt = y0 + (x-x0)*(-1*sin(theta)) + (y-y0)*cos(theta)
            if (((xt-x0)/(xlen/2.0))**2 + ((yt-y0)/(ylen/2.0))**2 < 1): gated_events.append(event)
    if gate_type == 'rectangle':
        if len(gate_params) == 2:
            xlen, ylen = gate_params
            gated_events = []
            for event in events:
                x,y = event[0:2]
                if abs(x-x0) < xlen/2.0 and abs(y-y0) < ylen/2.0: gated_events.append(event)
        if len(gate_params) == 3:
            xlen, ylen, theta = gate_params
            gated_events = []
            for event in events:
                x,y, = event[0:2]
                xt = x0 + (x-x0)*cos(theta) + (y-y0)*sin(theta)
                yt = y0 + (x-x0)*(-1*sin(theta)) + (y-y0)*cos(theta)
                if abs(xt-x0) < xlen/2.0 and abs(yt-y0) < ylen/2.0: gated_events.append(event) 
    return gated_events

def transform_events(events):
    """
    Accepts a list of event lists and transforms them according to the logamp. Returns
    the transformed list in the same format.
    """
    transformed_events = []
    for event in events:
        new_event = []
        for value in event:
            new_event.append(10**(value/256.0))
        transformed_events.append(new_event)
    return transformed_events

def stats(values, return_list = False):
    """
    Accepts a list of values (not events) and processes the data. Will return the stats
    in a dictionary.
    """
    import numpy
    from numpy import mean, exp, median, std, log
    from scipy.stats import mode, variation, scoreatpercentile, skew, kurtosis
    stat_dict = {}

    n = float(len(values))    
    
    keys = ['amean','gmean','median','mode','stdev','cv','iqr','rcv','skew','kurt']    
    
    stat_dict[keys[0]] = mean(values)
    stat_dict[keys[1]] = exp(mean([log(value) for value in values]))
    stat_dict[keys[2]] = median(values)
    stat_dict[keys[3]] = int(mode(values)[0])
    stat_dict[keys[4]] = std(values)
    stat_dict[keys[5]] = variation(values)
    stat_dict[keys[6]] = scoreatpercentile(values,per = 75) - scoreatpercentile(values,per = 25)
    stat_dict[keys[7]] = 0.75*stat_dict['iqr'] / stat_dict['median']    
    stat_dict[keys[8]] = skew(values)
    stat_dict[keys[9]] = kurtosis(values)
    
    if return_list:
        return [stat_dict[key] for key in keys]
    return stat_dict

def events_to_channels(events):
    import numpy
    from numpy import arange
    
    channels = [[] for i in arange(len(events[0]))]
    for i,channel in enumerate(channels):
        for event in events:
            channel.append(event[i])            
    return channels

def hist_plot(values, outfile,dpi = 100,log = True,N=100,xmin = None, xmax = None, label=None):
    """
    Accepts a list of values (not events). Will create a simple plot of the histogram
    with matplotlib and save it to outfile if specified. If no outfile, the plot will
    be sent to the standard matplotlib output terminal.
    """
    
    if not xmin:
        xmin = min(values)
    if not xmax:
        xmax = max(values)
    
    if log == True:
        bins = 10**np.linspace(np.log10(xmin),np.log10(xmax),N)
    else:
        bins = np.linspace(xmin,xmax,N)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(values, bins=bins,histtype='stepfilled')
    if log:
        plt.xscale('log')
    if not label:
        label = 'Value'
    plt.xlabel(label)
    plt.ylabel('Events')
    
    savefig(outfile+".png",dpi=dpi,facecolor='white')
    
    return 1