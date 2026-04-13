#!/bin/bash

#SBATCH --job-name=data_gen
#SBATCH --output=data_gen_%j.txt
#SBATCH --partition=mcs.default.q
#SBATCH --time=5-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G

# Execute the script or command
source venv/bin/activate
python timing_pareto_4_16.py