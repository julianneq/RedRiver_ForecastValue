import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.gridspec import GridSpec
import seaborn as sns
import pandas as pd
from utils import getFormulations
        
def makeFigure4_ParallelAxes(opt=True):
    # load formulations
    baseline_100 = getFormulations('baseline_100')
    HydroInfo_100 = getFormulations('HydroInfo_100')
    baseline_500 = getFormulations('baseline_500')
    HydroInfo_500 = getFormulations('HydroInfo_500')
    formulations = [baseline_100, HydroInfo_100, baseline_500, HydroInfo_500]
    
    # negate maximization objective (hydropower)
    for formulation in formulations:
        formulation.reeval_1000[:,0] = -formulation.reeval_1000[:,0]
        formulation.reeval_100000[:,0] = -formulation.reeval_100000[:,0]
    
    # plotting features
    labels = [r'$J_{Hydro}$' + '\n(Gwh/day)',\
        r'$J_{Deficit^2}$' + '\n' + '(m$\mathregular{^3}\!$/s)$\mathregular{^2}$',\
        r'$J_{Flood,100}$' + '\n(m above' + '\n11.25 m)',\
        r'$J_{Flood,500}$' + '\n(m above' + '\n11.25 m)']
    precision = [1,0,2,2]
    colors = ['#ff7f00','#4daf4a','#377eb8','#984ea3']
    
    # compute minimum and maximum across formulations for each axis
    BL100mins = np.min(baseline_100.reeval_1000,0)
    BL100maxs = np.max(baseline_100.reeval_1000,0)
    BL500mins = np.min(baseline_500.reeval_1000,0)
    BL500maxs = np.max(baseline_500.reeval_1000,0)
    HI100mins = np.min(HydroInfo_100.reeval_1000,0)
    HI100maxs = np.max(HydroInfo_100.reeval_1000,0)
    HI500mins = np.min(HydroInfo_500.reeval_1000,0)
    HI500maxs = np.max(HydroInfo_500.reeval_1000,0)
    minVals = np.zeros(5)
    maxVals = np.zeros(5)
    for j in range(5):
        minVals[j] = min(BL100mins[j],BL500mins[j],HI100mins[j],HI500mins[j])
        maxVals[j] = max(BL100maxs[j],BL500maxs[j],HI100maxs[j],HI500maxs[j])
        
    # remove maxDef column
    minVals = minVals[[0,1,3,4]]
    maxVals = maxVals[[0,1,3,4]]
        
    # make figure
    sns.set_style("dark")
    fig = plt.figure()
    gs = GridSpec(1,5,figure=fig)
    ax1 = fig.add_subplot(gs[0,0:2])
    
    # plot each formulation
    for i in range(len(formulations)):
        table = pd.DataFrame(formulations[i].reeval_1000[:,[0,1,3,4]],columns=labels)
        if opt == True:
            if formulations[i].name == 'baseline_100' or formulations[i].name == 'HydroInfo_100':
                parallel_coordinate(fig, ax1, table, formulations[i].reeval_1000[:,[0,1,3,4]], \
                            minVals, maxVals, precision, [formulations[i].compromise100_opt], colors[i])
            else:
                parallel_coordinate(fig, ax1, table, formulations[i].reeval_1000[:,[0,1,3,4]], \
                            minVals, maxVals, precision, [formulations[i].compromise500_opt], colors[i])
        else:
            if formulations[i].name == 'baseline_100' or formulations[i].name == 'HydroInfo_100':
                parallel_coordinate(fig, ax1, table, formulations[i].reeval_1000[:,[0,1,3,4]], \
                            minVals, maxVals, precision, [formulations[i].compromise100_reeval], colors[i])
            else:
                parallel_coordinate(fig, ax1, table, formulations[i].reeval_1000[:,[0,1,3,4]], \
                            minVals, maxVals, precision, [formulations[i].compromise500_reeval], colors[i])
    
    # create newlabels so they aren't appended to labels each time
    newlabels=[]
    for k in range(len(labels)):
        if precision[k] != 0:
            if j>3:
                newlabels.append(str(np.round(minVals[k],precision[k])) + '\n' + labels[k])
            else:
                newlabels.append(str(np.round(minVals[k],precision[k])))
        else:
            if j>3:
                newlabels.append(str(int(minVals[k]))+ '\n' + labels[k])
            else:
                newlabels.append(str(int(minVals[k])))
        
        # don't show negative sign on maximization objectives
        if minVals[k] < 0:
            newlabels[k] = newlabels[k][1:]
        
    # round number of significant digits shown on objective labels
    toplabels = []
    for i in range(len(precision)):
        if precision[i] != 0:
            toplabels.append(str(np.round(maxVals[i],precision[i])))
        else:
            toplabels.append(str(int(maxVals[i])))
        if maxVals[i] < 0:
            # don't show negative sign on maximization objectives
            toplabels[i] = toplabels[i][1:]
            
    ax1.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax1.set_yticks([])
    ax1.plot([2.9,3],[2.15/maxVals[3],2.15/maxVals[3]],c='k')
    ax1.plot([2.9,2.9],[2.15/maxVals[3],1],c='k')
    ax1.plot([2.9,3],[1,1],c='k')
    ax1.set_xlim([0,np.shape(table)[1]-1])
    ax1.set_ylim([0,1])
    ax1.set_xticklabels(newlabels,fontsize=16)
    
    # make subplot frames invisible
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax1.plot([i,i],[0,1],c='k')
    
    # create twin y axis to put x tick labels on top
    ax2 = ax1.twiny()
    ax2.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax2.set_yticks([])
    ax2.set_xlim([0,np.shape(table)[1]-1])
    ax2.set_ylim([0,1])
    ax2.set_xticklabels(toplabels,fontsize=16)
    
    # make subplot frames invisible
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    
    
    # make table of values
    sns.set_style("white")
    ax3 = fig.add_subplot(gs[0,2:])
    
    # negate maximization objective (hydropower)
    for formulation in formulations:
        formulation.reeval_1000[:,0] = -formulation.reeval_1000[:,0]
        formulation.reeval_100000[:,0] = -formulation.reeval_100000[:,0]
    
    rowNames = ['Baseline 100','Forecast 100','Baseline 500','Forecast 500']
    colNames =  [r'$J_{Hydro}$ (Gwh/day)', r'$J_{Deficit^2}$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$', \
                r'$J_{Flood,100}$ (m)', r'$J_{Flood,500}$ (m)']
    table_vals, cellColors, sm = getTableData(baseline_100, baseline_500, HydroInfo_100, HydroInfo_500,
                                          rowNames, colNames, opt)
    table = ax3.table(cellText=table_vals, cellColours=cellColors, cellLoc='center', 
                      rowLabels=rowNames, colLabels=colNames, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    
    cellDict = table.get_celld()
    for j in range(len(rowNames)+1):
        for i in range(-1,len(colNames)):
            if j==0 and i==-1:
                pass
            else:
                cellDict[(j,i)].set_height(0.26)
    
    ax3.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax3.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)
        
    cbar = plt.colorbar(sm, ax=ax3, orientation='horizontal', fraction=0.1, aspect=30)
    cbar.set_ticks([0,1])
    cbar.set_ticklabels(['Unfavorable','Favorable'])
    cbar.ax.tick_params(labelsize=16)
        
    fig.set_size_inches([17.4,5.3])
    fig.tight_layout()
    if opt == True:
        fig.savefig('ParallelAxes_opt.pdf')
    else:
        fig.savefig('ParallelAxes_reeval.pdf')
    fig.clf()
    
    return None
    
