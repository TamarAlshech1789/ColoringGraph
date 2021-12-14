#!/bin/bash
#SBATCH --mem=1G
#SBATCH -c4
#SBATCH --time=5-0

python3 metropolis_markov_chain.py $1 $2 $3
