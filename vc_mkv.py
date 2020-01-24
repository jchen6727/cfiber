from neuron import h
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
# example use:
# simdata = vc()
# plot_data( title = "gna17a_states", xlabel = "t (m/s)", ylabel = "states", xdata = simdata['t'], labels = ['O2', 'O1', 'C2', 'C1', 'I2', 'I1'], ydatas = [simdata[40]['O2'], simdata[40]['O1'], simdata[40]['C2'], simdata[40]['C1'], simdata[40]['I2'], simdata[40]['I1']] )
# plot_states("na17a_40mV", simdata['t'], simdata[40])
h.load_file("stdrun.hoc")

# gna + state variables
vc_mkv_states = [
    'gna', 'C1', 'C2', 'I1', 'I2', 'O1', 'O2'
]

# rate variables
vc_mkv_rates = [
    'C1C2_a', 'C2C1_a', 'C2O1_a', 'O1C2_a',
    'C2O2_a', 'O2C2_a', 'O1I1_a', 'I1O1_a',
    'I1I2_a', 'I2I1_a', 'I1C1_a', 'C1I1_a'
    ]

# all variables
vc_mkv_vars = [
    'gna', 'C1', 'C2', 'I1', 'I2', 'O1', 'O2',
    'C1C2_a', 'C2C1_a', 'C2O1_a', 'O1C2_a',
    'C2O2_a', 'O2C2_a', 'O1I1_a', 'I1O1_a',
    'I1I2_a', 'I2I1_a', 'I1C1_a', 'C1I1_a'
    ]

# specific voltage clamp for markov models
def vc(chan = "na17a", vstart = -150, vstep = 0, vstop = -150, dur = [5,5,5], skip = [True, False, True], dt = 0.025, vars = vc_mkv_vars):
    simdata = {'chan': chan, 'vars': vars, 'vstart':vstart, 'vsteps':vsteps, 'vstop': vstop, 'dur': dur, 'dt': dt}
    h.dt = dt
    h.steps_per_ms = 1/h.dt
    h.tstop = dur[0]+dur[1]+dur[2]

    h.v_init = vstart

    h.celsius = 36

    secs = [] #sections
    vcs  = [] #voltage clamps
    rvs  = {} #record  vectors
    

    sec = h.Section()
    sec.insert(chan)
    secs.append(sec)

# normalize gna -> gnabar = 1
    exestr = "sec.gnabar_%s = 1" %(chan)
    exec(exestr)
    vc = h.VClamp(sec(0.5))
    vc.dur[0], vc.dur[1], vc.dur[2] = dur[0], dur[1], dur[2]
    vc.amp[0], vc.amp[1], vc.amp[2] = vstart, vstep, vstop
    vcs.append(vc)
    rvs[vstep] = {}
    for var in vars:
        rv = h.Vector()
        exestr = "rv.record(sec(0.5)._ref_%s_%s)" %( var, chan )
        exec(exestr)
        rvs[vstep][var] = rv


    tv = h.Vector()
    tv.record(h._ref_t)
    
    h.t = 0
    h.stdinit()

    for i, dur_ in enumerate(dur_):
        if skip[i]:
            h.dt = dur_
            h.steps_per_ms = 1/h.dt
        h.continuerun(dur_)
        h.dt = dt
        h.steps_per_ms = 1/h.dt

    for var in vars:
        simdata[vstep][var] = [ val for val in rvs[vstep][var] ]
    
    t = [t for t in tv]
    simdata['t'] = t

    return simdata
   
def plot_data( title = "title", xlabel = "xlabel", ylabel = "ylabel", xdata = [0], labels = ['0'], ydatas = [ [0] ] ):
    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.set_title(title)

    for i, label in enumerate(labels):
        ax.plot(xdata, ydatas[i], label = label)

    ax.legend()
    plt.savefig( title + ".png")

    plt.cla()
    plt.clf()
    plt.close()

def get_rates( simdata ):
    ydatas_dict = {}
    ydatas_list = []
    index = int(simdata['dur'][0]/simdata['dt']) + 1
    for rate in vc_mkv_rates:
        ydatas_dict[rate] = [  simdata[v][rate][index] for v in simdata['vsteps'] ]
        ydatas_list.append(ydatas_dict[rate])

    plot_data(title = simdata['chan'] + '_rates', xlabel = 'voltage (mV)', xdata = simdata['vsteps'], ylabel = "rate", labels = vc_mkv_rates, ydatas = ydatas_list )
    return ydatas_dict, ydatas_list


def plot_states( title, simdata_t, simdata_v):
# specifically for the MM channels
# feed time vector, simdata for specific voltage
#
#    Markov Model State Diagram
#                C1
#            <->    <->
#  I2 <-> I1            C2 <-> O2
#            <--    <->
#                O1

    C1, C2, O1, O2, I1, I2 = simdata_v['C1'], simdata_v['C2'], simdata_v['O1'], simdata_v['O2'], simdata_v['I1'], simdata_v['I2']
    pts = range(len(simdata_t))    
# get plot data visualized
    I1 = [ I2[x] + I1[x] for x in pts ]
    C1 = [ I1[x] + C1[x] for x in pts ]
    C2 = [ C1[x] + C2[x] for x in pts ]
    O1 = [ C2[x] + O1[x] for x in pts ]
    O2 = [ O1[x] + O2[x] for x in pts ]
    


    fig, ax = plt.subplots()
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("state populations")
    
    ax.fill_between(simdata_t, O1, O2, color = "#64FF00", label = "O2")
    ax.fill_between(simdata_t, C2, O1, color = "#00FF80", label = "O1")
    ax.fill_between(simdata_t, C1, C2, color = "#00D0FF", label = "C2")
    ax.fill_between(simdata_t, I1, C1, color = "#3800FF", label = "C1")
    ax.fill_between(simdata_t, I2, I1, color = "#D800FF", label = "I1")
    ax.fill_between(simdata_t, 0 , I2, color = "#FF0000", label = "I2")

    ax.legend()
    plt.savefig( title + ".png")

    plt.cla()
    plt.clf()
    plt.close()