""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 307
#cfg.dt = 0.01
cfg.hParams = {'celsius': 37, 'v_init': -50}

cfg.cvode_active = True
# cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording

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

#cfg.recordTraces = {'vs' : {'sec': 'drgsoma', 'loc': 0.5, 'var': 'v'}}

#cfg.recordTraces = {'ina17': {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_nav17'},
#                    'ina18': {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_na18a'}}

#cfg.recordTraces = { 'v03' : {'sec': 'axnperi', 'loc': 0.3, 'var': 'v'} }

cfg.recordStims = False  
cfg.recordStep = 0.05 
#cfg.recordStep = 1
# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = Dict({'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True, 
                             'showFig': False, 'timeRange': [300, cfg.duration]})

# Parameters
#cfg.gna17 = 0.0057
#cfg.gna18 = 0.013

#cfg.gna17 = 0.01066
#cfg.gna18 = 0.02427

cfg.vrest = cfg.hParams['v_init']

#cfg.gna17 = 0.01
#cfg.gna18 = 0.03
#cfg.cndct = [ 1.5 , 0.5 ]

#length of the peripheral axon
cfg.L     = 100
cfg.nseg  = 101


#cfg.gna17 = 0.8
#cfg.gna18 = 0.6
cfg.gna17 = 0.8
cfg.gna18 = 0.6
cfg.gna19 = 0.06
cfg.nacndct = [ 0.4 , 0.4 , 1 ]

#cfg.nacndct = [ 0.5 , 0.5 , 1 ]


###TEST VALUES###
cfg.gk1 = 0.000
cfg.gk2 = 0.6    # KDR channel
cfg.gk3 = 0.5    # A-type channel
cfg.gk4 = 0.000
cfg.gk7 = 0.0200 # IM channel

cfg.kcndct  = [ 0, 0.1, 2, 0, 1]
cfg.gca = 0.0
"""
###WORKING VALUES###
cfg.gk1 = 0.30225
cfg.gk2 = 2.34
cfg.gk3 = 0.192
cfg.gk4 = 0.06139
cfg.gk7 = 0.008

cfg.kcndct  = [ 1, 1, 1 , 1, 1 ]
"""
#55.805
#ena, ek for testing values...
# 66.7  , -81.31
cfg.ena =  66.7
cfg.ek  =  -81.31
cfg.rmut = 0.0

cfg.gm  = 0.0002
cfg.delay = [ 300] #, 200, 300, 400, 500 ]#, 100, 200, 300, 400, 500]#s, 200, 300, 400, 500, 600, 700, 800, 900  ]

#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
# * 10 too much for gnabar17
#somewhere around 175 for original gnabar17
#cfg.navs = {'nav1p7': 0.04, 'na18a': 0, 'na19a': 0}
#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
#cfg.navs = {'na17a': 0.04/3 * 100, 'na18a': 0.04}
#cfg.navs = {'na17a': 0.04/6, 'na18a': 0.04/2, 'na19a': 0.04/3 }


