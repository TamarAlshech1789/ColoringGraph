#!/bin/bash
#SBATCH --mem=1G
#SBATCH -c4
#SBATCH --time=2:0:0

python metropolis_markov_chain.py 14 8