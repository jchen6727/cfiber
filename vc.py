from neuron import h
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

h.load_file("stdrun.hoc")

# fit functions
# curves will fit to these functions

def fx_hh( t , minf, mtau, hinf, htau):
# Hodgkin Huxley equation with m0 and h0 taken to be 0 and 1 
# respectively -- so start at a very hyperpolarized voltage
    m = minf - minf*np.exp(-t/mtau)
    h = hinf + (1 - hinf)*np.exp(-t/htau)
    return m*m*m*h

def fx_ab( v , a0, b0, delta, s):
# calculate values to determine the A(v), B(v) values to fit
# (A(v) B(v) being forward and backward rate functions of v)
# NB, many different possible functions can be 
# used here
    A = a0*np.exp(    -delta*v /s  )
    B = b0*np.exp(  (1-delta)*v/s  )

    return A / (A + B)


def fx_bz( v , v2m, sm):
# Boltzmann function which can be taken from ab
    f = ( v - v2m ) / sm
    return 1 / (1 + np.exp(f))

def vc(chan = "hh", record = "gna", vstart = -150, vsteps = range(-50, 50, 10), vstop = 0, dur = [25,25,25], gna_normalize = True):
    varstr = record + "_" + chan
    simData = {'sim':varstr, 'vstart':vstart, 'vsteps':vsteps, 'vstop': vstop, 'dur': dur, 'dt': h.dt}
    h.tstop = dur[0]+dur[1]+dur[2]
    secs = [] #sections
    vcs  = [] #voltage clamps
    rvs  = [] #record  vectors
    
    for vstep in vsteps:
        sec = h.Section()
        sec.insert(chan)
        secs.append(sec)
        
        if gna_normalize:
            if chan == "hh":
                sec.gnabar_hh = 1
            else: 
                exestr = "sec.gbar_" + chan + " = 1"
                exec(exestr)
        vc = h.VClamp(sec(0.5))
        vc.dur[0], vc.dur[1], vc.dur[2] = dur[0], dur[1], dur[2]
        vc.amp[0], vc.amp[1], vc.amp[2] = vstart, vstep, vstop
        vcs.append(vc)

        rv = h.Vector()
        if (record == "ina"):
            rv.record(sec(0.5)._ref_ina)
        else:
            exestr = "rv.record(sec(0.5)._ref_" + varstr + ")"
            exec(exestr)
        rvs.append(rv)


    t = [x * h.dt for x in range( int(h.tstop/h.dt) + 1 )]

    h.t = 0
    h.finitialize(vstart)
    h.fcurrent()
    h.run()

    for i, rv in enumerate(rvs):
        rv = [rv_ for rv_ in rv]
        rvs[i] = rv

    fig, ax = plt.subplots()
    ax.set_xlabel("time (ms)")

    ax.set_ylabel(record)

    ax.set_title( varstr + "_vclamp_" + str(vstart) + "__E--" + str(vstop))
    
    simData['t'] = t
    for i, vstep in enumerate(vsteps):
        simData[vstep] = rvs[i]
        ax.plot(t, rvs[i], label = str(vstep))

    ax.legend(fontsize=8)
    plt.savefig(varstr + "_vclamp.png")
    # close the plot so you can call it again
    plt.close()
    return simData

def fit_hh( strt, stop, t, gna, bounds = [ [0,0,0,0], [1, np.inf,1,np.inf] ] ):

# def fx_hh( t , minf, mtau, hinf, htau):
#     m = minf - minf*np.exp(-t/mtau)
#     h = hinf + (1 - hinf)*np.exp(-t/htau)
#     return m*m*m*h

# for a high enough voltage, for a long enough time, m->1, h->0
# for a low enough voltage, for a long enough time, m->0, h->1
# if need be can adjust the bounds to take into account other data points.

# just use indexing values for now so can manually adjust window size
    gna = gna[strt:stop]
    # reset window for t to represent new 0
    # maybe use actual t values here in
    # case of vardt? but wouldn't recommend
    # using vardt to evaluate unknown
    # sodium channels...
    t   = t  [:len(gna)]
    popt, pcov = curve_fit(fx_hh, t, gna, bounds = bounds )
    return {'minf': popt[0], 'mtau': popt[1], 'hinf':popt[2], 'htau':popt[3]} , pcov

def fit_bz( v, inf, bounds = [ [-100, 0], [100, np.inf]] ):

