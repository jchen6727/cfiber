'''
c fiber peripheral nerve fiber
contains only the peripheral nerve fiber for simulation of NaV channel effects on peripheral axon
'''

from neuron import h

class cfiber():
    secs = {'axnperi': {'nseg':100, 'L':5000, 'diam': 1  }}
    # 100 segments, 1 mm x 1 um, 100000 micron length (100 mm) 1 micron diameter

    def __init__(self,x=0,y=0,z=0,ID=0, 
                 navs = {'na17a': 0.04/6, 'na18a': 0.12/6, 'na19a': 0.08/6  }, 
                 kvs  = {'kv4'  : 0.01  , 'kv2'  : 0.002 , 'kv1'  : 0.00006 },
                 ena  = 70,
                 ek   = -70,
                 rmut = 0.5):
        self.regions = {'all': [], 'axn': []}
        
        self.navs = navs # sodium channel dictionary
        self.ena  = ena  # Nernst of sodium

        self.kvs  = kvs  # potassium channel dictionary
        self.ek   = ek   # Nernst of potassium

        self.emut = (ena + ek) / 2 # mutated reversal in between sodium and potassium channel
        self.rmut = rmut           # percent mutation RNA

        self.set_morphology()
        self.insert_conductances()
        
#        self.connect_secs()
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

            sec.ena = self.ena

            for kv in self.kvs:
                sec.insert(kv)
                exestr = "sec.gkbar_%s = self.kvs[kv]" %(kv)
                exec(exestr)

            sec.ek  = self.ek

            sec.insert('pas')
            sec.g_pas = 1/10000
            ##sec.e_pas = -60

    def initialize_values(self):
        #sets passive current to allow for steady state voltage.
        for i, sec in enumerate(self.regions['all']):
            h.finitialize(-60)
            h.fcurrent()
            sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas
            print( "e_pas: %f" %(sec.e_pas) )