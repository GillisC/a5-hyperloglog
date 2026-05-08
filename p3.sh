#!/usr/bin/env bash

#SBATCH -c 32
#SBATCH -o latest.log

container="/data/courses/2026_dat471_dit066/containers/assignment5.sif"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a5-hyperloglog/data" \
    $container \
    bash -c "./assignment5_problem3.py -s 0x9747b28c -m 16 -w 32 data/small;"
