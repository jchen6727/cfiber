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
kvs  = {'kv4'  : cfg.gk4 , 'kv2'  : cfg.gk2 , 'kv1'  : cfg.gk1 }
#cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber_mkv.py', cellName='cfiber', cellArgs={ 'navs': navs })
cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='fiber.py', cellName='cfiber', cellArgs={ 'navs': navs, 'kvs': kvs, 'ena': cfg.ena, 'ek': cfg.ek, 'vrest': cfg.vrest, 'gm': cfg.gm})
netParams.cellParams['cfiber0'] = cfiber
#netParams.cellParams['cfiber1'] = cfiber

for delay in cfg.delay:
    key = 'ic%i'%delay
    netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': delay, 'dur': 5, 'amp': 0.5}
    netParams.stimTargetParams[key] = {'source': key, 'conds': {'popLabel': 'cfiber'}, 'sec': 'axnperi', 'loc': 0.0}

#key = 'vc%i'%delay
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {'type': 'VClamp'}
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {}