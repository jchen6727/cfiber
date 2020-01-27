""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 100
cfg.dt = 0.05
cfg.hParams = {'celsius': 37, 'v_init': -60}

cfg.cvode_active = False
# cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'v': {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
                    'gna_17': {'sec': 'axnperi', 'loc': 0.5, 'var': 'gna_na17a'}}
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
cfg.gnaT = 0.5
# * 10 too much for gnabar17
#cfg.gnabar17, cfg.gnabar18, cfg.gnabar19 = cfg.gnaT/6, cfg.gnaT/2, cfg.gnaT/3
cfg.gnabar17, cfg.gnabar18, cfg.gnabar19 = cfg.gnaT * 250, cfg.gnaT * 0, cfg.gnaT * 0