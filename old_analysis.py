"""
old analysis file to work with my old batch files
"""


import json
import numpy as np
import matplotlib.pyplot as plt
from batch_cfg import cfg

#usage:
#from analysis import analysis
#an = analysis(<<input file>>, <<output string>>)
#an.set_window(<<start time (ms)>>, <<stop time (ms)>>)
#an.plot_traces(<<title>>, <<y unit>>, <<variable string>>)

class analysis():
    def __init__(self, filename, output = "analysis/"):
        try:
            with open(filename, 'r') as fp:
                jdata = json.load(fp)
                self.fexist = True
        except:
            print("file not found")
            self.fexist = False

        self.output = output
        data = {}

        data['t'] = jdata['simData']['t']
    
        for var in ['ik2', 'ik3', 'ik7', 'in7', 'in8', 'in9', 'v1', 'v3', 'v5', 'v7', 'v9', 'vc', 'vs']:
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
        vs   = self.get_spike('v1')
        vf   = self.get_spike('v9')
        # convert to meters
        dx   = 10000 * 0.8 * 1e-6
        # convert to seconds
        dt   = ( vf['time'] - vs['time'] ) / 1000
        vel  = dx / dt
        return vel

    def plot_soma( self, start = 0, stop = cfg.duration ):
        self.set_window(start, stop)
        vs   = self.get_spike('vs')
        sstart = vs['time'] - 3
        sstop  = vs['time'] + 17
        self.set_window(sstart, sstop)

        fig, axs = plt.subplots(2, 1, figsize=(12,9), sharex=True)

        ax0 = axs[0]
        ax1 = axs[1]
        fig.suptitle( "soma" )
        #plot for soma specifically with subplots for voltage and current

        self.get_traces("i")
        ax0.set_ylabel("current (ma/cm2)")
        for i, label in enumerate(self.labels):
            ax0.plot(self.xdata, self.ydatas[i], label = label)

        self.get_traces("vs")
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("voltage (mv)")
#        ax1.set_title("soma")
        for i, label in enumerate(self.labels):
            ax1.plot(self.xdata, self.ydatas[i], label = label)
        
        plt.subplots_adjust(hspace=0)
        for ax in axs:
            ax.legend()
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-')
            ax.grid(which='minor', linestyle=':')

        plt.margins(x = 0, y = 0.0125)
        plt.savefig( self.output + "soma.png", bbox_inches = 'tight', pad_inches = 0.075)

        plt.cla()
        plt.clf()
        plt.close()

        self.plot_traces(title = "soma(v)", yu = "mv", idstr = "vs")
        self.plot_traces(title = "soma(i)", yu = "ma/cm2" , idstr = 'i')

    def get_propts( self ):
        propts = {}
        propts['soma_pkv'] = max(self.data['vs'])
        propts['soma_pkt'] = self.data['t'][np.argmax(self.data['vs'])]
        propts['soma_ahp'] = min(self.data['vs'])
        return propts

    def plot_data( self, title = "title", xaxis = "xlabel", yaxis = "ylabel", labels = ['0'], xdatas = [ [0] ], ydatas = [ [0] ] ):
        fig, ax = plt.subplots(figsize=(12,9))
        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.set_title(title)

        for i, label in enumerate(labels):
            ax.plot(xdatas[i], ydatas[i], label = label)

        ax.legend()
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-')
        ax.grid(which='minor', linestyle=':')

        plt.margins(x = 0, y = 0.0125)
        plt.savefig( self.output + title + ".png", bbox_inches = 'tight', pad_inches = 0.075)

        plt.cla()
        plt.clf()
        plt.close()

    def plot_traces( self, title = "current", yu = "ma/cm2", idstr = "i" ):
        self.get_traces(idstr)
        self.plot_data( title, "time (ms)", "%s (%s)" %(title, yu), self.labels, [self.xdata] * len(self.labels), self.ydatas )

    def get_traces( self, idstr = 'i'):
        idlen  = len(idstr)
        labels = [key for key in self.data.keys() if key[:idlen]==idstr]
        xdata  = self.data['t'][self.start:self.stop]
        ydatas = [self.data[i][self.start:self.stop] for i in labels ]
        bounds = {}
        for i, label in enumerate(labels):
            bounds[label] = [min(ydatas[i]), max(ydatas[i])]
        
        self.labels = labels
        self.xdata  = xdata
        self.ydatas = ydatas
        
        return bounds


if __name__ == "__main__":
    from cfg import cfg
    an = analysis("data/sim1.json", "adata/")
    print("velocity is %f m/s" %(an.get_vel()) )
    an.set_window(cfg.delay[1]-5, cfg.delay[-1]+25)
    an.plot_traces( "voltage", "mv", "v")
    an.plot_soma(cfg.delay[1]-5, cfg.delay[-1]+25)

    start = int( (cfg.delay[1]  - 3) / cfg.recordStep )

    print("RMP: %f" %(an.data['vs'][start]))

    print(an.get_propts())