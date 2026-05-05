#!/usr/bin/env python3

import seaborn as sns
import pandas as pd

def distribution_graph(df):
    diagram_name = "p1_hash_distribution.pdf"
    histogram = sns.histplot(data=df, x="index", weights="count", bins=128)
    histogram.set_title("Hash Distribution")
    histogram.set_xlabel("Hash Index")
    histogram.set_ylabel("Count")

    fig = histogram.get_figure()
    fig.savefig(diagram_name, format="pdf")
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
    
    print(f"distribution stats")
    print(f"\tperfect mean: {420769 / 128:.2f}")
    print(f"\tarithmetic mean: {mean:.2f}")
    print(f"\tstandard deviation: {std:.2f}")
    print(f"\tcollision probability: {collision_prob}")

    distribution_graph(dist_df)
