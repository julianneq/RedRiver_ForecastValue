import numpy as np
import pandas as pd

class Formulation():
    def __init__(self):
        self.name = None
        self.opt100 = None
        self.reeval100 = None
        self.opt500 = None
        self.reeval500 = None
        
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    if name == 'baseline_100' or name == 'HydroInfo_100':
        formulation.opt100 = pd.read_csv('./100yr_refs/optimization/' + name + '.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood100"])
        formulation.opt500 = pd.read_csv('./500yr_refs/optimization/' + name + '_500yr.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood500"])
    elif name == 'baseline_500' or name == 'HydroInfo_500':
        formulation.opt100 = pd.read_csv('./100yr_refs/optimization/' + name + '_100yr.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood100"])
        formulation.opt500 = pd.read_csv('./500yr_refs/optimization/' + name + '.reference',
                                            delimiter=' ', header=None, 
                                            names=["Hydro","Deficit","Flood500"])
        
    formulation.reeval100 = pd.read_csv('./100yr_refs/reevaluation/' + name + '_re-eval_100yr.reference',
                                        delimiter=' ', header=None, 
                                        names=["Hydro","Deficit","Flood100"])
    formulation.reeval500 = pd.read_csv('./500yr_refs/reevaluation/' + name + '_re-eval_500yr.reference',
                                        delimiter=' ', header=None, 
                                        names=["Hydro","Deficit","Flood500"])
    
    return formulation

baseline_100 = getFormulations('baseline_100')
HydroInfo_100 = getFormulations('HydroInfo_100')
baseline_500 = getFormulations('baseline_500')
HydroInfo_500 = getFormulations('HydroInfo_500')
formulations = [baseline_100, HydroInfo_100, baseline_500, HydroInfo_500]

RefSet100_opt = pd.read_csv("./100yr_refs/optimization/overall_100yr.reference", delimiter=' ',
                            header=None, names=["Hydro","Deficit","Flood100"])
RefSet500_opt = pd.read_csv("./500yr_refs/optimization/overall_500yr.reference", delimiter=' ',
                            header=None, names=["Hydro","Deficit","Flood500"])
RefSet100_reeval = pd.read_csv("./100yr_refs/reevaluation/overall_re-eval_100yr.reference", 
                               delimiter=' ', header=None, names=["Hydro","Deficit","Flood100"])
RefSet500_reeval = pd.read_csv("./500yr_refs/reevaluation/overall_re-eval_500yr.reference", 
                               delimiter=' ', header=None, names=["Hydro","Deficit","Flood500"])

RefSets = [RefSet100_opt, RefSet500_opt, RefSet100_reeval, RefSet500_reeval]

for i in range(len(RefSets)):
    df = RefSets[i]
    df['Formulation'] = ""
    for formulation in formulations:
        if RefSets[i].equals(RefSet100_opt):
            df = pd.merge(df, formulation.opt100, on=["Hydro","Deficit","Flood100"], how='left',
                      indicator='Exist')
        elif RefSets[i].equals(RefSet100_reeval):
            df = pd.merge(df, formulation.reeval100, on=["Hydro","Deficit","Flood100"], how='left',
                      indicator='Exist')
        elif RefSets[i].equals(RefSet500_opt):
            df = pd.merge(df, formulation.opt500, on=["Hydro","Deficit","Flood500"], how='left',
                      indicator='Exist')
        else:
            df = pd.merge(df, formulation.reeval500, on=["Hydro","Deficit","Flood500"], how='left',
                      indicator='Exist')
            
        df['Formulation'].iloc[np.where(df.Exist=='both')[0]] = formulation.name
        df = df.drop(columns=['Exist'])
        
    df = df.drop(df.index[-1])
    RefSets[i] = df
    
setNames = ['opt100_contribution', 'opt500_contribution', 'reeval100_contribution', 
            'reeval500_contribution']
paths = ["./100yr_refs/optimization/", "./500yr_refs/optimization/", "./100yr_refs/reevaluation/",
         "./500yr_refs/reevaluation/"]
for i, RefSet in enumerate(RefSets):
    RefSet.to_csv(paths[i] + setNames[i] + ".csv")