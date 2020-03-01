from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()

ivs = [int(x) for x in np.linspace(20, 200, 10)]

delays = [ [300, 300 + iv] for iv in ivs]

params['nacndct'] = [ [ 1 , 1 - x , 1 ] for x in np.linspace(0.0 , 0.9 , 10) ]
params['delay']   = delays

b = Batch(params = params, cfgFile = 'batch_cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'cndct'
b.saveFolder = 'batch_cndct'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()