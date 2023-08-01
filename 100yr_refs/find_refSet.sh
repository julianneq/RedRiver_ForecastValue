#/bin/bash
python pareto.py ./optimization/*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/overall_100yr.reference --delimiter=" " --comment='#'
python pareto.py ./reevaluation/*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/overall_re-eval_100yr.reference --delimiter=" " --comment='#'

python pareto.py ./optimization/*100.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/BL100_HI100_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/*100*100yr.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/BL100_HI100_re-eval_100yr.reference --delimiter=" " --comment="#"

python pareto.py ./optimization/*500*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/BL500_HI500_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/*500*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/BL500_HI500_re-eval_100yr.reference --delimiter=" " --comment="#"

python pareto.py ./optimization/baseline_100.reference ./optimization/HydroInfo_500_100yr.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/BL100_HI500_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/baseline_100_re-eval_100yr.reference ./reevaluation/HydroInfo_500_re-eval_100yr.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/BL100_HI500_re-eval_100yr.reference --delimiter=" " --comment="#"

python pareto.py ./optimization/baseline_500_100yr.reference ./optimization/HydroInfo_100.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/BL500_HI100_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/baseline_500_re-eval_100yr.reference ./reevaluation/HydroInfo_100_re-eval_100yr.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/BL500_HI100_re-eval_100yr.reference --delimiter=" " --comment="#"

python pareto.py ./optimization/baseline*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/BL100_BL500_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/baseline*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/BL100_BL500_re-eval_100yr.reference --delimiter=" " --comment="#"

python pareto.py ./optimization/HydroInfo*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./optimization/HI100_HI500_100yr.reference --delimiter=" " --comment="#"
python pareto.py ./reevaluation/HydroInfo*.reference -o 0-2 -e 0.5 25.0 0.05 --output ./reevaluation/HI100_HI500_re-eval_100yr.reference --delimiter=" " --comment="#"