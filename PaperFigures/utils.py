import numpy as np
import pandas as pd

class Formulation():
    def __init__(self):
        self.name = None
        self.reference = None
        self.reeval_1000 = None
        self.reeval_100000 = None
        self.HV100 = None
        self.HV500 = None
        self.HV100_reeval = None
        self.HV500_reeval = None
        self.bestFlood100_opt = None
        self.bestFlood500_opt = None
        self.bestHydro_opt = None
        self.bestDeficit_opt = None
        self.compromise100_opt = None
        self.compromise500_opt = None
        self.bestFlood100_reeval = None
        self.bestFlood500_reeval = None
        self.bestHydro_reeval = None
        self.bestDeficit_reeval = None
        self.compromise100_reeval = None
        self.compromise500_reeval = None

class Soln():
    def __init__(self):
        self.solnNo = None
        self.allObjs = None
        self.allInputs = None
        self.allOutputs = None
        self.Flood100Yr = None
        self.Flood500Yr = None
        self.DeficitYr = None
        self.HydroYr = None
        self.rSL_SI = None
        self.rHB_SI = None
        self.rTQ_SI = None
        self.rTB_SI = None

def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    formulation.reference = np.loadtxt('../' + name + '/' + name +  '.reference')
    formulation.reeval_1000 = np.loadtxt('../' + name + '/' + name +  '_re-eval_1x1000.obj')
    formulation.reeval_100000 = np.loadtxt('../' + name + '/' + name +  '_re-eval_1x100000.obj')
    
    if name == 'HydroInfo_500' or name == 'baseline_500':
        formulation.reeval_1000[:,[0,1,4]] = formulation.reference
    else:
        formulation.reeval_1000[:,[0,1,3]] = formulation.reference
    
    if name == 'baseline_100' or name == 'HydroInfo_100':
        formulation.HV100 = np.loadtxt('../100yr_refs/optimization/metrics/' + name + 
                                       '.metrics',skiprows=1,usecols=[0]) 
        formulation.HV500 = np.loadtxt('../500yr_refs/optimization/metrics/' + name + 
                                       '_500yr.metrics',skiprows=1,usecols=[0])
    else:
        formulation.HV100 = np.loadtxt('../100yr_refs/optimization/metrics/' + name + 
                                       '_100yr.metrics',skiprows=1,usecols=[0])
        formulation.HV500 = np.loadtxt('../500yr_refs/optimization/metrics/' + name + 
                                       '.metrics',skiprows=1,usecols=[0])
    
    formulation.HV100_reeval = np.loadtxt('../100yr_refs/reevaluation/metrics/' + name + 
                                          '_re-eval_100yr.metrics',skiprows=1,usecols=[0])
    formulation.HV500_reeval = np.loadtxt('../500yr_refs/reevaluation/metrics/' + name + 
                                          '_re-eval_500yr.metrics',skiprows=1,usecols=[0])
    
    formulation.bestHydro_opt = np.argmin(formulation.reeval_1000[:,0])
    formulation.bestHydro_reeval = np.argmin(formulation.reeval_100000[:,0])
    formulation.bestDeficit_opt = np.argmin(formulation.reeval_1000[:,1])
    formulation.bestDeficit_reeval = np.argmin(formulation.reeval_100000[:,1])
    # if there is a tie for the lowest 100-yr flood, pick the one with the lowest 500-yr flood
    lowest100indices_opt = np.where(formulation.reeval_1000[:,3] == np.min(formulation.reeval_1000[:,3]))[0]
    if len(lowest100indices_opt) > 0:
        formulation.bestFlood100_opt = lowest100indices_opt[np.argmin(formulation.reeval_1000[lowest100indices_opt,4])]
    else:
        formulation.bestFlood100_opt = np.argmin(formulation.reeval_1000[:,3])
        
    # repeat for reevaluation
    lowest100indices_reeval = np.where(formulation.reeval_100000[:,3] == np.min(formulation.reeval_100000[:,3]))[0]
    if len(lowest100indices_reeval) > 0:
        formulation.bestFlood100_reeval = lowest100indices_reeval[np.argmin(formulation.reeval_100000[lowest100indices_reeval,4])]
    else:
        formulation.bestFlood100_reeval = np.argmin(formulation.reeval_100000[:,3])

    formulation.bestFlood500_opt = np.argmin(formulation.reeval_1000[:,4])
    formulation.bestFlood500_reeval = np.argmin(formulation.reeval_100000[:,4])
    compIndex100_opt = findCompromise(formulation.reeval_1000[:,[0,1,3]],1)
    compIndex100_reeval = findCompromise(formulation.reeval_100000[:,[0,1,3]],1)
    
    satisfy500_opt = np.where(formulation.reeval_1000[:,4] < 2.15)[0]
    sample500_opt = formulation.reeval_1000[:,[0,1,4]]
    compIndex500_opt = satisfy500_opt[findCompromise(sample500_opt[satisfy500_opt,:],1)]
    formulation.compromise100_opt = compIndex100_opt
    formulation.compromise500_opt = compIndex500_opt
    
    satisfy500_reeval = np.where(formulation.reeval_100000[:,4] < 2.15)[0]
    sample500_reeval = formulation.reeval_100000[:,[0,1,4]]
    compIndex500_reeval = satisfy500_reeval[findCompromise(sample500_reeval[satisfy500_reeval,:],1)]
    formulation.compromise100_reeval = compIndex100_reeval
    formulation.compromise500_reeval = compIndex500_reeval
    
    # negate maximization objective (hydropower)
    formulation.reeval_1000[:,0] = -formulation.reeval_1000[:,0]
    formulation.reeval_100000[:,0] = -formulation.reeval_100000[:,0]
    
    if name == 'baseline_100' or name == 'HydroInfo_100':
        formulation.bestIndices_opt = [formulation.bestHydro_opt, formulation.bestDeficit_opt, 
                                       formulation.bestFlood100_opt, formulation.compromise100_opt]
        formulation.bestIndices_reeval = [formulation.bestHydro_reeval, formulation.bestDeficit_reeval, 
                                       formulation.bestFlood100_reeval, formulation.compromise100_reeval]
    else:
        formulation.bestIndices_opt = [formulation.bestHydro_opt, formulation.bestDeficit_opt, 
                                          formulation.bestFlood500_opt, formulation.compromise500_opt]
        formulation.bestIndices_reeval = [formulation.bestHydro_reeval, formulation.bestDeficit_reeval, 
                                          formulation.bestFlood500_reeval, formulation.compromise500_reeval]
    
    return formulation

