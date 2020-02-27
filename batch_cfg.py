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
cfg.L     = 1000
cfg.nseg  = 101
#testing dlambda
"""
#MM channel values
cfg.gna17 = 0.8 * 0.3
#cfg.gna18 = 0.6            #<---#          0.6 for MM model
cfg.gna18 = 0.9 * 0.3             #<---#          0.9 for HH model   
cfg.gna19 = 0.06
#cfg.nacndct = [ 0.4 , 0.4 , 1 ]
cfg.nacndct = [ 1 , 1 , 0.5 ]
#cfg.nacndct = [ 0.4 , 0.4 , 0.5]
#cfg.nacndct = [ 0.2 , 0.2 , 0.5 ]
###TEST VALUES###
cfg.gk1 = 0.000
cfg.gk2 = 0.06    # KDR channel
cfg.gk3 = 0.05    # A-type channel
cfg.gk4 = 0.000
cfg.gk7 = 0.0200 # IM channel 0.02 is the value for XE9 blockade.

cfg.gk2 = 0.002
cfg.gk3 = 0.06

cfg.gk2 = 0.06

#cfg.kcndct  = [ 0, 0.1, 2, 0, 1]
#cfg.kcndct  = [ 0, 0.05 , 0.8 , 0, 1]
cfg.kcndct  = [ 0, 1 , 1 , 0, 0.5]
cfg.gca = 0.0

cfg.naq = 1.0
#cfg.kq  = 4.0
cfg.kvq = { 'kv2': 1.5 , 'kv3': 3.0 }
"""

"""
###WORKING VALUES###
cfg.gk1 = 0.30225
cfg.gk2 = 2.34
cfg.gk3 = 0.192
cfg.gk4 = 0.06139
cfg.gk7 = 0.008

cfg.kcndct  = [ 1, 1, 1 , 1, 1 ]
"""


cfg.gna17 = 0.8 * 0.3
cfg.gna18 = 0.9 * 0.3   
cfg.gna19 = 0.06 * 0.5
cfg.nacndct = [ 1 , 1 , 1 ]

cfg.gk2 = 0.06    # KDR channel
cfg.gk3 = 0.06    # A-type channel

cfg.gk7 = 0.01 # IM channel 0.02 is the value for XE9 blockade.

cfg.kcndct  = [ 0, 1 , 1 , 0, 1]

cfg.navq = { 'nav17': 1.0, 'nav18': 1.}
cfg.kvq = { 'kv2': 1.5 , 'kv3': 3.0 }

cfg.gca = 0

#55.805
#ena, ek for testing values... maybe? 140/10
# 66.7  , -81.31
cfg.ena =  60 #5.8#66.7
cfg.ek  =  -70#-81.31
cfg.rmut = 0.0

cfg.gm  = 0.0001
cfg.delay = [ 200 ]#, 250, 300] #, 400, 500, 600 ] #, 200, 300, 400, 500 ]#, 100, 200, 300, 400, 500]#s, 200, 300, 400, 500, 600, 700, 800, 900  ]

#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
# * 10 too much for gnabar17
#somewhere around 175 for original gnabar17
#cfg.navs = {'nav1p7': 0.04, 'na18a': 0, 'na19a': 0}
#cfg.navs = {'na17a': cfg.gnaT * cfg.na17r * cfg.na17o, 'na18a': cfg.gnaT * cfg.na18o}
#cfg.navs = {'na17a': 0.04/3 * 100, 'na18a': 0.04}
#cfg.navs = {'na17a': 0.04/6, 'na18a': 0.04/2, 'na19a': 0.04/3 }

# Run parameters
#cfg.duration = cfg.delay[-1] + 20

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

cfg.duration  = 700
cfg.analysis.plotTraces = {'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3), 
                           'showFig': False, 'timeRange': [0, cfg.duration]}
