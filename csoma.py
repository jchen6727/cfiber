'''
c soma only
(removed everything including stem)
'''

from neuron import h

class csoma():
    secs = {'drgsoma': {'nseg':1  , 'L':25,   'diam': 25  }}
    # 100 segments, 0.5 mm x 0.8 um

    def __init__(self,x=0,y=0,z=0,ID=0, 
                 navs = {'na17a': 0.04/6, 'na18a': 0.12/6, 'na19a': 0.08/6  }, 
                 kvs  = {'kv4'  : 0.01  , 'kv2'  : 0.002 , 'kv1'  : 0.00006 },
                 ena  = 70,
                 ek   = -70,
                 vrest= -57,
                 gm   = 1/10000,
                 rmut = 0.5):
        self.regions = {'all': [], 'axn': [], 'drg': [], 'soma': []}
        
        self.vrest = vrest

        self.navs = navs # sodium channel dictionary
        self.ena  = ena  # Nernst of sodium

        self.kvs  = kvs  # potassium channel dictionary
        self.ek   = ek   # Nernst of potassium

        self.emut = (ena + ek) / 2 # mutated reversal in between sodium and potassium channel
        self.rmut = rmut           # percent mutation RNA

        self.gm = gm

        self.set_morphology()
        self.insert_conductances()
        
        self.connect_secs()
        self.initialize_values()

    def add_comp(self, sec, *regions):
        self.__dict__[sec] = h.Section(name=sec)
        for region in regions:
            self.regions[region].append(self.__dict__[sec])

    def set_morphology(self):
        for sec in ['drgsoma']:
            self.add_comp(sec, 'drg', 'soma', 'all')
            self.set_geom(sec)

    def set_geom(self, sec):
        self.__dict__[sec].nseg = csoma.secs[sec]['nseg']
        self.__dict__[sec].L    = csoma.secs[sec]['L']
        self.__dict__[sec].diam = csoma.secs[sec]['diam']

    def insert_conductances (self):
        
        for sec in self.regions['all']:
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
            sec.g_pas = self.gm
            sec.e_pas = self.vrest
            ##sec.e_pas = -60

    def connect_secs(self):
        #nothing to connect
        return


    def initialize_values(self):

        for i, sec in enumerate(self.regions['all']):
            h.finitialize(self.vrest)
            h.fcurrent()
            for nav in self.navs:
                exestr = "print( \"ina_" + nav + ": %f\" %(sec.ina_" + nav + "))"   
                exec(exestr)

            for kv in self.kvs:
                exestr = "print( \"ik_"  + kv + " : %f\" %(sec.ik_"  + kv + "))"
                exec(exestr)
            
            sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas

        ##sets passive current to allow for steady state voltage.
        #for i, sec in enumerate(self.regions['all']):
        #    h.finitialize(self.vrest)
        #    h.fcurrent()
        #    ##sec.g_pas = sec.v + (sec.ina + sec.ik) / sec.e_pas
        #    sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas
        #    ##print( "e_pas: %f" %(sec.e_pas) )
        #    print( "e_pas: %f" %(sec.e_pas) )