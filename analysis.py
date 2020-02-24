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

def plot_currents(start = 0, stop = 10):
    labels = [key for key in data.keys() if key[0]=='i']
    xdatas = [data['t'][start:stop]] * len(labels)
    ydatas = [ data[i][start:stop] for i in labels ]
    plot_data( "currents", "time (ms)", "current (na)", labels, xdatas, ydatas )

def plot_voltages(start = 0, stop = 10):
    labels = [key for key in data.keys() if key[0]=='v']
    xdatas = [data['t'][start:stop]] * len(labels)
    ydatas = [data[v][start:stop] for v in labels ]
    plot_data( "voltages", "time (ms)", "voltage (mv)", labels, xdatas, ydatas )  

start = 290 * 20
stop  = 307 * 20
plot_currents(start, stop)
plot_voltages(start, stop)

print("RMP: %f" %(data['vs'][6000]))