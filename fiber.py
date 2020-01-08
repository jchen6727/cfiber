from neuron import h

class fiber():
    secs = {'prox': {'nseg':100, 'L':5000, 'diam': .8  }, 
            'dist': {'nseg':100, 'L':5000, 'diam': .8  } }

# proportion of 1.7 is approximately 1/3 to 1.8 in nociceptive c fibers
    def __init__(self,x=0,y=0,z=0,ID=0, gnabar17=0.04/6, gnabar18=0.12/6):
        #gnabar17 = 1/6, gnabar18 = 3/6, gnabar19 = 2/6
        self.gnabar17, self.gnabar18 = gnabar17, gnabar18
        self.set_morphology()
        self.insert_conductances()
        self.connect_secs()

    def add_comp(self, sec):
        self.__dict__[sec] = h.Section(name=sec)

    def set_morphology(self):

        for sec in ['axnperi', 'axncntr', 'drgperi', 'drgcntr', 'drgstem']:
            self.add_comp(sec)
            self.set_geom(sec)

        for sec in ['drgsoma']:
            self.add_comp(sec, 'drg', 'soma')
            self.set_geom(sec)

    def set_geom(self, sec):
        self.__dict__[sec].nseg = cfiber.secs[sec]['nseg']
        self.__dict__[sec].L    = cfiber.secs[sec]['L']
        self.__dict__[sec].diam = cfiber.secs[sec]['diam']

    def insert_conductances (self):
        
        for sec in self.regions['axn'] + self.regions['drg']:
            sec.Ra    = 100

            sec.insert('nav1p7')
            sec.gnabar_nav1p7 = self.gnabar17
            sec.insert('nav1p8')
            sec.gnabar_nav1p8 = self.gnabar18
            sec.insert('nav1p9')
            sec.gnabar_nav1p9 = self.gnabar19
            
            #sec.insert('na17a')
            #sec.gbar_na17a = self.gnabar17
            #sec.insert('na18a')
            #sec.gbar_na18a = self.gnabar18
            #sec.insert('na19a')
            #sec.gbar_na19a = self.gnabar19

            sec.insert('borgkdr')
            sec.gkdrbar_borgkdr = 0.04
            sec.ek = -90
            
            sec.insert('pas')
            sec.g_pas = 1/10000
            sec.e_pas = -60
            
        for sec in self.regions['drg']:
            
            sec.e_pas = -54
            
            sec.insert('iM')
            sec.gkbar_iM = 0.0004
            sec.vshift_iM = -5

        for sec in self.regions['soma']:
            
            sec.gnabar_nav1p7 = self.gnabar17/2
            sec.gnabar_nav1p8 = self.gnabar18/2
            sec.gnabar_nav1p9 = self.gnabar19/2

            #sec.gbar_na17a = self.gnabar17/2
            #sec.gbar_na18a = self.gnabar18/2
            #sec.gbar_na19a = self.gnabar19/2

    def connect_secs(self):
        self.drgperi.connect(self.axnperi)
        self.drgstem.connect(self.drgperi)
        self.drgsoma.connect(self.drgstem)
        self.drgcntr.connect(self.drgperi)
        self.axncntr.connect(self.drgcntr)
