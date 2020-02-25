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

def get_traces(title = "current", y = "na", start = 0, stop = 10, idstr = 'i', plot = True, peak = False):
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


start = int( (cfg.delay[0] - 3) / cfg.recordStep )
stop  = int( (cfg.delay[-1] + 7) / cfg.recordStep )

start = int(200 / cfg.recordStep)
stop  = int(204 / cfg.recordStep)
print("RMP: %f" %(data['vs'][start]))

get_traces("current", "na", start, stop, 'i', True, False)

peaks = get_traces("voltage", "mv", start, stop, 'v', True, True)
print(peaks)
peaks = get_traces("current (Na)", "na", start, stop, 'in', True, True)
print(peaks)
