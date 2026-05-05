#!/usr/bin/env bash

#SBATCH -c 1
#SBATCH -o latest.log

container="/data/courses/2026_dat471_dit066/containers/assignment5.sif"
data="/data/courses/2026_dat471_dit066/datasets/words"

apptainer exec \
    --bind "$HOME" \
    --bind "$data:$HOME/a5-hyperloglog/data/words" \
    $container \
    bash -c "./p1_get_distribution.py data/words;"
