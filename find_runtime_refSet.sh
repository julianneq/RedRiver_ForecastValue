#/bin/bash\
NSEEDS=10
NISLANDS=1
NSTEPS=99
SEEDS=$(seq 1 ${NSEEDS})
ISLANDS=$(seq 0 ${NISLANDS})
STEPS=$(seq 0 ${NSTEPS})

for SEED in ${SEEDS}
do
	for STEP in ${STEPS}
	do
		python pareto.py ./baseline_100/objs/runtime/baseline_100_S${SEED}_M*/*_step${STEP}.obj -o 0-2 -e 0.5 25.0 0.05 \
		--output ./baseline_100/objs/runtime/reference/baseline_100_S${SEED}_step${STEP}.runref --delimiter=" " --comment="#" --blank
		python pareto.py ./baseline_100/runtime/baseline_100_S${SEED}_M*/*_step${STEP}.set -o 134-136 -e 0.5 25.0 0.05 \
		--output ./baseline_100/runtime/reference/baseline_100_S${SEED}_step${STEP}.runset --delimiter=" " -c "#" "//" --blank

		python pareto.py ./baseline_500/objs/runtime/baseline_500_S${SEED}_M*/*_step${STEP}.obj -o 0-2 -e 0.5 25.0 0.05 \
		--output ./baseline_500/objs/runtime/reference/baseline_500_S${SEED}_step${STEP}.runref --delimiter=" " --comment="#" --blank
		python pareto.py ./baseline_500/runtime/baseline_500_S${SEED}_M*/*_step${STEP}.set -o 134-136 -e 0.5 25.0 0.05 \
		--output ./baseline_500/runtime/reference/baseline_500_S${SEED}_step${STEP}.runset --delimiter=" " -c "#" "//" --blank

		python pareto.py ./HydroInfo_100/objs/runtime/HydroInfo_100_S${SEED}_M*/*_step${STEP}.obj -o 0-2 -e 0.5 25.0 0.05 \
		--output ./HydroInfo_100/objs/runtime/reference/HydroInfo_100_S${SEED}_step${STEP}.runref --delimiter=" " --comment="#" --blank
		python pareto.py ./HydroInfo_100/runtime/HydroInfo_100_S${SEED}_M*/*_step${STEP}.set -o 170-172 -e 0.5 25.0 0.05 \
		--output ./HydroInfo_100/runtime/reference/HydroInfo_100_S${SEED}_step${STEP}.runset --delimiter=" " -c "#" "//" --blank

		python pareto.py ./HydroInfo_500/objs/runtime/HydroInfo_500_S${SEED}_M*/*_step${STEP}.obj -o 0-2 -e 0.5 25.0 0.05 \
		--output ./HydroInfo_500/objs/runtime/reference/HydroInfo_500_S${SEED}_step${STEP}.runref --delimiter=" " --comment="#" --blank
		python pareto.py ./HydroInfo_500/runtime/HydroInfo_500_S${SEED}_M*/*_step${STEP}.set -o 170-172 -e 0.5 25.0 0.05 \
		--output ./HydroInfo_500/runtime/reference/HydroInfo_500_S${SEED}_step${STEP}.runset --delimiter=" " -c "#" "//" --blank
	done
done