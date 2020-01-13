from neuron import h
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")


def vc(chan = "hh", record = "m", vstart = 0, vsteps = range(-50, 50, 10), vstop = 0, dur = [25,25,25]):
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

    t = h.Vector()
    t.record(h._ref_t)

    h.t = 0
    h.finitialize(vstart)
    h.fcurrent()
    h.run()

    #slice off initialization
    t  = [t_ for t_ in t if t_ > dur[0] * 0.7]
    for i, rv in enumerate(rvs):
        rv = [rv_ for rv_ in rv][-len(t):]
        rvs[i] = rv

    fig, ax = plt.subplots()
    ax.set_xlabel("time (ms)")

    ax.set_ylabel(record)

    ax.set_title( varstr + "_vclamp")
    
    simData['t'] = t
    for i, vstep in enumerate(vsteps):
        simData[vstep] = rvs[i]
        ax.plot(t, rvs[i], label = str(vstep))

    ax.legend(fontsize=8)
    plt.savefig(varstr + "_vclamp.png")

    return simData

if __name__ == "__main__":
    print("simData = vc(chan, record, vstart, vsteps, vstop, dur)")
    print("simData.keys()")

