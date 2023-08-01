#/bin/bash
python pareto.py *100*.reference -o 0-2 -e 0.5 25.0 0.05 --output overall_100.reference --delimiter=" " --comment="#"
python pareto.py *500*.reference -o 0-2 -e 0.5 25.0 0.05 --output overall_500.reference --delimiter=" " --comment="#"