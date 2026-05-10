#!/usr/bin/env bash

# For getting the results for Problem 3 a)
# Run the program on the huge dataset using 1024 registers and the seed: 0x9747b28c

#SBATCH -c 64
#SBATCH -o latest_huge.log

container="/data/courses/2026_dat471_dit066/containers/assignment5.sif"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a5-hyperloglog/data" \
    $container \
    bash -c "./assignment5_problem3.py -s 0x9747b28c -m 1024 -w 64 data/huge;"
