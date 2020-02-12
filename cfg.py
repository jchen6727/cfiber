""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 1000
#cfg.dt = 0.01
cfg.hParams = {'celsius': 37, 'v_init': -60}

cfg.cvode_active = True
# cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {#'v0' : {'sec': 'axnperi', 'loc': 0.0, 'var': 'v'},
                    'v1' : {'sec': 'axnperi', 'loc': 0.1, 'var': 'v'},
                    #'v2' : {'sec': 'axnperi', 'loc': 0.2, 'var': 'v'},
                    'v3' : {'sec': 'axnperi', 'loc': 0.3, 'var': 'v'},
                    #'v4' : {'sec': 'axnperi', 'loc': 0.4, 'var': 'v'},
                    'v5' : {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
                    #'v6' : {'sec': 'axnperi', 'loc': 0.6, 'var': 'v'},
                    'v7' : {'sec': 'axnperi', 'loc': 0.7, 'var': 'v'},
                    #'v8' : {'sec': 'axnperi', 'loc': 0.8, 'var': 'v'},
                    'v9' : {'sec': 'axnperi', 'loc': 0.9, 'var': 'v'}}
                    #'v10': {'sec': 'axnperi', 'loc': 1.0, 'var': 'v'}}

#cfg.recordTraces = {'v01' : {'sec': 'axnperi', 'loc': 0.1, 'var': 'v'},
#                    'v03' : {'sec': 'axnperi', 'loc': 0.3, 'var': 'v'},
#                    'v05' : {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
#                    'v07' : {'sec': 'axnperi', 'loc': 0.7, 'var': 'v'},
#                    'v09' : {'sec': 'axnperi', 'loc': 0.9, 'var': 'v'}}

#cfg.recordTraces = {'ina17': {'sec': 'axnperi', 'loc': 0.3, 'var': 'ina_nav17'}}
#cfg.recordTraces = {'ina18': {'sec': 'axnperi', 'loc': 0.3, 'var': 'ina_na18a'}}

#cfg.recordTraces = { 'v03' : {'sec': 'axnperi', 'loc': 0.3, 'var': 'v'} }

cfg.recordStims = False  
cfg.recordStep = 0.05 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
#cfg.savePickle = True
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = Dict({'include': ['cfiber'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True, 
                             'showFig': False, 'timeRange': [0, 1000]})

# Parameters
#cfg.gna17 = 0.0057
#cfg.gna18 = 0.013

#cfg.gna17 = 0.01066
#cfg.gna18 = 0.02427

cfg.gna17 = 0.02427
cfg.gna18 = 0.01066
cfg.cndct = [ 0.85, 0.85 ]
#cfg.cndct = [ 1.75, 1.75 ]

cfg.delay = [ 100, 200, 300, 400, 500, 600, 700, 800, 900  ]

#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
# * 10 too much for gnabar17
#somewhere around 175 for original gnabar17
#cfg.navs = {'nav1p7': 0.04, 'na18a': 0, 'na19a': 0}
#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
#cfg.navs = {'na17a': 0.04/3 * 100, 'na18a': 0.04}
#cfg.navs = {'na17a': 0.04/6, 'na18a': 0.04/2, 'na19a': 0.04/3 }
