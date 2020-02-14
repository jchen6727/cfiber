from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg


netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams['cnrn']  = {'cellType': 'cnrn' , 'numCells': 1, 'cellModel': '_cnrn' }
netParams.popParams['csoma'] = {'cellType': 'csoma', 'numCells': 1, 'cellModel': '_csoma'}
#calculate navs from config file
#navs = {'nav17': cfg.gna17 * cfg.block[0], 'na18a': cfg.gna18 * cfg.block[1]}
navs = {'nav17': cfg.gna17 * cfg.cndct[0], 'na18a': cfg.gna18 * cfg.cndct[1]}
kvs  = {'kv7'  : cfg.gk7 , 'kv4'  : cfg.gk4 , 'kv2'  : cfg.gk2} #, 'kv1'  : cfg.gk1 }

args = {'navs': navs, 'kvs': kvs, 'ena': cfg.ena, 'ek': cfg.ek, 'vrest': cfg.vrest, 'gm': cfg.gm} 
cnrnParams  = netParams.importCellParams(label='cnrn' , conds={'cellType': 'cnrn' }, fileName='cnrn.py' , cellName='cnrn' , cellArgs=args)
cdrgParams  = netParams.importCellParams(label='cdrg' , conds={'cellType': 'cdrg' }, fileName='cdrg.py' , cellName='cdrg' , cellArgs=args)
csomaParams = netParams.importCellParams(label='csoma', conds={'cellType': 'csoma'}, fileName='csoma.py', cellName='csoma', cellArgs=args)


netParams.cellParams['cnrn' ] = cnrnParams
netParams.cellParams['cdrg' ] = cdrgParams
netParams.cellParams['csoma'] = csomaParams

#netParams.cellParams['cfiber1'] = cfiber


for delay in cfg.delay:
    key = 'ic%i'%delay
    netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': delay, 'dur': 2.5, 'amp': 0.5}
    netParams.stimTargetParams[key] = {'source': key, 'conds': {'popLabel': 'cnrn' }, 'sec': 'axnperi', 'loc': 0.0}
"""
for delay in cfg.delay:
    key = 'vc%i'%delay
    netParams.stimSourceParams[key] = {'type': 'VClamp', 'dur': [delay, 50, 0], 'amp': [cfg.vrest, 10, cfg.vrest]}
    netParams.stimTargetParams[key] = {'source': key, 'conds': {'popLabel': 'csoma'}, 'sec': 'axnperi', 'loc': 0.0}
"""
#key = 'vc%i'%delay
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {'type': 'VClamp'}
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {}