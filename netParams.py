from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg


netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams['cfiber'] = {'cellType': 'cfiber', 'numCells': 1, 'cellModel': '_cf'}
#cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber.py', cellName='cfiber')

#calculate navs from config file
navs = {'na17a': cfg.gna17 * cfg.block[0], 'na18a': cfg.gna18 * cfg.block[1]}
cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber_mkv.py', cellName='cfiber', cellArgs={ 'navs': navs })
netParams.cellParams['cfiber'] = cfiber

netParams.stimSourceParams['stim'] = {'type': 'IClamp', 'delay': 250, 'dur': 5, 'amp': 2}
netParams.stimTargetParams['stim'] = {'source': 'stim', 'conds': {'popLabel': 'cfiber'}, 'sec': 'axnperi', 'loc': 0.0}
