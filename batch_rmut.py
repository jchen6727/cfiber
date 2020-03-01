from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()

ivs = [int(x) for x in np.linspace(20, 200, 10)]

delays = [ [300, 300 + iv] for iv in ivs]

# give 0.0 to the other batch file--no need to run default settings again
params['rmut']  = [ x for x in np.linspace(0.1 , 0.9 , 9) ]
params['delay'] = delays

b = Batch(params = params, cfgFile = 'batch_cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'rmut'
b.saveFolder = 'batch_rmut'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()