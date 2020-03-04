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
cfg.L     = 10000
cfg.nseg  = 1001

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
cfg.delay = [ 300 ]#, 250, 300] #, 400, 500, 600 ] #, 200, 300, 400, 500 ]#, 100, 200, 300, 400, 500]#s, 200, 300, 400, 500, 600, 700, 800, 900  ]


cfg.cvode_active = True


cfg.recordStims = False  
cfg.recordStep = 0.0125

cfg.nav17 = 'nav17'
cfg.nav18 = 'nav18'
cfg.nav19 = 'na19a'
#generate recordTraces for the peripheral axon, note that will be in centimeters
for x in [ 0.1, 0.3, 0.5, 0.7, 0.9]:
    cfg.recordTraces['v(%.2fcm)' %(x * cfg.L / 10000)] = {'sec': 'axnperi', 'loc': x, 'var': 'v'}

#generate recordTraces for the soma
for i, chan in [ ['ina7','nav17'], ['ina8','nav18'], ['ina9','na19a'] ]:
    cfg.recordTraces[i] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}

for i, chan in [ ['ikdr','kv2'], ['ika','kv3'], ['ikm','kv7'] ]:
    cfg.recordTraces[i] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_%s' %(chan)}

cfg.recordTraces['vs'] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'v'}
cfg.recordTraces['vc'] = {'sec': 'axncntr', 'loc': 0.5, 'var': 'v'}

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData']


# Analysis and plotting 
#cfg.analysis.plotTraces = {'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3), 
#                           'showFig': False, 'timeRange': [cfg.delay[0], cfg.duration]}

cfg.duration  = 600
cfg.analysis.plotTraces = {'include': ['cnrn'], 'overlay': True, 'oneFigPer': 'cell', 'saveData': True, 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3), 
                           'showFig': False, 'timeRange': [200, cfg.duration]}

#use the saveData to plot values