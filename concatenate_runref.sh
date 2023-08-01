#!/bin/bash
NSEEDS=10
NSTEPS=99
SEEDS=$(seq 1 ${NSEEDS})
STEPS=$(seq 0 ${NSTEPS})
FORMULATIONS=(baseline_100 baseline_500 HydroInfo_100 HydroInfo_500)

for FORMULATION in ${FORMULATIONS[@]}
	do
	for STEP in ${STEPS}
		do
		for SEED in ${SEEDS}
			do
			echo "#" >> ./${FORMULATION}/objs/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runref 
			cat ./${FORMULATION}/objs/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runref 
			cat ./${FORMULATION}/objs/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runref >> ./${FORMULATION}/objs/runtime/reference/${FORMULATION}_S${SEED}.runref

			echo "#" >> ./${FORMULATION}/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runset 
			cat ./${FORMULATION}/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runset
			cat ./${FORMULATION}/runtime/reference/${FORMULATION}_S${SEED}_step${STEP}.runset >> ./${FORMULATION}/runtime/reference/${FORMULATION}_S${SEED}.runset
			done
		done
	done