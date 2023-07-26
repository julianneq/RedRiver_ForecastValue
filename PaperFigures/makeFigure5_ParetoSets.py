import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from utils import getFormulations, getExtremePoints

# see https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
def func(pct,sizes):
    absolute = int(np.round(pct/100.*np.sum(sizes)))
    if absolute !=0:
        return "{:d}".format(absolute)

def compareParetoReevals2D(baseline_100, HydroInfo_100, baseline_500, HydroInfo_500, 
                           idealPoint, worstPoint, RefSets, figname):
    # indices of re-evaluation objectives to plot
    # order is Jhydro_WP1, Jdef2_WP1, JmaxDef_WP1, Jflood_100, Jflood_500
    indices = [[0,1,3],[0,1,4]]
    xlims = [[-0.1,3.5],[-0.1,6]]
    ylims = [29,47]
    ylabel = r'$J_{Hydro}$ (Gwh/day)'
    title = r'$J_{Deficit^2}$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$'
    colors = ['#ff7f00','#4daf4a','#377eb8','#984ea3']
    formulations = ['Baseline 100', 'Forecast 100', 'Baseline 500', 'Forecast 500']
    
    sns.set_style('darkgrid')
    fig = plt.figure()
    for i in range(2):
        for j in range(2):
            if j == 0:
                HVs = [[baseline_100.HV100, HydroInfo_100.HV100, baseline_500.HV100, HydroInfo_500.HV100],\
                       [baseline_100.HV500, HydroInfo_100.HV500, baseline_500.HV500, HydroInfo_500.HV500]]
                BL100 = baseline_100.reeval_1000[:,indices[i]]
                HI100 = HydroInfo_100.reeval_1000[:,indices[i]]
                BL500 = baseline_500.reeval_1000[:,indices[i]]
                HI500 = HydroInfo_500.reeval_1000[:,indices[i]]
            else:
                HVs = [[baseline_100.HV100_reeval, HydroInfo_100.HV100_reeval, 
                        baseline_500.HV100_reeval, HydroInfo_500.HV100_reeval],
                       [baseline_100.HV500_reeval, HydroInfo_100.HV500_reeval,
                        baseline_500.HV500_reeval, HydroInfo_500.HV500_reeval]]
                BL100 = baseline_100.reeval_100000[:,indices[i]]
                HI100 = HydroInfo_100.reeval_100000[:,indices[i]]
                BL500 = baseline_500.reeval_100000[:,indices[i]]
                HI500 = HydroInfo_500.reeval_100000[:,indices[i]]
            
            #2-D Figure multi color
            ax = plt.subplot2grid((4,5), (2*i+j,0), colspan=2)
            
            ptsBL100 = ax.scatter(BL100[:,2], BL100[:,0], s=200*BL100[:,1]/worstPoint[1], 
                                  color = '#ff7f00', alpha=0.3)
            ptsHI100 = ax.scatter(HI100[:,2], HI100[:,0], s=200*HI100[:,1]/worstPoint[1], 
                                  color = '#4daf4a', alpha=0.3)
            ptsBL500 = ax.scatter(BL500[:,2], BL500[:,0], s=200*BL500[:,1]/worstPoint[1], 
                                  color = '#377eb8', alpha=0.3)
            ptsHI500 = ax.scatter(HI500[:,2], HI500[:,0], s=200*HI500[:,1]/worstPoint[1], 
                                  color = '#984ea3', alpha=0.3)
            
            if i == 0:
                FloodObj = 'Flood100'
                ptIdeal = ax.scatter(idealPoint[3], idealPoint[0], color = 'k', marker='*', s=500)
                ax.set_xlabel(r'$J_{Flood,100}$ (m above 11.25 m)', fontsize=16)
            else:
                FloodObj = 'Flood500'
                ptIdeal = ax.scatter(idealPoint[4], idealPoint[0], color = 'k', marker='*', s=500)
                ax.set_xlabel(r'$J_{Flood,500}$ (m above 11.25 m)', fontsize=16)
                
            # put the solutions in the reference set in full transparency
            ax.scatter(RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_100')[0]][FloodObj],
                       -RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_100')[0]]['Hydro'],
                       s = 200*RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_100')[0]]['Deficit']/
                       worstPoint[1], color = colors[0])
            ax.scatter(RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_100')[0]][FloodObj],
                       -RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_100')[0]]['Hydro'],
                       s = 200*RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_100')[0]]['Deficit']/
                       worstPoint[1], color = colors[1])
            ax.scatter(RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_500')[0]][FloodObj],
                       -RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_500')[0]]['Hydro'],
                       s = 200*RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='baseline_500')[0]]['Deficit']/
                       worstPoint[1], color = colors[2])
            ax.scatter(RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_500')[0]][FloodObj],
                       -RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_500')[0]]['Hydro'],
                       s = 200*RefSets[2*i+j].iloc[np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_500')[0]]['Deficit']/
                       worstPoint[1], color = colors[3])
                  
            l1 = ax.scatter([],[], s=200*idealPoint[1]/worstPoint[1], color='k')
            l2 = ax.scatter([],[], s=200, color='k')
            
            ax.set_xlim(xlims[i])
            ax.set_ylim(ylims)
            ax.set_ylabel(ylabel, fontsize=16)
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=14)
                
            dikeLine, = ax.plot([2.15,2.15], ylims, c='k', linewidth=2)
            legend1 = ax.legend([l1, l2], [str(round(idealPoint[1],1)), str(round(worstPoint[1],1))], \
                scatterpoints=1, title=title, fontsize=14, loc='upper right', frameon=False)
            plt.setp(legend1.get_title(),fontsize=14)
            
            # inset pie chart of percent contribution of each formulation to reference set
            ax = plt.subplot2grid((4,5), (2*i+j,2))
            sizes = [len(np.where(RefSets[2*i+j]['Formulation']=='baseline_100')[0]),
                     len(np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_100')[0]),
                     len(np.where(RefSets[2*i+j]['Formulation']=='baseline_500')[0]),
                     len(np.where(RefSets[2*i+j]['Formulation']=='HydroInfo_500')[0])]
            print(sizes)
            patches, texts, autotexts = ax.pie(sizes, colors=colors, shadow=False, startangle=90, counterclock=False,
                                    autopct=lambda pct: func(pct,sizes), textprops=dict(color="k"))
            plt.setp(autotexts, size=14)
            if i == 0 and j == 0:
                ax.set_title('Reference Set\nContribution', fontsize=16)
            
            # Hypervolume
            ax = plt.subplot2grid((4,5), (2*i+j,3), colspan=2)
            ax.bar(range(4), HVs[i], color=colors)
            ax.set_xticks(range(4))
            ax.set_ylim([0,1])
            ax.set_xticklabels(formulations, fontsize=16)
            ax.set_ylabel('Hypervolume',fontsize=16)
            ax.tick_params(axis='both',labelsize=14)
            rects = ax.patches
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2, height+0.01, str(np.round(height,2)),
                                ha='center',va='bottom',fontsize=14)
                
    # Put a legend below current axis
    fig.subplots_adjust(bottom=0.15,hspace=0.5)
    legend2 = fig.legend([ptsBL100, ptsHI100, ptsBL500, ptsHI500, dikeLine, ptIdeal],\
                         ['Baseline 100','Forecast 100','Baseline 500','Forecast 500','Dike Height','Ideal Point'],\
                         scatterpoints=1, loc= 'lower center', ncol=6, frameon=True, fontsize=14)
    
    fig.set_size_inches([18,15])
    plt.savefig(figname)
    plt.clf()

    return None

baseline_100 = getFormulations('baseline_100')
HydroInfo_100 = getFormulations('HydroInfo_100')
baseline_500 = getFormulations('baseline_500')
HydroInfo_500 = getFormulations('HydroInfo_500')

RefSet_opt100 = pd.read_csv("../100yr_refs/optimization/opt100_contribution.csv")
RefSet_reeval100 = pd.read_csv("../100yr_refs/reevaluation/reeval100_contribution.csv")
RefSet_opt500 = pd.read_csv("../500yr_refs/optimization/opt500_contribution.csv")
RefSet_reeval500 = pd.read_csv("../500yr_refs/reevaluation/reeval500_contribution.csv")
RefSets = [RefSet_opt100, RefSet_reeval100, RefSet_opt500, RefSet_reeval500]

idealPoint, worstPoint = getExtremePoints(baseline_100, HydroInfo_100, baseline_500, HydroInfo_500)

compareParetoReevals2D(baseline_100, HydroInfo_100, baseline_500, HydroInfo_500, 
                       idealPoint, worstPoint, RefSets, 'ParetoSets.pdf')
