import numpy as np
import math

def separate_input_params(formulation, nprocs=None):
	inputParams  = np.loadtxt(formulation + '.vars')
	nrows = np.shape(inputParams)[0]
	ncols = np.shape(inputParams)[1]
	if nprocs == None:
		nprocs = nrows

	count = int(math.floor(nrows)/nprocs)
	remainder = nrows % nprocs

	for i in range(nprocs):
		if i < remainder:
			inputs_per_proc = np.zeros([count+1, ncols])
			for j in range(count+1):
				inputs_per_proc[j,:] = inputParams[i*(count+1)+j,:]
		else:
			inputs_per_proc = np.zeros([count, ncols])
			for j in range(count):
				inputs_per_proc[j,:] = inputParams[remainder*(count+1)+(i-remainder)*count+j,:]

		np.savetxt('./' + formulation + '/Solns/' + formulation + '_Soln' + str(i+1) + '.txt', inputs_per_proc, fmt = '%19.17f', delimiter=' ')

	return None

formulations = ['baseline_100','baseline_500','HydroInfo_100','HydroInfo_500']
for formulation in formulations:
	separate_input_params(formulation)