#/bin/bash

# find reference set of each formulation on its own objectives in optimization
python pareto.py ./baseline_100/sets/baseline_100*.set -o 134-136 -e 0.5 25.0 0.05 --output baseline_100.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 135-137 baseline_100.resultfile >> baseline_100.reference
cut -d ' ' -f 1-134 baseline_100.resultfile >> baseline_100.vars
cp baseline_100.reference ./100yr_refs/optimization/baseline_100.reference

python pareto.py ./baseline_500/sets/baseline_500*.set -o 134-136 -e 0.5 25.0 0.05 --output baseline_500.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 135-137 baseline_500.resultfile >> baseline_500.reference
cut -d ' ' -f 1-134 baseline_500.resultfile >> baseline_500.vars
cp baseline_500.reference ./500yr_refs/optimization/baseline_500.reference

python pareto.py ./HydroInfo_100/sets/HydroInfo_100*.set -o 170-172 -e 0.5 25.0 0.05 --output HydroInfo_100.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 171-173 HydroInfo_100.resultfile >> HydroInfo_100.reference
cut -d ' ' -f 1-170 HydroInfo_100.resultfile >> HydroInfo_100.vars
cp HydroInfo_100.reference ./100yr_refs/optimization/HydroInfo_100.reference

python pareto.py ./HydroInfo_500/sets/HydroInfo_500*.set -o 170-172 -e 0.5 25.0 0.05 --output HydroInfo_500.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 171-173 HydroInfo_500.resultfile >> HydroInfo_500.reference
cut -d ' ' -f 1-170 HydroInfo_500.resultfile >> HydroInfo_500.vars
cp HydroInfo_500.reference ./100yr_refs/optimization/HydroInfo_500.reference


# find reference set of baseline 100 solutions on other formulations
# 500-yr flood optimization flows
python pareto.py ./baseline_100/baseline_100_re-eval_1x1000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/optimization/baseline_100_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/optimization/baseline_100_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/optimization/baseline_100_500yr.reference

# 100-yr flood re-evaluation flows
python pareto.py ./baseline_100/baseline_100_re-eval_1x100000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/reevaluation/baseline_100_re-eval_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/reevaluation/baseline_100_re-eval_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/reevaluation/baseline_100_re-eval_100yr.reference

# 500-yr flood re-evaluation flows
python pareto.py ./baseline_100/baseline_100_re-eval_1x100000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/reevaluation/baseline_100_re-eval_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/reevaluation/baseline_100_re-eval_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/reevaluation/baseline_100_re-eval_500yr.reference


# find reference set of baseline 500 solutions on other formulations
# 100-yr flood optimization flows
python pareto.py ./baseline_500/baseline_500_re-eval_1x1000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/optimization/baseline_500_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/optimization/baseline_500_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/optimization/baseline_500_100yr.reference

# 100-yr flood re-evaluation flows
python pareto.py ./baseline_500/baseline_500_re-eval_1x100000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/reevaluation/baseline_500_re-eval_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/reevaluation/baseline_500_re-eval_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/reevaluation/baseline_500_re-eval_100yr.reference

# 500-yr flood re-evaluation flows
python pareto.py ./baseline_500/baseline_500_re-eval_1x100000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/reevaluation/baseline_500_re-eval_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/reevaluation/baseline_500_re-eval_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/reevaluation/baseline_500_re-eval_500yr.reference


# find reference set of Hydro Info 100 solutions on other formulations
# 500-yr flood optimization flows
python pareto.py ./HydroInfo_100/HydroInfo_100_re-eval_1x1000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/optimization/HydroInfo_100_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/optimization/HydroInfo_100_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/optimization/HydroInfo_100_500yr.reference

# 100-yr flood re-evaluation flows
python pareto.py ./HydroInfo_100/HydroInfo_100_re-eval_1x100000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/reevaluation/HydroInfo_100_re-eval_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/reevaluation/HydroInfo_100_re-eval_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/reevaluation/HydroInfo_100_re-eval_100yr.reference

# 500-yr flood re-evaluation flows
python pareto.py ./HydroInfo_100/HydroInfo_100_re-eval_1x100000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/reevaluation/HydroInfo_100_re-eval_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/reevaluation/HydroInfo_100_re-eval_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/reevaluation/HydroInfo_100_re-eval_500yr.reference


# find reference set of Hydro Info 500 solutions on other formulations
# 100-yr flood optimization flows
python pareto.py ./HydroInfo_500/HydroInfo_500_re-eval_1x1000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/optimization/HydroInfo_500_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/optimization/HydroInfo_500_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/optimization/HydroInfo_500_100yr.reference

# 100-yr flood re-evaluation flows
python pareto.py ./HydroInfo_500/HydroInfo_500_re-eval_1x100000.obj -o 0 1 3 -e 0.5 25.0 0.05 \
--output ./100yr_refs/reevaluation/HydroInfo_500_re-eval_100yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,4 ./100yr_refs/reevaluation/HydroInfo_500_re-eval_100yr.reference >> temp.reference
mv temp.reference ./100yr_refs/reevaluation/HydroInfo_500_re-eval_100yr.reference

# 500-yr flood re-evaluation flows
python pareto.py ./HydroInfo_500/HydroInfo_500_re-eval_1x100000.obj -o 0 1 4 -e 0.5 25.0 0.05 \
--output ./500yr_refs/reevaluation/HydroInfo_500_re-eval_500yr.reference --delimiter=" " --comment="#"
cut -d ' ' -f 1,2,5 ./500yr_refs/reevaluation/HydroInfo_500_re-eval_500yr.reference >> temp.reference
mv temp.reference ./500yr_refs/reevaluation/HydroInfo_500_re-eval_500yr.reference