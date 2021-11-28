#!/bin/bash
#SBATCH --mem=1G
#SBATCH -c4
#SBATCH --time=2-0

python metropolis_markov_chain.py 50 5 85