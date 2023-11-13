import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from utils import getFormulations, getSolns_r

sns.set_style("dark")

def makeSensitivityFigures(opt=True):
    # load formulations
    baseline_100 = getFormulations('baseline_100')
    baseline_500 = getFormulations('baseline_500')
    HydroInfo_100 = getFormulations('HydroInfo_100')
    HydroInfo_500 = getFormulations('HydroInfo_500')
    
    # load best solutions from each formulation
    if opt == True:
        BL100_Hydro = getSolns_r(baseline_100, baseline_100.bestHydro_opt)
        BL100_Deficit = getSolns_r(baseline_100, baseline_100.bestDeficit_opt)
        BL100_Flood100 = getSolns_r(baseline_100, baseline_100.bestFlood100_opt)
        BL100_Comp100 = getSolns_r(baseline_100, baseline_100.compromise100_opt)
    
        BL500_Hydro = getSolns_r(baseline_500, baseline_500.bestHydro_opt)
        BL500_Deficit = getSolns_r(baseline_500, baseline_500.bestDeficit_opt)
        BL500_Flood500 = getSolns_r(baseline_500, baseline_500.bestFlood500_opt)
        BL500_Comp500 = getSolns_r(baseline_500, baseline_500.compromise500_opt)
    
        HI100_Hydro = getSolns_r(HydroInfo_100 , HydroInfo_100.bestHydro_opt)
        HI100_Deficit = getSolns_r(HydroInfo_100 , HydroInfo_100.bestDeficit_opt)
        HI100_Flood100 = getSolns_r(HydroInfo_100 , HydroInfo_100.bestFlood100_opt)
        HI100_Comp100 = getSolns_r(HydroInfo_100 , HydroInfo_100.compromise100_opt)
        
        HI500_Hydro = getSolns_r(HydroInfo_500 , HydroInfo_500.bestHydro_opt)
        HI500_Deficit = getSolns_r(HydroInfo_500 , HydroInfo_500.bestDeficit_opt)
        HI500_Flood500 = getSolns_r(HydroInfo_500 , HydroInfo_500.bestFlood500_opt)
        HI500_Comp500 = getSolns_r(HydroInfo_500 , HydroInfo_500.compromise500_opt)
    else:
        BL100_Hydro = getSolns_r(baseline_100, baseline_100.bestHydro_reeval)
        BL100_Deficit = getSolns_r(baseline_100, baseline_100.bestDeficit_reeval)
        BL100_Flood100 = getSolns_r(baseline_100, baseline_100.bestFlood100_reeval)
        BL100_Comp100 = getSolns_r(baseline_100, baseline_100.compromise100_reeval)
    
        BL500_Hydro = getSolns_r(baseline_500, baseline_500.bestHydro_reeval)
        BL500_Deficit = getSolns_r(baseline_500, baseline_500.bestDeficit_reeval)
        BL500_Flood500 = getSolns_r(baseline_500, baseline_500.bestFlood500_reeval)
        BL500_Comp500 = getSolns_r(baseline_500, baseline_500.compromise500_reeval)
    
        HI100_Hydro = getSolns_r(HydroInfo_100 , HydroInfo_100.bestHydro_reeval)
        HI100_Deficit = getSolns_r(HydroInfo_100 , HydroInfo_100.bestDeficit_reeval)
        HI100_Flood100 = getSolns_r(HydroInfo_100 , HydroInfo_100.bestFlood100_reeval)
        HI100_Comp100 = getSolns_r(HydroInfo_100 , HydroInfo_100.compromise100_reeval)
        
        HI500_Hydro = getSolns_r(HydroInfo_500 , HydroInfo_500.bestHydro_reeval)
        HI500_Deficit = getSolns_r(HydroInfo_500 , HydroInfo_500.bestDeficit_reeval)
        HI500_Flood500 = getSolns_r(HydroInfo_500 , HydroInfo_500.bestFlood500_reeval)
        HI500_Comp500 = getSolns_r(HydroInfo_500 , HydroInfo_500.compromise500_reeval)
    
    # create vectors of solutions to be plotted in each figure
    solns = [[BL100_Flood100, HI100_Flood100, BL500_Flood500, HI500_Flood500],
            [BL100_Hydro, HI100_Hydro, BL500_Hydro, HI500_Hydro],
            [BL100_Deficit, HI100_Deficit, BL500_Deficit, HI500_Deficit],
            [BL100_Comp100, HI100_Comp100, BL500_Comp500, HI500_Comp500]]
    
    # plotting features
    inputs = ['sSL','sHB','sTQ','sTB','HNfcst']
    outputs = [r'$r_{t+1}^{SL}$' + ' Sensitivity',r'$r_{t+1}^{HB}$' + ' Sensitivity',\
    r'$r_{t+1}^{TB}$' + ' Sensitivity',r'$r_{t+1}^{TQ}$' + ' Sensitivity', 'State Trajectories']
    colors = ['#fb9a99','#e31a1c','#33a02c','#6a3d9a','#1f78b4','#ff7f00']
    pSL = plt.Rectangle((0,0), 1, 1, fc=colors[0], edgecolor='none')
    pHB = plt.Rectangle((0,0), 1, 1, fc=colors[1], edgecolor='none')
    pTQ = plt.Rectangle((0,0), 1, 1, fc=colors[2], edgecolor='none')
    pTB = plt.Rectangle((0,0), 1, 1, fc=colors[3], edgecolor='none')
    pHNfcst = plt.Rectangle((0,0), 1, 1, fc=colors[4], edgecolor='none')
    pInteract = plt.Rectangle((0,0), 1, 1, fc=colors[5], edgecolor='none')
    titles = [['Baseline 100\nFlood 100 Policy','Forecast 100\nFlood 100 Policy',
                'Baseline 500\nFlood 500 Policy','Forecast 500\nFlood 500 Policy'],
                ['Baseline 100\nHydro Policy','Forecast 100\nHydro Policy',
                'Baseline 500\nHydro Policy','Forecast 500\nHydro Policy'],
                ['Baseline 100\nDeficit Policy','Forecast 100\nDeficit Policy',
                'Baseline 500\nDeficit Policy','Forecast 500\nDeficit Policy'],
                ['Baseline 100\nCompromise 100\nPolicy','Forecast 100\nCompromise 100\nPolicy',
                'Baseline 500\nCompromise 500\nPolicy','Forecast 500\nCompromise 500\nPolicy']]
    suptitles = ['','Year of 100-yr Flood', 'Year of 500-yr Flood', 'Year of WP1 Hydropower', 'Year of WP1 Squared Deficit']
    fignames = [['BestFloodPolicies_FloodYr.pdf','BestFloodPolicies_Flood100Yr.pdf','BestFloodPolicies_Flood500Yr.pdf',
                 'BestFloodPolicies_HydroYr.pdf','BestFloodPolicies_DeficitYr.pdf'],
                ['BestHydroPolicies_FloodYr.pdf','BestHydroPolicies_Flood100Yr.pdf','BestHydroPolicies_Flood500Yr.pdf',
                 'BestHydroPolicies_HydroYr.pdf','BestHydroPolicies_DeficitYr.pdf'],
                ['BestDeficitPolicies_FloodYr.pdf','BestDeficitPolicies_Flood100Yr.pdf','BestDeficitPolicies_Flood500Yr.pdf',
                 'BestDeficitPolicies_HydroYr.pdf','BestDeficitPolicies_DeficitYr.pdf'],
                ['CompromisePolicies_FloodYr.pdf','CompromisePolicies_Flood100Yr.pdf','CompromisePolicies_Flood500Yr.pdf',
                 'CompromisePolicies_HydroYr.pdf','CompromisePolicies_DeficitYr.pdf']]
    years = ['FloodYr','Flood100Yr','Flood500Yr','HydroYr','DeficitYr']
    
    # turn off display
    plt.switch_backend('agg')
    
    for m in range(len(solns)):
        for n in range(len(years)):
            fig = plt.figure()
            ymaxs = np.ones([len(outputs),len(solns[m])])
            ymins = np.zeros([len(outputs),len(solns[m])])
            for i in range(len(solns[m])):
                if years[n] == 'FloodYr':
                    if solns[m][i].name == 'baseline_100' or solns[m][i].name == 'HydroInfo_100':
                        year = solns[m][i].Flood100Yr
                    else:
                        year = solns[m][i].Flood500Yr
                elif years[n] == 'Flood100Yr':
                    year = solns[m][i].Flood100Yr
                elif years[n] == 'Flood500Yr':
                    year = solns[m][i].Flood500Yr
                elif years[n] == 'HydroYr':
                    year = solns[m][i].HydroYr
                else:
                    year = solns[m][i].DeficitYr

                # plot sensitivity indices of 4 reservoir releases in first 4 columns
                SIs = [solns[m][i].rSL_SI, solns[m][i].rHB_SI, solns[m][i].rTB_SI, solns[m][i].rTQ_SI]                
                for j in range(len(SIs)):
                    ax = fig.add_subplot(len(outputs),len(solns[m]),j*len(solns[m])+i+1)
                    y1 = np.zeros([365])
                    if solns[m][i].name == 'baseline_100' or solns[m][i].name == 'baseline_500':
                        K = len(inputs)-1
                    else:
                        K = len(inputs)
                    
                    for k in range(K): # 1st order SIs
                        y2 = np.zeros([365])
                        posIndices = np.where(np.sum(SIs[j][year*365:(year+1)*365,:],1)>0)[0]
                        y2[posIndices] = np.sum(SIs[j][year*365:(year+1)*365,0:(k+1)],1)[posIndices]/ \
                                np.sum(SIs[j][year*365:(year+1)*365,:],1)[posIndices]
                        ax.plot(range(0,365),y2,c='None')
                        ax.fill_between(range(0,365), y1, y2, where=y2>y1, color=colors[k])
                        ymaxs[j,i] = max(ymaxs[j,i],np.max(y2))
                        y1 = y2
                        
                    # attribute rest to interactions
                    y2 = np.ones([365])
                    ZeroIndices = np.where(y1==0)
                    y2[ZeroIndices] = 0
                    negIndices = np.where(np.sum(SIs[j][year*365:(year+1)*365,K::],1)<0)[0]
                    y2[negIndices] = np.sum(SIs[j][year*365:(year+1)*365,K::],1)[negIndices]/ \
                        np.sum(SIs[j][year*365:(year+1)*365,:],1)[negIndices]
                    ax.fill_between(range(0,365), y1, y2, where=y1<y2, color=colors[-1])
                    ax.fill_between(range(0,365), y2, 0, where=y1>y2, color=colors[-1])
                    ymaxs[j,i] = max(ymaxs[j,i], np.max(y2))
                    ymins[j,i] = min(ymins[j,i], np.min(y2))
                    
                    #if j != 0:
                    #    ax.tick_params(axis='y', labelleft='off')
                    #else:
                    if j == 0:
                        ax.set_title(titles[m][i], fontsize=16)
                        
                    ax.tick_params(axis='y', labelsize=14)
                    ax.tick_params(axis='x', labelbottom=False)
	                    
                    if i == 0:
                        ax.set_ylabel(outputs[j], fontsize=16)
                        
                    ax.set_xlim([0,364])
                    ax.set_ylim([ymins[j,i],ymaxs[j,i]])
                    
                # plot state trajectories in last row
                ax = fig.add_subplot(len(outputs),len(solns[m]),(j+1)*len(solns[m])+i+1)
                for k in range(len(inputs)-1):
                    ax.plot(range(0,365),solns[m][i].allInputs[year,:,k],c=colors[k],linewidth=2)
                
                ax.set_ylim([0,1E10])
                
                ax.set_xticks([15,45,75,106,137,167,198,229,259,289,319,350])
                ax.set_xticklabels(['M','J','J','A','S','O','N','D','J','F','M','A'],fontsize=14)
                
                if i == 0:
                    ax.set_ylabel('Storage (m' + r'$\mathregular{^3}\!)$', fontsize=16)
                    ax.tick_params(axis='y', labelsize=14, left=False)
                else:
                    ax.tick_params(axis='y', labelleft=False, left=False)
                
	            # plot HNfcst on twin axis of last column
                ax2 = ax.twinx()
                ax2.plot(range(0,365),solns[m][i].allInputs[year,:,k+1],c=colors[k+1],linewidth=2)
                dikeLine, = ax2.plot([0,364],[13.4,13.4],c='k',linewidth=2)
                ax2.tick_params(axis='x',labelbottom=False)
                ax2.set_ylim([0,16])
                ax2.set_xlim([0,364])
                
                if i == 3:
                    ax2.set_ylabel(r'$\tilde{z}_{t+2}^{HN}$' + ' (m)', fontsize=16)
                    ax2.tick_params(axis='y',labelsize=14,right=False)
                else:
                    ax2.tick_params(axis='y',labelright=False,labelleft=False,right=False,left=False)
                        
            fig.text(0.01, 0.625, 'Portion of Variance', va='center', rotation='vertical', fontsize=18)
            if suptitles[n] != '':
                fig.suptitle(suptitles[n], fontsize=18)
            else:
                fig.text()
            fig.subplots_adjust(bottom=0.15,hspace=0.3, wspace=0.3)
            plt.figlegend([pSL,pHB,pTB,pTQ,pHNfcst,pInteract,dikeLine],\
                          [r'$s_t^{SL}$',r'$s_t^{HB}$',r'$s_t^{TB}$',r'$s_t^{TQ}$',r'$\tilde{z}_{t+2}^{HN}$','Interactions','Dike Height'],\
                          loc='lower center', ncol=4, fontsize=16, frameon=True)
            fig.set_size_inches([10,12])
            fig.savefig(fignames[m][n])
            fig.clf()
            
    return None

makeSensitivityFigures()
