from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()


#good target -- 1.0 -> 1.3
#params['gna17'] = [ x for x in np.linspace(0.8, 2.2, 15)]

#good target -- 0.013 -> 0.014
params['nacndct'] = [ [x, x, 1] for x in [0.2, 0.3, 0.4, 0.5, 0.6 ] ]
params['gna19']   = [ 0.03 + 0.01 * x for x in range(6)  ]
params['gk2']     = [ 0.1 + 0.1 * x for x in range(10) ]
params['gk3']     = [ 0.1 + 0.1 * x for x in range(10) ]


b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'NaV'
b.saveFolder = 'batch_data'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()