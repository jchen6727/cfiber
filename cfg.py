""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict

cfg = specs.SimConfig()  

# Parameters
#cfg.gna17 = 0.0057
#cfg.gna18 = 0.013

#cfg.gna17 = 0.01066
#cfg.gna18 = 0.02427
cfg.hParams = {'celsius': 37, 'v_init': -50}
cfg.vrest = cfg.hParams['v_init']

#cfg.gna17 = 0.01
#cfg.gna18 = 0.03
#cfg.cndct = [ 1.5 , 0.5 ]

#length of the peripheral axon
cfg.L     = 10000#100000
cfg.nseg  = 1001
#testing dlambda

cfg.gna17 = 0.8 * 0.3
cfg.gna18 = 0.9 * 0.3   
cfg.gna19 = 0.06 * 0.5
cfg.nacndct = [ 1 , 1 , 1 ]

cfg.gk2 = 0.06    # KDR channel
cfg.gk3 = 0.06    # A-type channel

cfg.gk7 = 0.01 # IM channel 0.02 is the value for XE9 blockade.

cfg.kcndct  = [ 0, 1 , 1 , 0, 1]

cfg.navq = { 'nav17': 1.0, 'nav18': 1, 'na19a': 5}
cfg.kvq = { 'kv2': 1.5 , 'kv3': 3.0 }

cfg.gca = 0

#55.805
#ena, ek for testing values... maybe? 140/10
# 66.7  , -81.31
cfg.ena =  60 #5.8#66.7
cfg.ek  =  -70#-81.31
cfg.rmut = 0.0

cfg.gm  = 0.0001
cfg.delay = [ 300 ]#, 250, 300] #, 400, 500, 600 ] #, 200, 300, 400, 500 ]#, 100, 200, 300, 400, 500]#s, 200, 300, 400, 500, 600, 700, 800, 900  ]

cfg.cvode_active = True
#cfg.dt = 0.01
#cfg.hParams = {'celsius': 37, 'v_init': -50}

cfg.recordStims = False  
cfg.recordStep = 0.0125

cfg.nav17 = 'nav17'
cfg.nav18 = 'nav18'
cfg.nav19 = 'na19a'
cfg.recordTraces = {'v1' : {'sec': 'axnperi', 'loc': 0.1, 'var': 'v'},
                    'v3' : {'sec': 'axnperi', 'loc': 0.3, 'var': 'v'},
                    'v5' : {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
                    'v7' : {'sec': 'axnperi', 'loc': 0.7, 'var': 'v'},
                    'v9' : {'sec': 'axnperi', 'loc': 0.9, 'var': 'v'},
                    'vs' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'v'},
                    'vc' : {'sec': 'axncntr', 'loc': 0.5, 'var': 'v'},
                    'in7' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_nav17'},
                    'in8' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_nav18'},
                    'in9' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_na19a'},
#                    'ik1' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_kv1'   },
                    'ik2' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_kv2'   },
                    'ik3' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_kv3'   },
#                    'ik4' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_kv4'   },
                    'ik7' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_kv7'   }}

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
#cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']


# Analysis and plotting 
#cfg.analysis.plotTraces = {'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3), 
#                           'showFig': False, 'timeRange': [cfg.delay[0], cfg.duration]}

cfg.duration = cfg.delay[-1] + 100
cfg.analysis.plotTraces = {'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3), 
                           'showFig': False, 'timeRange': [0, cfg.duration]}
