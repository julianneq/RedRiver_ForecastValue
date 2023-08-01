NSEEDS=10
SEEDS=$(seq 1 ${NSEEDS})
JAVA_ARGS="-cp MOEAFramework-2.4-Demo.jar"

for SEED in ${SEEDS}
do
	java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
    -d 3 -i ./baseline_100/objs/runtime/reference/baseline_100_S${SEED}.runref -r overall_100.reference \
    -o ./baseline_100/metrics/runtime/baseline_100_S${SEED}.metrics

    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
    -d 3 -i ./baseline_500/objs/runtime/reference/baseline_500_S${SEED}.runref -r overall_500.reference \
    -o ./baseline_500/metrics/runtime/baseline_500_S${SEED}.metrics

    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
    -d 3 -i ./HydroInfo_100/objs/runtime/reference/HydroInfo_100_S${SEED}.runref -r overall_100.reference \
    -o ./HydroInfo_100/metrics/runtime/HydroInfo_100_S${SEED}.metrics

    java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
    -d 3 -i ./HydroInfo_500/objs/runtime/reference/HydroInfo_500_S${SEED}.runref -r overall_500.reference \
    -o ./HydroInfo_500/metrics/runtime/HydroInfo_500_S${SEED}.metrics
done
