from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()


#good target -- 1.0 -> 1.3
#params['gna17'] = [ x for x in np.linspace(0.8, 2.2, 15)]

#good target -- 0.013 -> 0.014
#params['gna18'] = [ x for x in np.linspace(0.01, 0.02, 11)]
params['gna18'] = [ x for x in np.linspace(0.013000, 0.013005, 6)]
params['cndct'] = [ [1, 1] ]
#params['block'] = [ [0, 1], [1, 1], [1, 0] ]

b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'NaV'
b.saveFolder = 'batch_data'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()