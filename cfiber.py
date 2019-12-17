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
    
    def __init__(self,x=0,y=0,z=0,ID=0):
        self.regions = {'axn': [], 'drg': [], 'soma': []}

        self.set_morphology()
        self.insert_conductances()
        
        self.connect_secs()

    def add_comp(self, sec, *regions):
        self.__dict__[sec] = h.Section(name=sec)
        for region in regions:
            self.regions[region].append(self.__dict__[sec])

    def set_morphology(self):

        for sec in ['axnperi', 'axncntr', 'drgperi', 'drgcntr', 'drgstem']:
            self.add_comp(sec, sec[0:3])
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
            
            sec.insert('nahh')
            sec.gnabar_nahh = 0.04
            sec.mshift_nahh = -6
            sec.hshift_nahh = 6
            
            sec.insert('borgkdr')
            sec.gkdrbar_borgkdr = 0.04
            sec.ek = -90
            
            sec.insert('pas')
            sec.g_pas = 1/10000
            sec.e_pas = -60
            sec.Ra    = 100
            
        for sec in self.regions['drg']:
            
            sec.e_pas = -54
            
            sec.insert('iM')
            sec.gkbar_iM = 0.0004
            sec.vshift_iM = -5

        for sec in self.regions['soma']:
            
            sec.gnabar_nahh = 0.02

    def connect_secs(self):
        self.drgperi.connect(self.axnperi)
        self.drgstem.connect(self.drgperi)
        self.drgsoma.connect(self.drgstem)
        self.drgcntr.connect(self.drgperi)
        self.axncntr.connect(self.drgcntr)

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