import os

maindir = os.getcwd()
formulations = ['baseline_100','baseline_500','HydroInfo_100','HydroInfo_500']
for formulation in formulations:
	runtimeObjsList = [f for f in os.listdir(maindir + "/" + formulation + "/runtime") if f[-8::] == '.runtime']
	for j in range(len(runtimeObjsList)):
	    os.chdir(maindir + "/" + formulation + "/runtime")
	    with open(runtimeObjsList[j], mode="r") as bigfile:
	        reader = bigfile.read()
	        os.mkdir(maindir + "/" + formulation + "/runtime/" + runtimeObjsList[j][:-8])
	        os.chdir(maindir + "/" + formulation + "/runtime/" + runtimeObjsList[j][:-8])
	        for k,part in enumerate(reader.split("#")):
	            with open(runtimeObjsList[j][:-8] + "_step" + str(int(k)) + ".set", mode="w") as newfile:
	                newfile.write(part + "#")