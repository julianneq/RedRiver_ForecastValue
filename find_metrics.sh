NSEEDS=10
NISLANDS=1

SEEDS=$(seq 1 ${NSEEDS})
ISLANDS=$(seq 0 ${NISLANDS})
JAVA_ARGS="-cp MOEAFramework-2.4-Demo.jar"

for FORMULATION in ${FORMULATIONS[@]}
    do
    for SEED in ${SEEDS}
        do
        for ISLAND in ${ISLANDS}
        	do
        	    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
            	-d 3 -i ./baseline_100/sets/baseline_100_S${SEED}.set -r overall_100.reference -o ./baseline_100/metrics/baseline_100_S${SEED}.metrics

        	    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
            	-d 3 -i ./baseline_500/sets/baseline_500_S${SEED}.set -r overall_500.reference -o ./baseline_500/metrics/baseline_500_S${SEED}.metrics

            	java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
            	-d 3 -i ./HydroInfo_100/sets/HydroInfo_100_S${SEED}.set -r overall_100.reference -o ./HydroInfo_100/metrics/HydroInfo_100_S${SEED}.metrics

        	    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
            	-d 3 -i ./HydroInfo_500/sets/HydroInfo_500_S${SEED}.set -r overall_500.reference -o ./HydroInfo_500/metrics/HydroInfo_500_S${SEED}.metrics
            done
        done
    done
