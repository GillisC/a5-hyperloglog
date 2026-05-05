#!/usr/bin/env python3

import argparse
import csv

from assignment5_problem1 import murmur3_32

# lazy read lines from text file
def get_lines(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Computes a distribution of hashes from a word file (7 LSB)."
    )
    parser.add_argument("filename", help="filename with word(s) to be hashed", type=str)
    args = parser.parse_args()

    filename = args.filename
    seed = 0xee418b6c
    mask = 0x7f # 128 - 1

    counts = {}

    for word in get_lines(filename):
        h = murmur3_32(word, seed)
        index = h & mask # grab the 7 least significant bits
        if index not in counts.keys():
            counts[index] = 1
        else:
            counts[index] += 1

    # list of tuples easier for the csv
    data = list(counts.items())

    with open("p1_distribution.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "count"])
        writer.writerows(data)
