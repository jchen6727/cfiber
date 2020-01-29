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
def deinactivation(chan = "na17a", v = -65, ddur = 500, durstop = 50000):
    adata = {}
    durs = range(0, durstop, ddur)
    adata['dur'] = durs
    adata['gmax'] = []
    for var in vc_mkv_states:
        adata[var] = []
    for dur in durs:
        simdata = voltage_clamp(chan = "na17a", vinit = 150, vstart = v, vstep = 0, dur = [dur, 50, 0], skip = [True, False, False], vars = vc_mkv_states)
        adata['gmax'].append(max(simdata['gna']))
        for var in vc_mkv_states:
            adata[var].append(simdata[var][1])
    return adata
    

def inactivation(chan = "na17a", v = -65, ddur = 500, durstop = 50000):
# study voltage dependence of inactivation
# O1 -> I1 -> I2
    idata = {}
    durs  = range(0, durstop, ddur)
    idata['dur'] = durs
    idata['gmax'] = []
    for var in vc_mkv_states:
        idata[var] = []
    for dur in durs:
        simdata = voltage_clamp(chan = "na17a", vstart = v, dur = [dur, 50, 0], skip = [True, False, False], vars = vc_mkv_states)
        idata['gmax'].append(max(simdata['gna']))
        for var in vc_mkv_states:
            idata[var].append(simdata[var][1])
    return idata

def voltage_clamp(chan = "na17a", vinit = -150, vstart = -150, vstep = 0, vstop = -150, dur = [50,50,50], skip = [False, False, False], dt = 0.025, vars = vc_mkv_vars):
    simdata = {'chan': chan, 'vars': vars, 'vstart':vstart, 'vstep':vstep, 'vstop': vstop, 'dur': dur, 'dt': dt}
    h.dt = dt
    h.steps_per_ms = 1/h.dt

    h.v_init = vinit

    h.celsius = 36

    rvs  = {} #record  vectors
    
    sec = h.Section()
    sec.insert(chan)

# normalize gna -> gnabar = 1
    exestr = "sec.gnabar_%s = 1" %(chan)
    exec(exestr)
    vc = h.VClamp(sec(0.5))
    vc.dur[0], vc.dur[1], vc.dur[2] = dur[0], dur[1], dur[2]
    vc.amp[0], vc.amp[1], vc.amp[2] = vstart, vstep, vstop

    for var in vars:
        rv = h.Vector()
        exestr = "rv.record(sec(0.5)._ref_%s_%s)" %( var, chan )
        exec(exestr)
        rvs[var] = rv


    tv = h.Vector()
    tv.record(h._ref_t)
    
    h.t = 0
    h.stdinit()

    tstop = 0
    for i, dur_ in enumerate(dur):
        tstop+=dur_
        if skip[i]:
            if dur_ != 0:
                h.dt = dur_
                h.steps_per_ms = 1/h.dt
        h.continuerun(tstop)
        h.dt = dt
        h.steps_per_ms = 1/h.dt

    for var in vars:
        simdata[var] = [ val for val in rvs[var] ]
    
    t = [t for t in tv]
    simdata['t'] = t

    return simdata
   
def plot_data( title = "title", xaxis = "xlabel", yaxis = "ylabel", xdatas = [ [0] ], labels = ['0'], ydatas = [ [0] ] ):
    fig, ax = plt.subplots()
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)

    ax.set_title(title)

    for i, label in enumerate(labels):
        ax.plot(xdatas[i], ydatas[i], label = label)

    ax.legend()
    plt.savefig( title + ".png")

    plt.cla()
    plt.clf()
    plt.close()

def get_rates( chan = "na17a", vs = range(-90,90) ):
# just generate sections no voltage clamps
    sec = h.Section()
    sec.insert(chan)

    rates_dict = {'v': vs}
    for rate in vc_mkv_rates:
        rates_dict[rate] = []
    for v in vs:
        h.v_init = v
        h.stdinit()
        simdata = voltage_clamp( chan = chan, vinit = v, vstart = v, vstep = v, vstop = v, dur = [0,0,0], dt = 1, vars = vc_mkv_rates)
        for rate in vc_mkv_rates:
            rates_dict[rate].append(simdata[rate][0])

    plot_data(title = chan + '_rates', xaxis = 'voltage (mV)', yaxis = "rate", xdatas = [vs for rate in vc_mkv_rates], labels = vc_mkv_rates, ydatas = [rates_dict[rate] for rate in vc_mkv_rates] )
    return rates_dict

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