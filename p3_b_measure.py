#!/usr/bin/env python3

import subprocess
import re
import csv

workers = [1, 2, 4, 8, 16, 32, 64]
results = []

dataset = "big"
registers = 1024
seed = 0x9747b28c

for w in workers:
    cmd = ["./assignment5_problem3.py", "-s", str(seed), "-m", str(registers), "-w", str(w), f"data/{dataset}"]
    process = subprocess.run(cmd, capture_output=True, text=True)
    output = process.stdout

    if process.returncode != 0:
        print(f"Error: Subprocess failed with code: {process.returncode}")
        print(process.stderr)
        print(process.stdout)
        exit()
    else:
        match = re.search(r"Took ([\d.]+)", output)

        if match:
            total_time = match.group(1)

            results.append({
                "dataset": dataset,
                "workers": w,
                "total_time": total_time,
            })
        elif not match:
            print("Failed to find 'total time:' in stdout")
            exit()

    print(f"finished run using {w} workers")

with open("results_p3_b_big.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["dataset", "workers", "total_time"])
    writer.writeheader()
    writer.writerows(results)
