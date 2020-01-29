""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 300
cfg.dt = 0.05
cfg.hParams = {'celsius': 6.7, 'v_init': -65}

cfg.cvode_active = False
# cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'v': {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
                    'gna_17': {'sec': 'axnperi', 'loc': 0.5, 'var': 'na17a'}}
#                    'gna_18': {'sec': 'axnperi', 'loc': 0.5, 'var': 'gna_na18a'},
#                    'gna_19': {'sec': 'axnperi', 'loc': 0.5, 'var': 'gna_na19a'}}

#cfg.recordTraces = {'V_peri_0.0': {'sec': 'axnperi', 'loc': 0.0, 'var': 'v'},
#                    'V_peri_0.5': {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
#                    'V_peri_1.0': {'sec': 'axnperi', 'loc': 1.0, 'var': 'v'},
#                    'V_cntr_0.0': {'sec': 'axncntr', 'loc': 0.0, 'var': 'v'},
#                    'V_cntr_0.5': {'sec': 'axncntr', 'loc': 0.5, 'var': 'v'},
#                    'V_cntr_1.0': {'sec': 'axncntr', 'loc': 1.0, 'var': 'v'}}
cfg.recordStims = False  
cfg.recordStep = 0.05 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = Dict({'include': ['cfiber'], 'overlay': False, 'oneFigPer': 'cell', 'saveFig': True, 
                             'showFig': False, 'timeRange': [0,cfg.duration]})

# Parameters
cfg.gnaT = 0.4
cfg.na17r = 75
cfg.na17o = 1
cfg.na18o = 1
# * 10 too much for gnabar17
#somewhere around 175 for original gnabar17
#cfg.navs = {'nav1p7': 0.04, 'na18a': 0, 'na19a': 0}
cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * na17o, 'na18a': cfg.gnaT * }
#cfg.navs = {'na17a': 0.04/3 * 100, 'na18a': 0.04}
#cfg.navs = {'na17a': 0.04/6, 'na18a': 0.04/2, 'na19a': 0.04/3 }