def parallel_coordinate(fig, ax1, table, shade, mins, maxs, \
    precision, indices, color):
    
    newShade = np.copy(shade)
    minShade = np.min(shade)
    maxShade = np.max(shade)
    for i in range(len(shade)):
        newShade[i] = (shade[i]-minShade)/(maxShade-minShade)
        
    scaled = table.copy()
    index = 0
    for column in table.columns:
        scaled[column] = (table[column] - mins[index]) / (maxs[index] - mins[index])
        index = index + 1
    
    index = 0
    for k, solution in enumerate(scaled.iterrows()):
        ys = solution[1]
        xs = range(len(ys))
        if k in indices:
            # make line for most select solutions thicker and opaque
            ax1.plot(xs, ys, c=color, linewidth=2, \
                path_effects=[pe.Stroke(linewidth=5, foreground='k'), pe.Normal()], \
                    zorder=np.shape(table)[0])
            
        index = index + 1
    
    return ax1, fig

def getTableData(BL100, BL500, HI100, HI500, rowNames, colNames, opt=True):
    
    formulations = [BL100, HI100, BL500, HI500]
    
    # collect data into table (nested list caled table_vals)
    table_vals = []
    for i, formulation in enumerate(formulations):
        if opt==True:
            if formulation == 'baseline_100' or formulation == 'HydroInfo_100':
                solns = [formulation.compromise100_opt]
            else:
                solns = [formulation.compromise500_opt]
            for j, soln in enumerate(solns):
                row_vals = [np.round(formulation.reeval_1000[soln,0],1), int(np.round(formulation.reeval_1000[soln,1],0)), \
                            np.round(formulation.reeval_1000[soln,3],2), np.round(formulation.reeval_1000[soln,4],2)]
                table_vals.append(row_vals)
                
        else:
            if formulation == 'baseline_100' or formulation == 'HydroInfo_100':
                solns = [formulation.compromise100_reeval]
            else:
                solns = [formulation.compromise500_reeval]
            for j, soln in enumerate(solns):
                row_vals = [np.round(formulation.reeval_100000[soln,0],1), int(np.round(formulation.reeval_100000[soln,1],0)), \
                            np.round(formulation.reeval_100000[soln,3],2), np.round(formulation.reeval_100000[soln,4],2)]
                table_vals.append(row_vals)
                
    # determine best and worst values for each objective
    mins = np.ones(4)*np.inf
    maxs = np.zeros(4)
    for i in range(len(rowNames)):
        for j in range(len(mins)):
            if table_vals[i][j] < mins[j]:
                mins[j] = table_vals[i][j]
            if table_vals[i][j] > maxs[j]:
                maxs[j] = table_vals[i][j]
    
    # determine color of cell
    negate = [True, False, False, False]
    cmap = matplotlib.cm.get_cmap('coolwarm_r')
    sm = matplotlib.cm.ScalarMappable(cmap=cmap)
    sm.set_array([0,1])
    cellColors = []
    for i in range(len(rowNames)):
        rowColors = []
        for j in range(len(colNames)):
            normValue = (table_vals[i][j] - mins[j])/(maxs[j] - mins[j])
            if negate[j] == True:
                rowColors.append(cmap(normValue))
            else:
                rowColors.append(cmap(1.0-normValue))
            
        cellColors.append(rowColors)
    
    return table_vals, cellColors, sm

makeFigure4_ParallelAxes(opt=True)
makeFigure4_ParallelAxes(opt=False)