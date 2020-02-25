from netpyne import specs
from netpyne.batch import Batch
import numpy as np
params = specs.ODict()


#good target -- 1.0 -> 1.3
#params['gna17'] = [ x for x in np.linspace(0.8, 2.2, 15)]

#good target -- 0.013 -> 0.014
params['nacndct'] = [ [ x , x , 1] for x in np.linspace(0.1 , 1.0 , 10 ) ]
params['gna19']   = [ x for x in np.linspace(0.05, 0.1 , 6  ) ]
params['gk2']     = [ x for x in np.linspace(0.1 , 1.0 , 10 ) ]
params['gk3']     = [ x for x in np.linspace(0.1 , 1.0 , 10 ) ]


b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'NaV'
b.saveFolder = 'batch_data'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()