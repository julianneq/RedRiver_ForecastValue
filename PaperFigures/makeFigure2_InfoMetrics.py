import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pareto import eps_sort
import copy

# synthetic baseline Pareto set
set1 = np.array([[0,5],[1/3,5-2/3],[2/3,5-4/3],
                 [1,3],[1+2/3,3-2/3],[1+4/3,3-4/3],
                 [3,1],[3+2/3,1-1/3],[3+4/3,1-2/3],[5,0]])

set1[:,1] = set1[:,1] + 3

# synthetic forecast Pareto set
set2 = np.array([[0,7],[0.5,6],[1,5],[1.5,4],[2,3],
                 [2.5,2],[3,1],[3.5,0],[4,-1]])

set2[:,0] = set2[:,0] + 0.75
set2[:,1] = set2[:,1] + 1.25

# find reference set
set1 = pd.DataFrame(set1, columns=["Obj1","Obj2"])
set2 = pd.DataFrame(set2, columns=["Obj1","Obj2"])
refSet = eps_sort([set1,set2])
refSet = pd.DataFrame(refSet, columns=["Obj1","Obj2"])

# find ideal and nadir point; extend Pareto set by 1 to define nadir point
idealPoint = [np.min([np.min(set1["Obj1"]), np.min(set2["Obj1"])]), np.min([np.min(set1["Obj2"]), np.min(set2["Obj2"])])]
nadirPoint = [np.max([np.max(set1["Obj1"]), np.max(set2["Obj1"])])+1, np.max([np.max(set1["Obj2"]), np.max(set2["Obj2"])])+1]

# extend Pareto sets to extent of ideal and nadir point for plottiing
set1_extended = copy.copy(set1)
set1_extended.loc[-1] = [np.min(set1["Obj1"]), nadirPoint[1]]
set1_extended.index = set1_extended.index + 1
set1_extended = set1_extended.sort_index()
set1_extended.loc[len(set1_extended)] = [nadirPoint[0], np.min(set1["Obj2"])]

set2_extended = copy.copy(set2)
set2_extended.loc[-1] = [np.min(set2["Obj1"]), nadirPoint[1]]
set2_extended.index = set2_extended.index + 1
set2_extended = set2_extended.sort_index()
set2_extended.loc[len(set2_extended.index)] = [nadirPoint[0], np.min(set2["Obj2"])]

def calcHypervolume(setPts, idealPt, nadirPt):
    totalVol = (nadirPt[1]-idealPt[1]) * (nadirPt[0]-idealPt[0])
    
    rawHV = (nadirPt[0] - setPts["Obj1"].iloc[0]) * (nadirPt[1] - setPts["Obj2"].iloc[0])
    for i in range(1,len(setPts.index)-1):
        rawHV += (nadirPt[0] - setPts["Obj1"].iloc[i+1]) * (setPts["Obj2"].iloc[i] - setPts["Obj2"].iloc[i+1])
    
    HV = rawHV/totalVol
    
    return HV

# calculate hypervolume of each set and reference set across them
set1_HV = calcHypervolume(set1, idealPoint, nadirPoint)
set2_HV = calcHypervolume(set2, idealPoint, nadirPoint)
refSet_HV = calcHypervolume(refSet, idealPoint, nadirPoint)
shared_HV = set1_HV + set2_HV - refSet_HV
set1_extraHV = set1_HV - shared_HV
set2_extraHV = set2_HV - shared_HV

def calcAvgBenefits(leftSet, refSet):
    mergedSet = pd.merge(leftSet, refSet, on=["Obj1","Obj2"], how="outer", indicator="Exist")
    dominated = mergedSet.iloc[np.where(mergedSet.Exist=='left_only')[0]]
    nondominated = mergedSet.iloc[np.where(mergedSet.Exist=='right_only')[0]]    
    avg_benefits = np.zeros([np.shape(dominated)[0],2])
    for i in range(np.shape(dominated)[0]):
        better_policies = np.intersect1d(np.where(nondominated["Obj1"] < dominated["Obj1"].iloc[i])[0],
                                         np.where(nondominated["Obj2"] < dominated["Obj2"].iloc[i])[0])
        avg_benefits[i,:] = np.mean(dominated.iloc[i,0:2] - nondominated.iloc[better_policies,0:2])
    
    avg_benefits = np.nanmean(avg_benefits,0)
    if np.all(np.isnan(avg_benefits)):
        avg_benefits = np.zeros([2])
    
    return avg_benefits

