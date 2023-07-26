import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

class Formulation():
    def __init__(self):
        self.name = None
        self.nickname = None
        self.opt100 = None
        self.reeval100 = None
        self.opt500 = None
        self.reeval500 = None
        
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    if name == 'baseline_100':
        formulation.nickname = "BL100"
    elif name == "HydroInfo_100":
        formulation.nickname = "HI100"
    elif name == "baseline_500":
        formulation.nickname = "BL500"
    else:
        formulation.nickname = "HI500"
        
    if name == 'baseline_100' or name == 'HydroInfo_100':
        formulation.opt100 = pd.read_csv('../100yr_refs/optimization/' + name + '.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood100"])
        formulation.opt500 = pd.read_csv('../500yr_refs/optimization/' + name + '_500yr.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood500"])
    elif name == 'baseline_500' or name == 'HydroInfo_500':
        formulation.opt100 = pd.read_csv('../100yr_refs/optimization/' + name + '_100yr.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood100"])
        formulation.opt500 = pd.read_csv('../500yr_refs/optimization/' + name + '.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood500"])
    
    formulation.opt100 = formulation.opt100.drop(np.where(formulation.opt100["Hydro"]=="#")[0][0])
    formulation.opt100["Hydro"] = pd.to_numeric(formulation.opt100["Hydro"])
    formulation.opt500 = formulation.opt500.drop(np.where(formulation.opt500["Hydro"]=="#")[0][0])
    formulation.opt500["Hydro"] = pd.to_numeric(formulation.opt500["Hydro"])
        
    formulation.reeval100 = pd.read_csv('../100yr_refs/reevaluation/' + name + '_re-eval_100yr.reference',
                                        delimiter=' ', header=None, 
                                        names=["Hydro","Deficit","Flood100"])
    formulation.reeval500 = pd.read_csv('../500yr_refs/reevaluation/' + name + '_re-eval_500yr.reference',
                                        delimiter=' ', header=None, 
                                        names=["Hydro","Deficit","Flood500"])
    
    formulation.reeval100 = formulation.reeval100.drop(np.where(formulation.reeval100["Hydro"]=="#")[0][0])
    formulation.reeval100["Hydro"] = pd.to_numeric(formulation.reeval100["Hydro"])
    formulation.reeval500 = formulation.reeval500.drop(np.where(formulation.reeval500["Hydro"]=="#")[0][0])
    formulation.reeval500["Hydro"] = pd.to_numeric(formulation.reeval500["Hydro"])
    
    return formulation

def calcAvgBenefits(leftSet, refSet, floodLevel):
    mergedSet = pd.merge(leftSet, refSet, on=["Hydro","Deficit","Flood" + floodLevel], how="outer", indicator="Exist")
    dominated = mergedSet.iloc[np.where(mergedSet.Exist=='left_only')[0]]
    nondominated = mergedSet.iloc[np.where(mergedSet.Exist=='right_only')[0]]    
    avg_benefits = np.zeros([np.shape(dominated)[0],3])
    for i in range(np.shape(dominated)[0]):
        better_policies = np.intersect1d(np.intersect1d(np.where(nondominated["Hydro"] < dominated["Hydro"].iloc[i])[0],
                                         np.where(nondominated["Deficit"] < dominated["Deficit"].iloc[i])[0]),
                                         np.where(nondominated["Flood" + floodLevel] < dominated["Flood" + floodLevel].iloc[i])[0])
        avg_benefits[i,:] = np.mean(dominated.iloc[i,0:3] - nondominated.iloc[better_policies,0:3])
    
    avg_benefits = np.nanmean(avg_benefits,0)
    if np.all(np.isnan(avg_benefits)):
        avg_benefits = np.zeros([3])
    
    return avg_benefits

def getAvgBenefits(formulation1, formulation2, floodLevel, streamflowSet):
    if streamflowSet == "optimization":
        refSet = pd.read_csv("../" + floodLevel + "yr_refs/" + streamflowSet + "/" + formulation1.nickname + "_" + 
                         formulation2.nickname + "_" + floodLevel + "yr.reference", delimiter = " ", 
                         header=None, names=["Hydro","Deficit","Flood" + floodLevel])
    else:
        refSet = pd.read_csv("../" + floodLevel + "yr_refs/" + streamflowSet + "/" + formulation1.nickname + "_" + 
                         formulation2.nickname + "_re-eval_" + floodLevel + "yr.reference", delimiter = " ", 
                         header=None, names=["Hydro","Deficit","Flood" + floodLevel])
        
    refSet = refSet.drop(np.where(refSet["Hydro"]=="#")[0][0])
    refSet["Hydro"] = pd.to_numeric(refSet["Hydro"])
    
    if streamflowSet == "optimization":
        if floodLevel == "100":
            set1 = formulation1.opt100
            set2 = formulation2.opt100
        else:
            set1 = formulation1.opt500
            set2 = formulation2.opt500
    else:
        if floodLevel == "100":
            set1 = formulation1.reeval100
            set2 = formulation2.reeval100
        else:
            set1 = formulation1.reeval500
            set2 = formulation2.reeval500
            
    avg_benefits = calcAvgBenefits(set1, refSet, floodLevel)
    avg_losses = -calcAvgBenefits(set2, refSet, floodLevel)
    
    return avg_benefits, avg_losses

def makePlotLabels(ax, ylim, ylabel, decimal, title, sign):
    ax.set_ylim(ylim)
    ax.set_ylabel(ylabel,fontsize=14)
    ax.tick_params(axis='y',labelsize=14)
    ax.set_xlim([-0.5,1.5])
    ax.set_xticklabels(['',''])
    if i == 1:
        ax.set_title(title,fontsize=16,pad=10)
        
    yrange = ylim[1] - ylim[0]
    rects = ax.patches
    if sign == "positive":
        for rect in rects[0:2]:
            height = rect.get_height()
            if decimal != 0:
                ax.text(rect.get_x() + rect.get_width()/2, height+yrange/100, str(np.round(height,decimal)),
                    ha='center', va='bottom', fontsize=14)
            else:
                ax.text(rect.get_x() + rect.get_width()/2, height+yrange/100, str(int(height)),
                    ha='center', va='bottom', fontsize=14)
    else:
        for rect in rects[2::]:
            height = rect.get_height()
            if decimal !=0:
                ax.text(rect.get_x() + rect.get_width()/2, height-yrange/10, str(np.round(height,decimal)),
                        ha='center', va='bottom', fontsize=14, color="#e41a1c")                
            else:
                if height <= 0:
                    ax.text(rect.get_x() + rect.get_width()/2, height-yrange/10, str(int(height)),
                        ha='center', va='bottom', fontsize=14, color="#e41a1c")
    
    return None


baseline_100 = getFormulations('baseline_100')
HydroInfo_100 = getFormulations('HydroInfo_100')
baseline_500 = getFormulations('baseline_500')
HydroInfo_500 = getFormulations('HydroInfo_500')

BL100_rect = plt.Rectangle((0, 0), 1, 1, fc="#ff7f00", edgecolor='none')
BL500_rect = plt.Rectangle((0, 0), 1, 1, fc="#377eb8", edgecolor='none')
HI100_rect = plt.Rectangle((0, 0), 1, 1, fc="#4daf4a", edgecolor='none')
HI500_rect = plt.Rectangle((0, 0), 1, 1, fc="#984ea3", edgecolor='none')

# plotting parameters
x = np.arange(2)
hydroMax = 3.5
deficitMax = 600
floodMax = 1
ylabels=[r'$J_{Hydro}$ (Gwh/day)', r'$J_{Deficit^2}$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$', r'$J_{Flood}$ (m)']

streamflows = ["optimization","reevaluation"]
sns.set_style("darkgrid")
for streamflow in streamflows:
    # value/cost of information
    # find avg benefits of HydroInfo_100 policies over baseline_100 policies they dominate in 100-yr space
    HI100_over_BL100, HI100_under_BL100 = getAvgBenefits(baseline_100, HydroInfo_100, "100", streamflow)
    
    # find avg benefits of HydroInfo_500 policies over baseline_100 policies they dominate in 100-yr space
    HI500_over_BL100, HI500_under_BL100 = getAvgBenefits(baseline_100, HydroInfo_500, "100", streamflow)
    
    # find avg benefits of HydroInfo_500 policies over baseline_500 policies they dominate in 500-yr space
    HI500_over_BL500, HI500_under_BL500 = getAvgBenefits(baseline_500, HydroInfo_500, "100", streamflow)
    
    # find avg benefits of HydroInfo_100 policies over baseline_500 policies they dominate in 500-yr space
    HI100_over_BL500, HI100_under_BL500 = getAvgBenefits(baseline_500, HydroInfo_100, "100", streamflow)
    
    # value/cost of constraints
    # find avg benefits of baseline_100 policies over baseline_500 policies they dominate in 100-yr space
    BL500_over_BL100_100yr, BL500_under_BL100_100yr = getAvgBenefits(baseline_100, baseline_500, "100", streamflow)
    
    # find avg benefits of HydroInfo_100 policies over HydroInfo_500 policies they dominate in 100-yr space
    HI500_over_HI100_100yr, HI500_under_HI100_100yr = getAvgBenefits(HydroInfo_100, HydroInfo_500, "100", streamflow)
    
    # find avg benefits of baseline_500 policies over baseline_100 policies they dominate in 500-yr space
    BL100_over_BL500_500yr, BL100_under_BL500_500yr = getAvgBenefits(baseline_500, baseline_100, "500", streamflow)
    
    # find avg benefits of HydroInfo_500 policies over HydroInfo_100 policies they dominate in 500-yr space
    HI100_over_HI500_500yr, HI100_under_HI500_500yr = getAvgBenefits(HydroInfo_500, HydroInfo_100, "500", streamflow)
    
    decimals = [1, 0, 2]
    fig = plt.figure()
    for i in range(3):
        if i == 0:
            ylim = [-hydroMax, hydroMax]
        elif i == 1:
            ylim = [-deficitMax, deficitMax]
        else:
            ylim = [-floodMax, floodMax]
            
        ax = fig.add_subplot(2,3,i+1)
        ax.bar(x, [HI100_over_BL100[i], HI500_over_BL100[i]], color=["#4daf4a", "#984ea3"]) # green, purple
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of Forecast Information vs. Baseline 100", "positive")
        ax.bar(x, [HI100_under_BL100[i], HI500_under_BL100[i]], color=["#4daf4a", "#984ea3"]) # green, purple
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of Forecast Information vs. Baseline 100", "negative")
        
        ax = fig.add_subplot(2,3,i+4)
        ax.bar(np.arange(2), [HI100_over_BL500[i], HI500_over_BL500[i]], color=["#4daf4a","#984ea3"])
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of Forecast Information vs. Baseline 500", "positive")
        ax.bar(np.arange(2), [HI100_under_BL500[i], HI500_under_BL500[i]], color=["#4daf4a","#984ea3"])
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of Forecast Information vs. Baseline 500", "negative")
    
    fig.set_size_inches([10.6,6.7])
    fig.subplots_adjust(bottom=0.15,wspace=0.5)
    fig.legend([HI100_rect, HI500_rect],['Forecast 100', 'Forecast 500'], loc = 'lower center', ncol=4, fontsize=16)
    fig.savefig("VOI_fcst_" + streamflow + ".pdf")
    fig.clf()
    
    fig = plt.figure()
    for i in range(3):
        if i == 0:
            ylim = [-hydroMax, hydroMax]
        elif i == 1:
            ylim = [-deficitMax, deficitMax]
        else:
            ylim = [-floodMax-0.5, floodMax+0.5]
    
        ax = fig.add_subplot(2,3,i+1)
        ax.bar(x, [BL500_over_BL100_100yr[i], HI500_over_HI100_100yr[i]], color=["#377eb8","#984ea3"]) # blue, purple
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of 500-yr Constraint on 100-yr Formulation", "positive")
        ax.bar(x, [BL500_under_BL100_100yr[i], HI500_under_HI100_100yr[i]], color=["#377eb8","#984ea3",]) # blue, purple
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of 500-yr Constraint on 100-yr Formulation", "negative")
        
        ax = fig.add_subplot(2,3,i+4)
        ax.bar(x, [BL100_over_BL500_500yr[i], HI100_over_HI500_500yr[i]], color=["#ff7f00","#4daf4a"]) # orange, green
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of 100-yr Constraint on 500-yr Formulation", "positive")
        ax.bar(x, [BL100_under_BL500_500yr[i], HI100_under_HI500_500yr[i]], color=["#ff7f00","#4daf4a"]) # orange, green
        makePlotLabels(ax, ylim, ylabels[i], decimals[i], 
                       "Average Value/Cost of 100-yr Constraint on 500-yr Formulation", "negative")
            
    fig.set_size_inches([10.6,6.7])
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15,wspace=0.5)
    fig.legend([BL100_rect, BL500_rect, HI100_rect, HI500_rect],['Baseline 100', 'Baseline 500', 'Forecast 100', 'Forecast 500'],
               loc = 'lower center', ncol=4, fontsize=16)
    fig.savefig("VOI_constraint_" + streamflow + ".pdf")
    fig.clf()
