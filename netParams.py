from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg


netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams['cfiber'] = {'cellType': 'cfiber', 'numCells': 1, 'cellModel': '_cf'}
#cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber.py', cellName='cfiber')
cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber_mkv.py', cellName='cfiber', cellArgs={'gnabar17': cfg.gnabar17, 'gnabar18': cfg.gnabar18, 'gnabar19': cfg.gnabar19})
netParams.cellParams['cfiber'] = cfiber

netParams.stimSourceParams['stim'] = {'type': 'IClamp', 'delay': 50, 'dur': 5, 'amp': 2}
netParams.stimTargetParams['stim'] = {'source': 'stim', 'conds': {'popLabel': 'cfiber'}, 'sec': 'axnperi', 'loc': 0.0}
