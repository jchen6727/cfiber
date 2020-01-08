from netpyne import specs
from netpyne.batch import Batch

params = specs.ODict()

params['gnabar17'] = []
params['gnabar18'] = []
params['gnabar19'] = []

b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'NaV'
b.saveFolder = 'batch_data'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()