from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg


netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.popParams['cnrn']  = {'cellType': 'cnrn' , 'numCells': 1, 'cellModel': '_cnrn' }

navs = {'nav17': cfg.gna17 * cfg.nacndct[0], 
        'nav18': cfg.gna18 * cfg.nacndct[1], 
        'na19a': cfg.gna19 * cfg.nacndct[2]}
# more complex potassium channel config, not very useful until we get a 
kvs  = {#'kv1'  : cfg.gk1   * cfg.kcndct[0] ,
        'kv2'  : cfg.gk2   * cfg.kcndct[1] ,
        'kv3'  : cfg.gk3   * cfg.kcndct[2] ,
        #'kv4'  : cfg.gk4   * cfg.kcndct[3] , 
        'kv7'  : cfg.gk7   * cfg.kcndct[4] }

cavs = {'cal'  : cfg.gca }

args = {'navs' : navs,      'kvs': kvs,         'cavs': cavs,
        'navq' : cfg.navq,  'kvq': cfg.kvq,          
        'ena'  : cfg.ena,   'ek': cfg.ek, 
        'vrest': cfg.vrest, 'gm': cfg.gm, 
        'rmut' : cfg.rmut,
        'L'    : cfg.L,     'nseg': cfg.nseg,
        'connect': 'all'}
 
cnrnParams  = netParams.importCellParams(label='cnrn' , conds={'cellType': 'cnrn' }, fileName='cnrn.py' , cellName='cnrn' , cellArgs=args)

netParams.cellParams['cnrn' ] = cnrnParams

# current clamp block
for delay in cfg.delay:
    key = 'ic%i'%delay
    netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': delay, 'dur': 2.5, 'amp': 0.5}
    netParams.stimTargetParams[key] = {'source': key, 'conds': {'popLabel': 'cnrn' }, 'sec': 'axnperi', 'loc': 0.0}


"""
# Voltage clamp block
for delay in cfg.delay:
    key = 'vc%i'%delay
    netParams.stimSourceParams[key] = {'type': 'VClamp', 'dur': [delay, 2.5, 2.5], 'amp': [-57, 10, -57]}
    netParams.stimTargetParams[key] = {'source': key, 'conds': {'popLabel': 'cnrn'}, 'sec': 'drgsoma', 'loc': 0.5}
"""


#key = 'vc%i'%delay
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {'type': 'VClamp'}
#netParams.stimSourceParams['vc%i'%cfg.delay[0]] = {}