def getExtremePoints(baseline_100, HydroInfo_100, baseline_500, HydroInfo_500):
    
    minPoint = np.zeros(5)
    for i in range(5):
        minPoint[i] = np.min([np.min(baseline_100.reeval_1000[:,i]),
                                np.min(baseline_100.reeval_100000[:,i]),
                                np.min(HydroInfo_100.reeval_1000[:,i]),
                                np.min(HydroInfo_100.reeval_100000[:,i]),
                                np.min(baseline_500.reeval_1000[:,i]),
                                np.min(baseline_500.reeval_100000[:,i]),
                                np.min(HydroInfo_500.reeval_1000[:,i]),
                                np.min(HydroInfo_500.reeval_100000[:,i])])
    
    maxPoint = np.zeros(5)
    for i in range(5):
        maxPoint[i] = np.max([np.max(baseline_100.reeval_1000[:,i]),
                                np.max(baseline_100.reeval_100000[:,i]),
                                np.max(HydroInfo_100.reeval_1000[:,i]),
                                np.max(HydroInfo_100.reeval_100000[:,i]),
                                np.max(baseline_500.reeval_1000[:,i]),
                                np.max(baseline_500.reeval_100000[:,i]),
                                np.max(HydroInfo_500.reeval_1000[:,i]),
                                np.max(HydroInfo_500.reeval_100000[:,i])])
        
    idealPoint = minPoint
    idealPoint[0] = maxPoint[0]
    
    worstPoint = maxPoint
    worstPoint[0] = minPoint[0]
    
    return idealPoint, worstPoint

