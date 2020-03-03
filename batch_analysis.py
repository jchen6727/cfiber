import json
import numpy as np
from collections import OrderedDict as ODict
import matplotlib.pyplot as plt
from analysis import analysis
from itertools import product

bdir = "batch_cndct/"
bcfg = "cndct_batch.json"
bprm = ODict()
sims = ODict()

with open(bdir + bcfg, "r") as fp:
    jdata = json.load(fp)

blbl = jdata['batch']['batchLabel']

dimensions = []
bprm_keys = []
for prm in jdata['batch']['params']:
    bprm[prm["label"]] = prm["values"]
    bprm_keys.append( prm["label"] )
    dimensions.append( len( prm["values"] ) )
#generate filenames for analysis.

filenames = []

aix = [] # analyzed indexes
vel = [] # peripheral velocity
pkp = [] # peak voltage axon
pks = [] # peak voltage soma
pkc = [] # peak voltage central


#generate indexes
for ixs in product(*[range(x) for x in dimensions]):
    filename = blbl

    for i in ixs:
        filename = filename + "_%i"

    #for now, I just want to see what's going on for one stimulus
    #ignore interval data, so ixs[1] to 5 should space them far enough away?

    if ixs[1] == 5:
        a = analysis("%s.json" %(filename) , "analysis/%s" %(filename))
        if a.fexist:
            aix.append(ixs)
            vel.append(a.get_vel(300, 400))
            a.plot_traces( "voltage", "mv", "v")
            a.plot_soma(300, 400)
            pkp.append(a.get_spike('v9')['peak'])
            pks.append(a.get_spike('vs')['peak'])
            pkc.append(a.get_spike('vc')['peak'])










"""
while i < ( len(bprm_keys) - 1 ):
    filename = blbl
    for i in len(bprm[key]):
        filename = filename + "_%i" %(i)
        for i in len(bprm)
"""