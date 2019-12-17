""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict
cfg = specs.SimConfig()  

# Run parameters
cfg.duration = 100
cfg.dt = 0.05
cfg.hParams = {'celsius': 6.3}

cfg.cvode_active = False
# cfg.printRunTime = 0.1
# cfg.printPopAvgRates = True

# Recording 
cfg.recordTraces = {'V_peri_0.0': {'sec': 'axnperi', 'loc': 0.0, 'var': 'v'},
                    'V_peri_0.5': {'sec': 'axnperi', 'loc': 0.5, 'var': 'v'},
                    'V_peri_1.0': {'sec': 'axnperi', 'loc': 1.0, 'var': 'v'},
                    'V_cntr_0.0': {'sec': 'axncntr', 'loc': 0.0, 'var': 'v'},
                    'V_cntr_0.5': {'sec': 'axncntr', 'loc': 0.5, 'var': 'v'},
                    'V_cntr_1.0': {'sec': 'axncntr', 'loc': 1.0, 'var': 'v'}}
cfg.recordStims = False  
cfg.recordStep = 0.05 

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Analysis and plotting 
cfg.analysis.plotTraces = Dict({'include': ['cfiber'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True, 
                             'showFig': False, 'timeRange': [0,cfg.duration]})

# Parameters

