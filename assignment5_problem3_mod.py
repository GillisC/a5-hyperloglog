#!/usr/bin/env python3

import argparse
import sys
import os
from pyspark import SparkContext, SparkConf
import math
import time
import secrets
import csv

from assignment5_problem1 import murmur3_32 as hash_function
from assignment5_problem2 import rho as get_rho

def murmur3_32(key, seed):
    """Computes the 32-bit murmur3 hash"""
    # Use implementation from problem 1
    return hash_function(key, seed)

def auto_int(x):
    """Auxiliary function to help convert e.g. hex integers"""
    return int(x,0)

def dlog2(n):
    return n.bit_length() - 1

def rho(n):
    # Use implementation from problem 2
    return get_rho(n)


def compute_jr(key,seed,log2m):
    """hash the string key with murmur3_32, using the given seed
    then take the **least significant** log2(m) bits as j
    then compute the rho value **from the left**

    E.g., if m = 1024 and we compute hash value 0x70ffec73
    or 0b01110000111111111110110001110011
    then j = 0b0001110011 = 115
         r = 2
         since the 2nd digit of 0111000011111111111011 is the first 1

    Return a tuple (j,r) of integers
    """
    h = murmur3_32(key,seed)
    j = ~(0xffffffff << log2m) & h
    #print(f"hash: {h:0>32b}")
    r = rho(h)
    return j, r

def alpha(m):
    """Auxiliary function: bias correction"""
    # according to wikipedia
    if m == 16:
        return 0.673
    elif m == 32:
        return 0.697
    elif m == 64:
        return 0.709
    else:
        return (0.7213 / (1 + 1.079 / m))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Using HyperLogLog, computes the approximate number of '
            'distinct words in all .txt files under the given path.'
    )
    parser.add_argument('path',help='path to walk',type=str)
    parser.add_argument('-s','--seed',type=auto_int,default=0,help='seed value')
    parser.add_argument('-m','--num-registers',type=int,required=True,
                            help=('number of registers (must be a power of two)'))
    parser.add_argument('-w','--num-workers',type=int,default=1,
                        help='number of Spark workers')
    args = parser.parse_args()

    seed = args.seed
    m = args.num_registers
    if m <= 0 or (m&(m-1)) != 0:
        sys.stderr.write(f'{sys.argv[0]}: m must be a positive power of 2\n')
        quit(1)

    log2m = dlog2(m)

    num_workers = args.num_workers
    if num_workers < 1:
        sys.stderr.write(f'{sys.argv[0]}: must have a positive number of '
                         'workers\n')
        quit(1)

    path = args.path
    if not os.path.isdir(path):
        sys.stderr.write(f"{sys.argv[0]}: `{path}' is not a valid directory\n")
        quit(1)

    start = time.time()
    conf = SparkConf()
    conf.setMaster(f'local[{num_workers}]')
    conf.set('spark.driver.memory', '16g')
    sc = SparkContext(conf=conf)

    # data can be thought of like a long string containing the file contents
    data = sc.textFile(f"{path}/*.txt") # nodes read files instead of the driver
    
    seeds = [int(secrets.token_hex(4), 16) for _ in range(1000)]
    b_seeds = sc.broadcast(seeds)

    # main computation part
    # incoming data is a single file content as a single string
    # split the string into words
    # get the j and rho from the word
    # reduceByKey(max) takes all j and rho values and for each unique j reduces to the max rho value found
    results = data.flatMap(lambda x: x.split()) \
        .flatMap(lambda word: [
            ((seed_idx, compute_jr(word, seed, log2m)[0]), compute_jr(word, seed, log2m)[1])
            for seed_idx, seed in enumerate(b_seeds.value)
            ]) \
        .map(lambda x: (x[0], x[1]))
    
    # execute
    registers = results.reduceByKey(max).collect()

    estimates = {}
    for (seed_idx, j), r in registers:
        if seed_idx not in estimates:
            estimates[seed_idx] = [0] * m
        estimates[seed_idx][j] = r

    results = []
    for seed_idx, r_values in estimates.items():
        # harmonic mean calculation for all registers
        harm_mean = sum(1.0 / (2**r) for r in r_values)
        E = alpha(m) * (m**2) / harm_mean
        results.append({
            "seed_idx": seed_idx,
            "estimate": E,
        })
    
    with open("results_p3_c.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["seed_idx", "estimate"])
        writer.writeheader()
        writer.writerows(results)

    end = time.time()
    print(f'Took {end-start} s')

    
    

    

