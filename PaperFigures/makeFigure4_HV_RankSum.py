import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns
import scipy.stats as ss

sns.set()

nseeds=10

fig = plt.figure()
ax = fig.add_subplot(2,2,1)
HVmatrix_base = np.zeros([nseeds,101])
HVmatrix_fcst = np.zeros([nseeds,101])
Dstats = np.zeros(100)
pValues = np.ones(100)
for seed in range(nseeds):
    hv = np.loadtxt('../baseline_100/metrics/runtime/baseline_100_S' + str(seed+1) + '.metrics', skiprows=1, usecols=[0])
    HVmatrix_base[seed,(101-len(hv))::] = hv
    l1, = ax.plot(np.arange(0,101,1)*3000, HVmatrix_base[seed,:], linewidth=2, color='#ff7f00')
    
    hv = np.loadtxt('../HydroInfo_100/metrics/runtime/HydroInfo_100_S' + str(seed+1) + '.metrics', skiprows=1, usecols=[0])
    HVmatrix_fcst[seed,(101-len(hv))::] = hv
    l2, = ax.plot(np.arange(0,101,1)*3000, HVmatrix_fcst[seed,:], linewidth=2, color='#4daf4a')
                  
ax.set_ylim([0,0.8])
ax.set_xlim([0,300000])
ax.set_xticks([0,100000,200000,300000])
ax.set_ylabel('Hypervolume')
ax.legend([l1,l2], ['Baseline','Forecast'], loc='upper left', ncol=1)
ax.set_xticklabels('')
ax.set_title('100-yr Flood Objective')

for i in range(100):
    Dstats[i], pValues[i] = ss.ranksums(HVmatrix_base[:,i+1],HVmatrix_fcst[:,i+1])
    
x = np.arange(1,101,1)*3000
points = np.array([x, pValues]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

ax = fig.add_subplot(2,2,3)
cmap = ListedColormap(['#4daf4a','#ff7f00'])
norm = BoundaryNorm([np.min(Dstats), 0, np.max(Dstats)], cmap.N)
lc = LineCollection(segments, cmap=cmap, norm=norm)
lc.set_array(Dstats)
l3 = ax.add_collection(lc)
l4, = ax.plot([1,100*3000],[0.05,0.05],c='k')
ax.set_xlim([0,300000])
ax.set_ylim([0.0,1.0])
ax.set_ylabel('Rank Sum p-value')
ax.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xticks([0,100000,200000,300000])
ax.set_xlabel("NFE/master")

ax.legend([l1,l2,l4],['Baseline Better','Forecast Better','p-value = 0.05'],loc='upper right')

ax = fig.add_subplot(2,2,2)
for seed in range(nseeds):
    hv = np.loadtxt('../baseline_500/metrics/runtime/baseline_500_S' + str(seed+1) + '.metrics', skiprows=1, usecols=[0])
    HVmatrix_base[seed,(101-len(hv))::] = hv
    l1, = ax.plot(np.arange(100-len(hv)+1,101,1)*3000, hv, linewidth=2, color='#377eb8')
    
    hv = np.loadtxt('../HydroInfo_500/metrics/runtime/HydroInfo_500_S' + str(seed+1) + '.metrics', skiprows=1, usecols=[0])
    HVmatrix_fcst[seed,(101-len(hv))::] = hv
    l2, = ax.plot(np.arange(100-len(hv)+1,101,1)*3000, hv, linewidth=2, color='#984ea3')

ax.set_ylim([0,0.8])
ax.set_xlim([0,300000])
ax.set_xticks([0,100000,200000,300000])
ax.legend([l1,l2], ['Baseline','Forecast'], loc='upper left', ncol=1)
ax.set_yticklabels('')
ax.set_xticklabels('')
ax.set_title('500-yr Flood Objective')

for i in range(100):
    Dstats[i], pValues[i] = ss.ranksums(HVmatrix_base[:,i+1],HVmatrix_fcst[:,i+1])

points = np.array([x, pValues]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

ax = fig.add_subplot(2,2,4)
cmap = ListedColormap(['#984ea3','#377eb8'])
norm = BoundaryNorm([np.min(Dstats), 0, np.max(Dstats)], cmap.N)
lc = LineCollection(segments, cmap=cmap, norm=norm)
lc.set_array(Dstats)
l3 = ax.add_collection(lc)
l4, = ax.plot([1,100*3000],[0.05,0.05],c='k')
ax.set_xlim([0,300000])
ax.set_ylim([0.0,1.0])
ax.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xticks([0,100000,200000,300000])
ax.set_xlabel("NFE/master")

ax.legend([l1,l2,l4],['Baseline Better','Forecast Better','p-value = 0.05'],loc='upper right')

fig.set_size_inches([6.4,4.8])
plt.savefig('HV_RankSum.pdf')
plt.clf()