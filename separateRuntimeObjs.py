import os

maindir = os.getcwd()
formulations = ['baseline_100','baseline_500','HydroInfo_100','HydroInfo_500']
for formulation in formulations:
	runtimeObjsList = [f for f in os.listdir(maindir + "/" + formulation + "/objs/runtime") if f[-4::] == '.obj']
	for j in range(len(runtimeObjsList)):
	    os.chdir(maindir + "/" + formulation + "/objs/runtime")
	    with open(runtimeObjsList[j], mode="r") as bigfile:
	        reader = bigfile.read()
	        os.mkdir(maindir + "/" + formulation + "/objs/runtime/" + runtimeObjsList[j][:-4])
	        os.chdir(maindir + "/" + formulation + "/objs/runtime/" + runtimeObjsList[j][:-4])
	        for k,part in enumerate(reader.split("#")):
	            with open(runtimeObjsList[j][:-4] + "_step" + str(int(k)) + ".obj", mode="w") as newfile:
	                newfile.write(part + "#")