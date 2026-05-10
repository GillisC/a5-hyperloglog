#!/usr/bin/env python3

import argparse
import sys

from assignment5_problem1 import murmur3_32 as hash_function

def murmur3_32(key, seed):
    """Computes the 32-bit murmur3 hash"""
    # use the implementation from Problem 1
    return hash_function(key, seed)

def auto_int(x):
    """Auxiliary function to help convert e.g. hex integers"""
    return int(x,0)

def dlog2(n):
    """Auxiliary function to compute discrete base2 logarithm"""
    return n.bit_length() - 1

def rho(n):
    """Given a 32-bit number n, return the 1-based position of the first
    1-bit"""

    # Currently n is an integer

    n = n & 0xffffffff # make sure n is treated as 32-bit unsigned integer

    for i in range(32):
        if (n & 0x80000000) != 0: # check the most significant bit
            return i+1            # if it is 1, return the position (1-based)
        n = (n << 1) & 0xffffffff # left shift n by 1 bit and keep it as 32-bit unsigned integer

    return 0

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

def test() -> None:
    tests = [
        {"string": "", "seed": 0x00000000, "j": 0, "r": 0},
        {"string": "", "seed": 0x00000001, "j": 55, "r": 2},
        {"string": "", "seed": 0xffffffff, "j": 57, "r": 1},
        {"string": "test", "seed": 0x00000000, "j": 19, "r": 1},
        {"string": "test", "seed": 0x9747b28c, "j": 92, "r": 2},
        {"string": "Hello, world!", "seed": 0x00000000, "j": 67, "r": 1},
        {"string": "Hello, world!", "seed": 0x9747b28c, "j": 58, "r": 3},
        {
            "string": """The quick brown fox jumps over the lazy dog""",
            "seed": 0x00000000,
            "j": 35,
            "r": 3
        },
        {
            "string": """The quick brown fox jumps over the lazy dog""",
            "seed": 0x9747b28c,
            "j": 77,
            "r": 3
        },
        {
            "string": """Rýchla hnedá líška preskočila lenivého psa""",
            "seed": 0x00000000,
            "j": 105,
            "r": 2
        },
        {
            "string": """Rýchla hnedá líška preskočila lenivého psa""",
            "seed": 0x9747b28c,
            "j": 39,
            "r": 1
        },
        {
            "string": """Быстрая коричневая лиса перепрыгивает через ленивую собаку""",
            "seed": 0x00000000,
            "j": 117,
            "r": 1
        },
        {
            "string": """Быстрая коричневая лиса перепрыгивает через ленивую собаку""",
            "seed": 0x9747b28c,
            "j": 27,
            "r": 2
        },
        {"string": "敏捷的棕色狐狸跳过了懒狗", "seed": 0x00000000, "j": 100, "r": 2},
        {"string": "敏捷的棕色狐狸跳过了懒狗", "seed": 0x9747b28c, "j": 113, "r": 1}
    ]

    for test in tests:
        key = test["string"]
        seed = test["seed"]
        j = test["j"]
        r = test["r"]

        log2m = 7
        e_j, e_r = compute_jr(key, seed, log2m)

        p: bool = e_j == j and e_r == r
        if p:
            print(f"PASS key: {key}\tseed: {seed:#010x})")
        else:
            print(f"FAIL for key: {key} with seed: {seed}\n\tactual j={e_j}, expected j={j}\n\tactual r={e_r}, expected r={r}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Computes (j,r) pairs for input integers.'
    )
    parser.add_argument('key',nargs='*',help='key(s) to be hashed',type=str)
    parser.add_argument('-s','--seed',type=auto_int,default=0,help='seed value')
    parser.add_argument('-m','--num-registers',type=int,required=True,
                            help=('Number of registers (must be a power of two)'))
    args = parser.parse_args()

    seed = args.seed
    m = args.num_registers
    if m <= 0 or (m&(m-1)) != 0:
        sys.stderr.write(f'{sys.argv[0]}: m must be a positive power of 2\n')
        quit(1)

    log2m = dlog2(m)

    #test()

    for key in args.key:
        h = murmur3_32(key,seed)

        j, r = compute_jr(key,seed,log2m)

        print(f'{key}\t{j}\t{r}')
