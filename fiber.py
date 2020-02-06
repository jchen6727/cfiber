'''
c fiber nerve
contains only the peripheral nerve fiber for simulation of NaV channel effects on peripheral axon
'''

from neuron import h

class cfiber():
    secs = {'axnperi': {'nseg':100, 'L':5000, 'diam': .8  }}
        #if we treat the total expression of NaV channels as 1
        #we can distribute conductance as approximately
        #gnabar17 = 1/6, gnabar18 = 3/6, gnabar19 = 2/6
        #if using transcriptome profile

    def __init__(self,x=0,y=0,z=0,ID=0, navs = {'na17a': 0.04/6, 'na18a': 0.12/6, 'na19a': 0.08/6} ):
        self.regions = {'all': [], 'axn': []}
        
        self.navs = navs

        self.temp = temp

        self.set_morphology()
        self.insert_conductances()
        
        self.connect_secs()
        self.initialize_values()

    def add_comp(self, sec, *regions):
        self.__dict__[sec] = h.Section(name=sec)
        for region in regions:
            self.regions[region].append(self.__dict__[sec])

    def set_morphology(self):

        for sec in ['axnperi']:
            self.add_comp(sec, sec[0:3], 'all')
            self.set_geom(sec)

    def set_geom(self, sec):
        self.__dict__[sec].nseg = cfiber.secs[sec]['nseg']
        self.__dict__[sec].L    = cfiber.secs[sec]['L']
        self.__dict__[sec].diam = cfiber.secs[sec]['diam']

    def insert_conductances (self):
        
        for sec in self.regions['axn']:
            sec.Ra    = 100
            
            for nav in self.navs:
                sec.insert(nav)
                exestr = "sec.gnabar_%s = self.navs[nav]" %(nav)
                exec(exestr)

                sec.ena = 80

            sec.insert('borgkdr')
            sec.gkdrbar_borgkdr = 0.04
            sec.ek = -90
            
            sec.insert('pas')
            sec.g_pas = 1/10000
            ##sec.e_pas = -60

    def initialize_values(self):
        #sets passive current to allow for steady state voltage.
        e_pas = [-65, -65, -62, -62, -62, -62]
        for i, sec in enumerate(self.regions['all']):
            h.finitialize(-60)
            h.fcurrent()
            sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas