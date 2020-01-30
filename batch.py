from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()

params['gnaT'] = [x for x in np.linspace(0, 0.1, 10)]
params['gna17r'] = [x for x in np.logspace( 1, 5, 5 )]
params['gna17o'] = [0, 1]
params['gna18o'] = [0, 1]

b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'NaV'
b.saveFolder = 'batch_data'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()