# calculate average benefits/costs of forecast
set2_benefits = calcAvgBenefits(set1, refSet)
set2_losses = -calcAvgBenefits(set2, refSet)


# plot value metrics
sns.set_style("white")
fig = plt.figure(figsize=[10.2,8.6])

# illustration of multivariate value: hypervolume
ax1 = fig.add_subplot(2,2,1)
p2 = ax1.scatter(set2["Obj1"],set2["Obj2"],color='tab:red',s=50,linewidth=2)
p1 = ax1.scatter(set1["Obj1"],set1["Obj2"],color='tab:pink',s=50,linewidth=2)
set2_line = ax1.step(set2_extended["Obj1"],set2_extended["Obj2"],where='post',color='tab:red',linewidth=2)
set1_line = ax1.step(set1_extended["Obj1"],set1_extended["Obj2"],where='post',color='tab:pink',linewidth=2)
set2_top = ax1.plot(set2_extended["Obj1"],np.ones(len(set2_extended["Obj1"]))*6,color='none')
set1_top = ax1.plot(set1_extended["Obj1"],np.ones(len(set1_extended["Obj1"]))*6,color='none')
ax1.fill_between(set2_extended["Obj1"],set2_extended["Obj2"],nadirPoint[1],step='post',color="tab:red",alpha=0.3)
ax1.fill_between(set1_extended["Obj1"],set1_extended["Obj2"],nadirPoint[1],step='post',color="tab:pink",alpha=0.3)
nadirPt = ax1.scatter(nadirPoint[0],nadirPoint[1],color="black",s=50,linewidth=2)
idealPt = ax1.scatter(idealPoint[0],idealPoint[1],ec="black",fc="yellow",marker='*',s=200)
ax1.legend([p1,p2,idealPt,nadirPt],['Baseline','Forecast','Ideal Point','Nadir Point'],
          loc='upper right', bbox_to_anchor=[0.95, 0.95], fontsize=14)
ax1.set_xlabel("Objective 1",fontsize=16)
ax1.set_ylabel("Objective 2",fontsize=16)
ax1.tick_params(axis='both',labelsize=14)
ax1.text(4,4.5,str(np.round(shared_HV,2)),fontsize=14)
ax1.text(5,1.5,str(np.round(set2_extraHV,2)),fontsize=14)
ax1.text(0,5.5,str(np.round(set1_extraHV,2)),fontsize=14)
ax1.arrow(0.6, 6, 0.5, 1.0, color="black", head_width=0.15, head_length=1.5*0.15, length_includes_head=True)

# hypervolume bar chart
ax2 = fig.add_subplot(2,2,3)
ax2.bar(range(2), [set1_HV, set2_HV], color=['tab:pink','tab:red'])
ax2.set_xticks(range(2))
ax2.set_xticklabels(['Baseline','Forecast'],fontsize=16)
ax2.set_ylim([0,1])
ax2.tick_params(axis='y',labelsize=14)
ax2.set_ylabel('Hypervolume',fontsize=16)
rects = ax2.patches
for rect in rects:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, height+0.01, str(np.round(height,2)),
            ha='center',va='bottom',fontsize=14)

# illustration of univariate value: average improvement of nondominated points/loss of dominated points
ax3 = fig.add_subplot(2,2,2)
p2 = ax3.scatter(set2["Obj1"],set2["Obj2"],color='tab:red',linewidth=3)
p1 = ax3.scatter(set1["Obj1"],set1["Obj2"],color='tab:pink',linewidth=3)
set2_line = ax3.step(set2_extended["Obj1"],set2_extended["Obj2"],where='post',color='tab:red',linewidth=2)
set1_line = ax3.step(set1_extended["Obj1"],set1_extended["Obj2"],where='post',color='tab:pink',linewidth=2)
set2_top = ax3.plot(set2_extended["Obj1"],np.ones(len(set2_extended["Obj1"]))*6,color='none')
set1_top = ax3.plot(set1_extended["Obj1"],np.ones(len(set1_extended["Obj1"]))*6,color='none')
ax3.fill_between(set2_extended["Obj1"],set2_extended["Obj2"],nadirPoint[1],step='post',color="tab:red",alpha=0.3)
ax3.fill_between(set1_extended["Obj1"],set1_extended["Obj2"],nadirPoint[1],step='post',color="tab:pink",alpha=0.3)
nadirPt = ax3.scatter(nadirPoint[0],nadirPoint[1],color="black",s=50,linewidth=2)
idealPt = ax3.scatter(idealPoint[0],idealPoint[1],ec="black",fc="yellow",marker='*',s=200)
ax3.set_xlabel("Objective 1",fontsize=16)
ax3.set_ylabel("Objective 2",fontsize=16)
ax3.tick_params(axis='both',labelsize=14)

