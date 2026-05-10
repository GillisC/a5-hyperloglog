#!/usr/bin/env bash

#SBATCH --partition=short
#SBATCH -c 64
#SBATCH -o latest_p3_c_distinct_words.log

container="/data/courses/2026_dat471_dit066/containers/assignment4.sif"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a5-hyperloglog/data" \
    $container \
    bash -c "./p3_c.py;"
