from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

netParams.popParams['cfiber'] = {'cellType': 'cfiber', 'numCells': 1, 'cellModel': '_cf'}
cfiber=netParams.importCellParams(label='cfiber', conds={'cellType': 'cfiber'}, fileName='cfiber.py', cellName='cfiber')
netParams.cellParams['cfiber'] = cfiber

netParams.stimSourceParams['stim'] = {'type': 'IClamp', 'delay': 0, 'dur': 5, 'amp': 2}
netParams.stimTargetParams['stim'] = {'source': 'stim', 'conds': {'popLabel': 'cfiber'}, 'sec': 'axnperi', 'loc': 0.0}
