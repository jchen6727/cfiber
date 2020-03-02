import json

import numpy as np

import matplotlib.pyplot as plt

from cfg import cfg

class analysis():
    def __init__(self, filename, output = "analysis/"):
        with open(filename, 'r') as fp:
            jdata = json.load(fp)

        self.output = output
        data = {}

        data['t'] = jdata['simData']['t']
    
        for var in cfg.recordTraces.keys():
            data[var] = jdata['simData'][var]['cell_0']

    ### get all the data -- put in data{} ###
        self.data = data
        self.dt   = cfg.recordStep

        self.labels = [ '0' ]
        self.xdatas = [ [0] ]
        self.ydatas = [ [0] ]

        self.spikes = {}

        self.set_window( 0 , cfg.duration )

    def set_window(self, start, stop):
        self.start = self.get_index(start)
        self.stop  = self.get_index(stop)

    def get_index(self, time):
        return int(time / self.dt)

    def get_spike( self, trace = 'vs' ):
        ydata = self.data[trace][self.start:self.stop]
        self.spikes[trace] = {  'peak': max(ydata),
                                'time': self.data['t'][self.start + np.argmax(ydata)]  }
        return self.spikes[trace]

    def get_vel( self, start = 0, stop = cfg.duration ):
        self.set_window(start, stop)
        v1   = self.get_spike('v1')
        v9   = self.get_spike('v9')
        dx   = cfg.L * 0.8
        dt   = v9['time'] - v1['time']
        vel  = dx * 1E-6 / dt * 1E3
        return vel

    def plot_soma( self, start = 0, stop = cfg.duration ):
        self.set_window(start, stop)
        vs   = self.get_spike('vs')
        sstart = vs['time'] - 5
        sstop  = vs['time'] + 25
        self.set_window(sstart, sstop)
        self.plot_traces(title = "soma(v)", yu = "mv", idstr = "vs")
        self.plot_traces(title = "soma(i)", yu = "ma/cm2" , idstr = 'i')

    def get_propts( self ):
        propts = {}
        dx = cfg.L * 0.8 # in microns
        dt = self.data['t'][np.argmax(self.data['v9'])] - self.data['t'][np.argmax(self.data['v1'])] # in ms
        propts['peri_vel'] = dx/dt * 1e-3 # correction to meters/second
        propts['soma_pkv'] = max(self.data['vs'])
        propts['soma_pkt'] = self.data['t'][np.argmax(self.data['vs'])]
        propts['soma_ahp'] = min(self.data['vs'])
        return propts

    def plot_data( self, title = "title", xaxis = "xlabel", yaxis = "ylabel", labels = ['0'], xdatas = [ [0] ], ydatas = [ [0] ] ):
        fig, ax = plt.subplots()
        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.set_title(title)

        for i, label in enumerate(labels):
            ax.plot(xdatas[i], ydatas[i], label = label)

        ax.legend()
        plt.savefig( self.output + title + ".png")

        plt.cla()
        plt.clf()
        plt.close()

    def plot_traces( self, title = "current", yu = "ma/cm2", idstr = "i" ):
        self.get_traces(idstr)

        self.plot_data( title, "time (ms)", "%s (%s)" %(title, yu), self.labels, self.xdata * len(self.labels), self.ydatas )

    def get_traces( self, idstr = 'i'):
        idlen  = len(idstr)
        labels = [key for key in self.data.keys() if key[:idlen]==idstr]
        xdata  = [self.data['t'][self.start:self.stop]]
        ydatas = [self.data[i][self.start:self.stop] for i in labels ]
        bounds = {}
        for i, label in enumerate(labels):
            bounds[label] = [min(ydatas[i]), max(ydatas[i])]
        
        self.labels = labels
        self.xdata  = xdata
        self.ydatas = ydatas
        
        return bounds


if __name__ == "__main__":
    anl = analysis("data/sim1.json", "data/")
    print("velocity is %f m/s" %(anl.get_vel()) )
    anl.set_window(275, 375)
    anl.plot_traces( "voltage", "mv", "v")
    anl.plot_soma(275, 375)
    




    start = int( (cfg.delay[0]  - 3) / cfg.recordStep )

    print("RMP: %f" %(anl.data['vs'][start]))

    print(anl.get_propts())