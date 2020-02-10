from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg


netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams['cfiber'] = {'cellType': 'cfiber', 'numCells': 1, 'cellModel': '_cf'}
#cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber.py', cellName='cfiber')

#calculate navs from config file
#navs = {'nav17': cfg.gna17 * cfg.block[0], 'na18a': cfg.gna18 * cfg.block[1]}
navs = {'nav17': cfg.gna17 * cfg.cndct[0], 'na18a': cfg.gna18 * cfg.cndct[1]}
kvs  = {'kv4'  : 0.01  , 'kv2'  : 0.002 , 'kv1'  : 0.00006 }
#cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber_mkv.py', cellName='cfiber', cellArgs={ 'navs': navs })
cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='fiber.py', cellName='cfiber', cellArgs={ 'navs': navs, 'kvs': kvs})
netParams.cellParams['cfiber'] = cfiber

for delay in cfg.delay:
    netParams.stimSourceParams[delay] = {'type': 'IClamp', 'delay': delay, 'dur': 5, 'amp': 2}
    netParams.stimTargetParams[delay] = {'source': delay, 'conds': {'popLabel': 'cfiber'}, 'sec': 'axnperi', 'loc': 0.0}
