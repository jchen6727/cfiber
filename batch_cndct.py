from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()

"""
# log parameter testing
gkparams = []

for x in np.logspace( -4, 0, 5 ): gkparams.extend(np.multiply([1/3, 2/3, 1], x))

params['nacndct'] = [ [ x , x , 1 ] for x in np.linspace(0.1 , 0.4 , 4 ) ]

params['gk2']     = gkparams

params['gk3']     = gkparams
"""

ivs = [int(x) for x in np.linspace(20, 350, 10)]

delays = [ [300, 300 + iv] for iv in ivs]

params['nacndct'] = [ [ 1 , 1 - x , 1 ] for x in np.linspace(0.0 , 0.9 , 10) ]
params['delay']   = delays

b = Batch(params = params, cfgFile = 'batch_cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'cndct'
b.saveFolder = 'batch_cndct'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()