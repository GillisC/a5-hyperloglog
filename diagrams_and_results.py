#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import math

def distribution_graph(df):
    plt.figure()
    diagram_name = "p1_hash_distribution.pdf"
    histogram = sns.histplot(data=df, x="count", bins=32, kde=True)
    histogram.set_title("Frequency Distribution of Hash Values")
    histogram.set_xlabel("Hash Value")
    histogram.set_ylabel("Frequency")

    fig = histogram.get_figure()
    fig.savefig(diagram_name, format="pdf")
    plt.close()
    print(f"{diagram_name} created successfully")

def seed_distribution_graph(df):
    plt.figure()
    diagram_name = "p3_seed_distribution.pdf"
    histogram = sns.histplot(data=df, x="estimate", bins=30, kde=True)
    histogram.set_title("Frequency Distribution of Cardinality Estimates")
    histogram.set_xlabel("Cardinality Estimate")
    histogram.set_ylabel("Frequency")

    fig = histogram.get_figure()
    fig.savefig(diagram_name, format="pdf")
    plt.close()
    print(f"{diagram_name} created successfully")

def scalability_plot(df):
    plt.figure()
    diagram_name = "p3_scalability_plot.pdf"
    df["speedup"] = df["total_time"][0] / df["total_time"]
    plot = sns.lineplot(data=df, x="workers", y="speedup", marker="o")

    plot.set(title="Performance Scaling", xlabel="Workers", ylabel="Speedup")

    fig = plot.get_figure()
    fig.savefig(diagram_name, format="pdf")
    plt.close()
    print(f"{diagram_name} created successfully")


if __name__ == "__main__":
    # for the hash counts gather:
    # histogram, arithmetic mean, standard deviation
    dist_df = pd.read_csv("p1_distribution.csv")        
    
    mean = dist_df["count"].mean()
    std = dist_df["count"].std()

    collisions = dist_df["count"].sum()
    total_pairs = (collisions * (collisions - 1) / 2)
    colliding_pairs = dist_df["count"].apply(lambda x: x * (x - 1) / 2).sum()
    collision_prob = colliding_pairs / total_pairs

    print("============== Problem 1 Results ==============")
    
    print(f"distribution stats")
    print(f"\tperfect mean: {420769 / 128:.2f}")
    print(f"\tarithmetic mean: {mean:.2f}")
    print(f"\tstandard deviation: {std:.2f}")
    print(f"\tcollision probability: {collision_prob}")
    distribution_graph(dist_df)

    print("============== Problem 3 Results ==============")
    scalability_df = pd.read_csv("results_p3_b_big.csv")
    seed_dist_df = pd.read_csv("results_p3_c.csv")
    scalability_plot(scalability_df)
    seed_distribution_graph(seed_dist_df)
    print(f"seed distribution stats")
    print(f"\tarithmetic mean: {seed_dist_df["estimate"].mean():.2f}")
    print(f"\tstandard deviation: {seed_dist_df["estimate"].std():.2f}")
    # get the fraction of estimates that fall into interval n(1 +- ko) for k = [1,2,3
    n = 284689
    o = 1.04 / math.sqrt(1024)
    k_values = [1, 2, 3]
    for k in k_values:
        lower = n * (1 - k * o)
        upper = n * (1 + k * o)
        mask = (seed_dist_df["estimate"] >= lower) & (seed_dist_df["estimate"] <= upper)
        fraction = mask.mean()
        print(f"for k={k} fraction that fall inside of interval: {fraction}")

