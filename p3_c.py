#!/usr/bin/env python3

import secrets # used to generate random hex values
import argparse
import os
import subprocess
import re

def get_files(path):
    """
    A generator function: Iterates through all .txt files in the path and
    returns the content of the files

    Parameters:
    - path : string, path to walk through

    Yields:
    The content of the files as strings
    """
    for (root, dirs, files) in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                path = f'{root}/{file}'
                with open(path,'r') as f:
                    yield f.read()

def get_distinct_words(path) -> int:
    distinct_words = set() # set
    for f in get_files(path):
        for word in f.strip().split():
            distinct_words.add(word)

    return len(distinct_words)
        

def main() -> None:
    registers = 1024
    workers = 64

    # First get the exact number of distincs words 
    distinct_words_count = get_distinct_words("data/small")

    results = []
    for i in range(1000):
        seed = f"0x{secrets.token_hex(4)}" # random 32-bit hex value
        cmd = ["./assignment5_problem3.py", "-s", seed, "-m", str(registers), "-w", str(workers), f"data/small"]
        process = subprocess.run(cmd, capture_output=True, text=True)
        output = process.stdout

        if process.returncode != 0:
            print(f"Error: Subprocess failed with code in iteration {i}: {process.returncode}")
            print(process.stderr)
            print(process.stdout)
            exit()
        
        match = re.search(r"Cardinality estimate: ([\d.]+)", output)
        if not match:
            print("Failed to find pattern in stdout")
            exit()

        results.append({
            "seed": seed,
            "estimate": match.group(1),
        })
         
    with open("results_p3_c.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["seed", "estimate"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Correct number of distinct words: {distinct_words_count}")

if __name__ == "__main__":
    main()