def findCompromise(refSet, deficitIndex):
    # normalize objectives for calculation of compromise solution
    nobjs = np.shape(refSet)[1]
    normObjs = np.zeros([np.shape(refSet)[0],nobjs])
    for i in range(np.shape(refSet)[0]):
        for j in range(nobjs):
            # take the square root of the deficit so it's less skewed
            if j == deficitIndex:
                normObjs[i,j] = (np.sqrt(refSet[i,j])-np.mean(np.sqrt(refSet[:,j])))/np.std(np.sqrt(refSet[:,j]))
            else:
                normObjs[i,j] = (refSet[i,j]-np.mean(refSet[:,j]))/np.std(refSet[:,j])
    
    # find comprommise solution (solution closest to ideal point)
    dists = np.zeros(np.shape(refSet)[0])
    for i in range(len(dists)):
        for j in range(nobjs):
            dists[i] = dists[i] + (normObjs[i,j]-np.min(normObjs[:,j]))**2
            
    compromise = np.argmin(dists)
    
    return compromise

def getSolns_r(formulation, solnNo):
    inputNames = ['sSL','sHB','sTQ','sTB','HNfcst']
    outputNames = ['rSL','rHB','rTQ','rTB']
    objNames = ['Flood','SqDef','Hydro']

    soln = Soln()
    soln.solnNo = solnNo
    soln.name = formulation.name
    
    soln.allInputs = np.zeros([1000,365,5])
    soln.allOutputs = np.zeros([1000,365,4])
    soln.allObjs = np.zeros([1000,365,3])

    doy = np.array(np.concatenate((np.arange(121,366,1),np.arange(1,121,1)),0))
    for day in range(365):
        soln.allInputs[:,day,:] = pd.read_csv('../' + formulation.name + '/perturbations/Soln' + \
                      str(soln.solnNo+1) + '/r/Delta0.005/' + soln.name + '_Soln' \
                      + str(soln.solnNo+1) + '_day' + str(doy[day]) + '.txt', \
                      sep=' ', names=inputNames, usecols=[0,1,2,3,4])
        
        soln.allOutputs[:,day,:] = pd.read_csv('../' + formulation.name + '/perturbations/Soln' + \
                      str(soln.solnNo+1) + '/r/Delta0.005/' + soln.name + '_Soln' \
                      + str(soln.solnNo+1) + '_day' + str(doy[day]) + '.txt', \
                    sep=' ', names=outputNames, usecols=[5,6,7,8])
        
        soln.allObjs[:,day,:] = pd.read_csv('../' + formulation.name + '/perturbations/Soln' + \
                      str(soln.solnNo+1) + '/r/Delta0.005/' + soln.name + '_Soln' \
                      + str(soln.solnNo+1) + '_day' + str(doy[day]) + '.txt', \
                      sep=' ', names=objNames, usecols=[9,10,11])
        
    soln.Flood100Yr = np.argsort(np.max(soln.allObjs[:,:,0],1))[990]
    soln.Flood500Yr = np.argsort(np.max(soln.allObjs[:,:,0],1))[998]
    soln.DeficitYr = np.argsort(np.sum(soln.allObjs[:,:,1],1))[990]
    soln.HydroYr = np.argsort(np.sum(soln.allObjs[:,:,2],1))[990]
    
    soln.rSL_SI = np.loadtxt('../' + formulation.name + '/sensitivities/Soln' + str(soln.solnNo+1) + 
                             '/r/Delta0.005/' + formulation.name + '_rSL.txt', skiprows=1, delimiter=',')
    soln.rHB_SI = np.loadtxt('../' + formulation.name + '/sensitivities/Soln' + str(soln.solnNo+1) + 
                             '/r/Delta0.005/' + formulation.name + '_rHB.txt',
                             skiprows=1, delimiter=',')
    soln.rTQ_SI = np.loadtxt('../' + formulation.name + '/sensitivities/Soln' + str(soln.solnNo+1) + 
                             '/r/Delta0.005/' + formulation.name + '_rTQ.txt', skiprows=1, delimiter=',')
    soln.rTB_SI = np.loadtxt('../' + formulation.name + '/sensitivities/Soln' + str(soln.solnNo+1) + 
                             '/r/Delta0.005/' + formulation.name + '_rTB.txt', skiprows=1, delimiter=',')
    
    return soln
