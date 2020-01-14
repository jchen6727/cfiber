from neuron import h
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

h.load_file("stdrun.hoc")

#take m0 as 0 and t0 as 1

def func( t , minf, mtau, hinf, htau):
    m = minf - minf*np.exp(-t/mtau)
    h = hinf + (1 - hinf)*np.exp(-t/htau)
    return m*m*m*h
    
def func0( t , m0, minf, mtau, h0, hinf, htau):
    return minf - ( (m0 - minf) *np.exp(-t/mtau) )**3 * ( hinf + (h0 - hinf)*np.exp(-t/htau) ) 
    
def vc(chan = "hh", record = "gna", vstart = -90, vsteps = range(-50, 50, 10), vstop = 0, dur = [25,25,25], gna_normalize = True):
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
    #t = h.Vector()
    #t.record(h._ref_t)

    h.t = 0
    h.finitialize(vstart)
    h.fcurrent()
    h.run()

    #t  = [t_ for t_ in t]
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

    return simData

def fit( strt, stop, t, gna):
    #istrt = int(window[0]/h.dt)
    #istop = int(window[1]/h.dt)
    #add 1 to istrt to get the actual "start" stimulus
    #or else wierd things happen to the curve

    #just use indexing values for now so can manually adjust window size
    gna = gna[strt:stop]
    #reset window for t to represent new 0
    t   = t  [:len(gna)]
    popt, pcov = curve_fit(func, t, gna, bounds = (0, [1 , np.inf, 1 , np.inf]))
    return {'minf': popt[0], 'mtau': popt[1], 'hinf':popt[2], 'htau':popt[3], 'pcov':pcov}

def getHH(v = 0):
    h.rates_hh(v)
    return {'minf': h.minf_hh, 'mtau': h.mtau_hh, 'hinf': h.hinf_hh, 'htau': h.htau_hh}
#   actually just use:
#   h.rates_hh(v)
#   h.tau_hh, h.hinf_hh, h.mtau_hh, h.minf_hh
#
#use rates here to get mtau stuff
if __name__ == "__main__":
    print("simData = vc(chan, record, vstart, vsteps, vstop, dur)")
    print("simData.keys()")

