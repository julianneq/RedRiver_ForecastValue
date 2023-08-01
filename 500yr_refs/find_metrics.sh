JAVA_ARGS="-cp MOEAFramework-2.4-Demo.jar"

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./optimization/baseline_500.reference -r ./optimization/overall_500yr.reference \
-o ./optimization/metrics/baseline_500.metrics

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./reevaluation/baseline_500_re-eval_500yr.reference -r ./reevaluation/overall_re-eval_500yr.reference \
-o ./reevaluation/metrics/baseline_500_re-eval_500yr.metrics


java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./optimization/baseline_100_500yr.reference -r ./optimization/overall_500yr.reference \
-o ./optimization/metrics/baseline_100_500yr.metrics

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./reevaluation/baseline_100_re-eval_500yr.reference -r ./reevaluation/overall_re-eval_500yr.reference \
-o ./reevaluation/metrics/baseline_100_re-eval_500yr.metrics


java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./optimization/HydroInfo_500.reference -r ./optimization/overall_500yr.reference \
-o ./optimization/metrics/HydroInfo_500.metrics

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./reevaluation/HydroInfo_500_re-eval_500yr.reference -r ./reevaluation/overall_re-eval_500yr.reference \
-o ./reevaluation/metrics/HydroInfo_500_re-eval_500yr.metrics


java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./optimization/HydroInfo_100_500yr.reference -r ./optimization/overall_500yr.reference \
-o ./optimization/metrics/HydroInfo_100_500yr.metrics

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 \
-i ./reevaluation/HydroInfo_100_re-eval_500yr.reference -r ./reevaluation/overall_re-eval_500yr.reference \
-o ./reevaluation/metrics/HydroInfo_100_re-eval_500yr.metrics
