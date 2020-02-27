import json

import numpy as np

import matplotlib.pyplot as plt

from cfg import cfg

with open("data/sim1.json", "r") as rf:
    ndct = json.load(rf)

data = {}

data['t'] = ndct['simData']['t']
for var in cfg.recordTraces.keys():
    data[var] = ndct['simData'][var]['cell_0']

### get all the data -- put in data{} ###

def plot_data( title = "title", xaxis = "xlabel", yaxis = "ylabel", labels = ['0'], xdatas = [ [0] ], ydatas = [ [0] ] ):
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

def get_traces(title = "current", y = "ma/cm2", start = 0, stop = 10, idstr = 'i', plot = True, peak = False):
    idlen  = len(idstr)
    labels = [key for key in data.keys() if key[:idlen]==idstr]
    xdatas = [data['t'][start:stop]] * len(labels)
    ydatas = [ data[i][start:stop] for i in labels ]
    peaks = {}
    if plot:
        plot_data( title, "time (ms)", "%s (%s)" %(title, y), labels, xdatas, ydatas )
    if peak:
        for i, label in enumerate(labels):
            peaks[label] = [min(ydatas[i]), max(ydatas[i])]

    return peaks

def get_propts():
    propts = {}
    dx = cfg.L * 0.8 # in microns
    dt = data['t'][np.argmax(data['v9'])] - data['t'][np.argmax(data['v1'])] # in ms
    propts['peri_vel'] = dx/dt * 1e-3 # correction to meters/second
    propts['soma_pkv'] = max(data['vs'])
    propts['soma_pkt'] = data['t'][np.argmax(data['vs'])]
    propts['soma_ahp'] = min(data['vs'])
    
    return propts
    


start = int( (cfg.delay[0]  - 3) / cfg.recordStep )
stop  = int( (cfg.delay[-1] + 7) / cfg.recordStep )

start = int(200 / cfg.recordStep)
stop  = int(220 / cfg.recordStep)
print("RMP: %f" %(data['vs'][start]))

get_traces("current", "ma/cm2", start, stop, 'i', True, False)

peaks = get_traces("voltage", "mv", start, stop, 'v', True, True)
print(peaks)
peaks = get_traces("current (na)", "ma/cm2", start, stop, 'in', True, True)
#convert to ma/cm2 to na knowing that surface area of soma is 7.85e-5 cm2
#this means x (na) = 1.5 ma/cm2 * 1.96e-5 cm2 * 1e6 na/ma

print(peaks)

print(get_propts())


