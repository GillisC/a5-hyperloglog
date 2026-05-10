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

    print(f"Correct number of distinct words: {distinct_words_count}")

if __name__ == "__main__":
    main()