def plotValueLine(leftSet, refSet, ax, color):
    mergedSet = pd.merge(leftSet, refSet, on=["Obj1","Obj2"], how="outer", indicator="Exist")
    dominated = mergedSet.iloc[np.where(mergedSet.Exist=='left_only')[0]]
    nondominated = mergedSet.iloc[np.where(mergedSet.Exist=='right_only')[0]] 
    for i in range(np.shape(dominated)[0]):
        better_policies = np.intersect1d(np.where(nondominated["Obj1"] < dominated["Obj1"].iloc[i])[0],
                                         np.where(nondominated["Obj2"] < dominated["Obj2"].iloc[i])[0])
        for j in range(len(better_policies)):
            obj1_line, = ax.plot([dominated["Obj1"].iloc[i], nondominated["Obj1"].iloc[better_policies[j]]],
                                [dominated["Obj2"].iloc[i], dominated["Obj2"].iloc[i]], color=color, linestyle="dashed",linewidth=2)
            ax.scatter(nondominated["Obj1"].iloc[better_policies[j]], dominated["Obj2"].iloc[i], color=color)
            obj2_line, = ax.plot([dominated["Obj1"].iloc[i], dominated["Obj1"].iloc[i]],
                                [dominated["Obj2"].iloc[i], nondominated["Obj2"].iloc[better_policies[j]]], 
                                color=color, linestyle="dotted",linewidth=2)
            ax.scatter(dominated["Obj1"].iloc[i], nondominated["Obj2"].iloc[better_policies[j]], color=color)
            
    return obj1_line, obj2_line

# plot lines showing gains of nondominated forecast points over baseline dominated points
obj1_value, obj2_value = plotValueLine(set1, refSet, ax3, "black")

# plot lines showing losses of dominated forecast points by baseline nondominated points
obj1_losses, obj2_losses = plotValueLine(set2, refSet, ax3, "tab:brown")

ax3.legend([obj1_value, obj2_value, obj1_losses, obj2_losses],['Obj1 Gains', 'Obj2 Gains', 'Obj1 Losses', 'Obj2 Losses'],
           loc='upper right', bbox_to_anchor=[0.95, 0.95], fontsize=14)

def makePlotLabels(ax, ylim, sign):
    ax.set_ylim(ylim)
    #ax.tick_params(axis='y',labelsize=14)
    #ax.set_xlim([-0.5,1.5])
        
    yrange = ylim[1] - ylim[0]
    rects = ax.patches
    if sign == "positive":
        for rect in rects[0:2]:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height+yrange/100, str(np.round(height,2)),
                ha='center', va='bottom', fontsize=14)
    else:
        for rect in rects[2::]:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height-yrange/14, str(np.round(height,2)),
                    ha='center', va='bottom', fontsize=14, color="#e41a1c")
    
    return None

# univariate value bar chart
ax4 = fig.add_subplot(2,2,4)
ax4.bar(range(2), set2_benefits, color='tab:red')
makePlotLabels(ax4, [-1,1.25], 'positive')
ax4.bar(range(2), set2_losses, color='tab:red')
makePlotLabels(ax4, [-1,1.25], 'negative')
ax4.set_xticks(range(2))
ax4.set_xticklabels(['Objective 1','Objective 2'],fontsize=16)
ax4.set_ylabel('Average Value/Cost of\nForecast Information',fontsize=16)
ax4.tick_params(axis='y',labelsize=14)

fig.tight_layout()
fig.savefig("InfoMetrics.pdf")
fig.clf()
