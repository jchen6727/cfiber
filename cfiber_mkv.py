'''
nociceptive c fiber 
'''

from neuron import h

class cfiber():
    secs = {'axnperi': {'nseg':100, 'L':5000, 'diam': .8  }, 
            'axncntr': {'nseg':100, 'L':5000, 'diam': .4  },
            'drgperi': {'nseg':100, 'L':100,  'diam': .8  },
            'drgcntr': {'nseg':100, 'L':100,  'diam': .4  },
            'drgstem': {'nseg':100, 'L':75,   'diam': 1.4 },
            'drgsoma': {'nseg':1,   'L':25,   'diam': 25  }}
        #if we treat the total expression of NaV channels as 1
        #we can distribute conductance as approximately
        #gnabar17 = 1/6, gnabar18 = 3/6, gnabar19 = 2/6
        #if using transcriptome profile

    def __init__(self,x=0,y=0,z=0,ID=0, gnabar17=0.04/6, gnabar18=0.12/6, gnabar19=0.08/6):
        self.regions = {'all': [], 'axn': [], 'drg': [], 'soma': []}
        self.gnabar17, self.gnabar18, self.gnabar19 = gnabar17, gnabar18, gnabar19
        self.set_morphology()
        self.insert_conductances()
        
        self.connect_secs()
        self.initialize_values()

    def add_comp(self, sec, *regions):
        self.__dict__[sec] = h.Section(name=sec)
        for region in regions:
            self.regions[region].append(self.__dict__[sec])

    def set_morphology(self):

        for sec in ['axnperi', 'axncntr', 'drgperi', 'drgcntr', 'drgstem']:
            self.add_comp(sec, sec[0:3], 'all')
            self.set_geom(sec)

        for sec in ['drgsoma']:
            self.add_comp(sec, 'drg', 'soma', 'all')
            self.set_geom(sec)

    def set_geom(self, sec):
        self.__dict__[sec].nseg = cfiber.secs[sec]['nseg']
        self.__dict__[sec].L    = cfiber.secs[sec]['L']
        self.__dict__[sec].diam = cfiber.secs[sec]['diam']

    def insert_conductances (self):
        
        for sec in self.regions['axn'] + self.regions['drg']:
            sec.Ra    = 100
            
            sec.insert('na17a')
            sec.gnabar_na17a = self.gnabar17
            sec.insert('na18a')
            sec.gnabar_na18a = self.gnabar18
            sec.insert('na19a')
            sec.gnabar_na19a = self.gnabar19

            sec.insert('borgkdr')
            sec.gkdrbar_borgkdr = 0.04
            sec.ek = -90
            
            sec.insert('pas')
            sec.g_pas = 1/10000
            ##sec.e_pas = -60
            
        for sec in self.regions['drg']:
            
            ##sec.e_pas = -54
            
            sec.insert('iM')
            sec.gkbar_iM = 0.0004
            sec.vshift_iM = -5

        for sec in self.regions['soma']:
            
            sec.gnabar_na17a = self.gnabar17/2
            sec.gnabar_na18a = self.gnabar18/2
            sec.gnabar_na19a = self.gnabar19/2

    def connect_secs(self):
        self.drgperi.connect(self.axnperi)
        self.drgstem.connect(self.drgperi)
        self.drgsoma.connect(self.drgstem)
        self.drgcntr.connect(self.drgperi)
        self.axncntr.connect(self.drgcntr)

    def initialize_values(self):
        #sets passive current to allow for steady state voltage.
        for sec in self.regions['all']:
            h.finitialize(-60)
            h.fcurrent()
            sec.e_pas = sec.v + (sec.ina + sec.ik) / sec.g_pas



'''      
'axnperi'
'axncntr'
'drgperi'
'drgcntr'
'drgstem'
'drgsoma'

peri connect tjperi(0),1
tjperi connect stem(0),1
stem connect soma(0),1
tjperi connect tjcentral(0),1
tjcentral connect central(0),1   

peri {'nseg':100, 'L':5000, 'diam': .8}			// peripherial axon
tjperi {'nseg':100, 'L':100, 'diam': .8}		   	// tjunction axon
tjcentral {'nseg':100, 'L':100, 'diam': .4}		// tjunction axon
central {'nseg':100, 'L':5000, 'diam': .4}		// central axon
stem {'nseg':100, 'L':75, 'diam': 1.4}				// stem axon
soma {'nseg':1, 'L':25, 'diam':25}	
'''