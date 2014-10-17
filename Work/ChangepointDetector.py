import sys
sys.path.insert(0, '../../bayesian_changepoint_detection/')
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from bayesian_changepoint_detection import online_changepoint_detection as online
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')

def generate_normal_time_series(num, minl=50, maxl=1000):
    data = np.array([], dtype=np.float64)
    partition = np.random.randint(minl, maxl, num)
    for p in partition:
        mean = np.random.randn()*10
        var = np.random.randn()*1
        if var < 0:
            var = var * -1
        tdata = np.random.normal(mean, var, p)
        data = np.concatenate((data, tdata))
    return data

data = generate_normal_time_series(7, 50, 200)


fig, ax = plt.subplots(figsize=[16, 12])
ax.plot(data)
plt.savefig("timeseries.png")


import cProfile
import bayesian_changepoint_detection.offline_changepoint_detection as offcd
from functools import partial

Q, P, Pcp = offcd.offline_changepoint_detection(data, partial(offcd.const_prior, l=(len(data)+1)), offcd.gaussian_obs_log_likelihood, truncate=-20)

print Q
print P
print Pcp

fig, ax = plt.subplots(figsize=[18, 16])
ax = fig.add_subplot(2, 1, 1)
ax.plot(data[:])
ax = fig.add_subplot(2, 1, 2, sharex=ax)
ax.plot(np.exp(Pcp).sum(0))

plt.savefig("peaks.png")


import bayesian_changepoint_detection.online_changepoint_detection as oncd

R, maxes = oncd.online_changepoint_detection(data, partial(oncd.constant_hazard, 250), oncd.StudentT(10, .03, 1, 0))

print R
print maxes

import matplotlib.cm as cm
fig, ax = plt.subplots(figsize=[18, 16])
ax = fig.add_subplot(3, 1, 1)
ax.plot(data)
ax = fig.add_subplot(3, 1, 2, sharex=ax)
sparsity = 5  # only plot every fifth data for faster display
ax.pcolor(np.array(range(0, len(R[:,0]), sparsity)),
          np.array(range(0, len(R[:,0]), sparsity)),
          -np.log(R[0:-1:sparsity, 0:-1:sparsity]),
          cmap=cm.Greys, vmin=0, vmax=1000)
ax = fig.add_subplot(3, 1, 3, sharex=ax)
ax.plot(R[:, 1])


plt.savefig("stuff.png")