# def fx_bz( v , v2m, sm):
#     f = ( v - v2m ) / sm
#     return 1 / (1 + np.exp(f))

# calculate the boltzman constants v2m, sm for a function 
# fx_m(v) = minf
# or fx_h(v) = hinf
# this is to generate a good sigmoid curve when the 
# conductance curve is trivial or m(t)*m(t)*m(t)*h(t)=>0
# for all t
    popt, pcov = curve_fit(fx_bz, v, inf, bounds = bounds)
    return {'v2m': popt[0], 'sm': popt[1]}, pcov

#def fit_ab( v, inf):

# def fx_ab( v , a0, b0, delta, s):
#     A = a0*np.exp(    -delta*v /s  )
#     B = b0*np.exp(  (1-delta)*v/s  )
#     return A / (A + B)


def get_hh(v = 0):
    h.rates_hh(v)
    return {'minf': h.minf_hh, 'mtau': h.mtau_hh, 'hinf': h.hinf_hh, 'htau': h.htau_hh}

def run_hh( strt, stop , chan = 'na19a', record = 'g', vstart = -150, vsteps = range(50,- 75, -5), vstop = -150, dur = [150,150,150]):
    # run voltage high to low
    simData = vc(chan = chan, record = record, vstart = vstart, vsteps=vsteps, vstop = vstop, dur = dur)

    # initialize dictionary to store values
    # reverse how we feed the voltages to
    # fit function to help generate useful
    # bounds
    fitdata = {'v':vsteps}
    hhdata = {'v':vsteps}
    for entry in ['minf', 'mtau', 'hinf', 'htau']:
        fitdata[entry] = []
        hhdata[entry]  = []

    # bounds are for minf, mtau, hinf, htau
    bounds = [ [0, 0, 0, 0], [ 1, np.inf, 1, np.inf ]]
    # set bounds before rinning equation

    for v in fitdata['v']:
    # if we start low v, m(t)*m(t)*m(t)*h(t)=>0 for all
    # t which will give too much freedom to the 
    # curve_fit (...or...gives inappropriate results)
    # so start v high where we know that there will be 
    # a non-trivial function m(t) and h(t) and give 
    # boundary data from there
    # 
    # minf should be same or decreasing, hinf should be 
    # same or increasing as v decreases

        fdata, cov = fit_hh(strt, stop, simData['t'], simData[v], bounds)
        edata      = get_hh(v)

        minf = fdata['minf']
        hinf = fdata['hinf']

    # NB that bounds are inclusive.
        bounds = [ [0, 0, hinf, 0], [minf, np.inf, 1, np.inf ] ]
        for entry in ['minf', 'mtau', 'hinf', 'htau']:
            fitdata[entry].append(fdata[entry])
            hhdata[entry].append(edata[entry])

    # run boltzman fit on minf, hinf on good minf, hinf
    # values to get sigmoid curves
    
    # chop out minf and hinf values where fitdata is
    # less than 0

    vs    = [ v for v in fitdata['v'] if v > -65]
    minfs = fitdata['minf'][:len(vs)]
    hinfs = fitdata['hinf'][:len(vs)]

    # run boltzman fit on minf, hinf on good minf, hinf
    # values to get complete sigmoid curve

    m, cov = fit_bz( vs , minfs, bounds = [ [-100, -np.inf], [100, 0]])
    h, cov = fit_bz( vs , hinfs, bounds = [ [-100,  0], [100, np.inf]])

    # we can fit the equations for A and B.    
    fitdata['minf_bz'] = [fx_bz(v, m['v2m'], m['sm']) for v in fitdata['v']]
    fitdata['hinf_bz'] = [fx_bz(v, h['v2m'], h['sm']) for v in fitdata['v']]

    return fitdata, hhdata

def plotData( record, vv, fitdata, hhdata ):

    fig, ax = plt.subplots()
    ax.set_xlabel("voltage (mV)")

    ax.set_ylabel(record)

    ax.set_title( record + "_vclamp")

    ax.plot(vv, fitdata, label = 'fit')
    ax.plot(vv, hhdata, label = 'hh')

    ax.legend(fontsize=8)
    plt.savefig("hh_" + record + "_vclamp.png")
    plt.close()

if __name__ == "__main__":
    print("simData = vc(chan, record, vstart, vsteps, vstop, dur)")
    print("simData.keys()")

