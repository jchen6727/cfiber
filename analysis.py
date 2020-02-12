import json

import numpy as np

rvs = ['v%i' for i in range(11)]

with open("sim1.json", "r") as rf:
    data = json.load(rf)


# look at some AP for morphology

# base AP duration
th = -59.5
v  = data['simdata']['v3']['cell_0']
t  = data['simdata']['t']


mask = np.diff( 1 * ( v > th ) != 0) 

t[mask][1] - t[mask][0]


v10 = data['s']
data[]

