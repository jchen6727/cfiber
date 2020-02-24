'''
c neuron containing entire morphology--
including peripheral fiber, drg with soma, central fiber
'''

from neuron import h

class cnrn():
    secs = {'axnperi': {'nseg':301, 'L':10000,'diam': 0.8 },
            'drgperi': {'nseg':101 , 'L':100,  'diam': 0.8 },
            'drgstem': {'nseg':101 , 'L':75,   'diam': 1.4 },
            'drgsoma': {'nseg':1  , 'L':25,   'diam': 25  },
            'drgcntr': {'nseg':31 , 'L':100,  'diam': 0.4 },
            'axncntr': {'nseg':1  , 'L':10,   'diam': 0.4 }}
    # 100 segments, 0.5 mm x 0.8 um

    def __init__(self,x=0,y=0,z=0,ID=0, 
                 navs = { 'na17a': 1},   #{'na17a': 0.04/6, 'na18a': 0.12/6, 'na19a': 0.08/6  }, 
                 kvs  = { 'kv4'  : 1},   #{'kv4'  : 0.01  , 'kv2'  : 0.002 , 'kv1'  : 0.00006 },
                 cavs = { 'cal'  : 1},
                 ena  = 70,
                 ek   = -70,
                 vrest= -57,
                 gm   = 1/10000,
                 rmut = 0.0,
                 L    = 100,
                 nseg = 101):
        self.regions = {'all': [], 'axn': [], 'drg': [], 'soma': []}
        
        self.vrest = vrest

        self.navs = navs # sodium channel dictionary
        self.ena  = ena  # Nernst of sodium

        self.kvs  = kvs  # potassium channel dictionary
        self.ek   = ek   # Nernst of potassium

        self.cavs = cavs

        self.emut = (ena + ek) / 2 # mutated reversal in between sodium and potassium channel
        self.rmut = rmut           # percent mutation RNA

        self.gm = gm

        self.L = L
        self.nseg = nseg

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
            self.__dict__[sec].nseg = self.nseg
            self.__dict__[sec].L    = self.L

            self.__dict__[sec].diam = cnrn.secs[sec]['diam']

        for sec in ['axncntr', 'drgperi', 'drgcntr', 'drgstem']:
            self.add_comp(sec, sec[0:3], 'all')
            self.set_geom(sec)

        for sec in ['drgsoma']:
            self.add_comp(sec, 'drg', 'soma', 'all')
            self.set_geom(sec)

    def set_geom(self, sec):
        self.__dict__[sec].nseg = cnrn.secs[sec]['nseg']
        self.__dict__[sec].L    = cnrn.secs[sec]['L']
        self.__dict__[sec].diam = cnrn.secs[sec]['diam']

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

            for cav in self.cavs:
                sec.insert(cav)
                exestr = "sec.gcabar_%s = self.cavs[cav]" %(cav)

            sec.insert('pas')
            sec.g_pas = self.gm
            sec.e_pas = self.vrest


        ##half channel density at soma -- if necessary
        #for sec in self.regions['soma']:
        #    exestr = "sec.gnabar_%s = self.navs[nav]/2" %(nav)


    def connect_secs(self):
        self.drgperi.connect(self.axnperi)
        self.drgstem.connect(self.drgperi)
        self.drgsoma.connect(self.drgstem)
        self.drgcntr.connect(self.drgperi)
        self.axncntr.connect(self.drgcntr)

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

            for cav in self.cavs:
                exestr = "print( \"ica_"  + cav + " : %f\" %(sec.ica_"  + cav + "))"
                exec(exestr)


        
            #sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas
            #print("e_pas: %f" %sec.e_pas)   
        ##sets passive current to allow for steady state voltage.
        #for i, sec in enumerate(self.regions['all']):
        #    h.finitialize(self.vrest)
        #    h.fcurrent()
        #    ##sec.g_pas = sec.v + (sec.ina + sec.ik) / sec.e_pas
        #    sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas
        #    ##print( "e_pas: %f" %(sec.e_pas) )
        #    print( "e_pas: %f" %(sec.e_pas) )
