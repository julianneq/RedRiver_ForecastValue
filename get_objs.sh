#!/bin/bash
NSEEDS=10
NISLANDS=1
SEEDS=$(seq 1 ${NSEEDS})
ISLANDS=$(seq 0 ${NISLANDS})

for SEED in ${SEEDS}
do
	for ISLAND in ${ISLANDS}
	do
	awk 'BEGIN {FS=" "}; /^#/ {print $0}; /^[^#/]/ {printf("%s %s %s\n",$135,$136,$137)}' ./baseline_100/runtime/baseline_100_S${SEED}_M${ISLAND}.runtime \
	>./baseline_100/objs/runtime/baseline_100_S${SEED}_M${ISLAND}.obj
	awk 'BEGIN {FS=" "}; /^#/ {print $0}; /^[^#/]/ {printf("%s %s %s\n",$135,$136,$137)}' ./baseline_500/runtime/baseline_500_S${SEED}_M${ISLAND}.runtime \
	>./baseline_500/objs/runtime/baseline_500_S${SEED}_M${ISLAND}.obj
	awk 'BEGIN {FS=" "}; /^#/ {print $0}; /^[^#/]/ {printf("%s %s %s\n",$171,$172,$173)}' ./HydroInfo_100/runtime/HydroInfo_100_S${SEED}_M${ISLAND}.runtime \
	>./HydroInfo_100/objs/runtime/HydroInfo_100_S${SEED}_M${ISLAND}.obj
	awk 'BEGIN {FS=" "}; /^#/ {print $0}; /^[^#/]/ {printf("%s %s %s\n",$171,$172,$173)}' ./HydroInfo_500/runtime/HydroInfo_500_S${SEED}_M${ISLAND}.runtime \
	>./HydroInfo_500/objs/runtime/HydroInfo_500_S${SEED}_M${ISLAND}.obj
	done
done