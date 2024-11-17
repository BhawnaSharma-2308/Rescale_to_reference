import pandas as pd
import numpy as np
import sys

def resample_query(query_dist, ref_dist, query_file):
    # Load distributions
    query_dist = pd.read_csv(query_dist, sep="\t", header=None, names=["length", "freq"])
    ref_dist = pd.read_csv(ref_dist, sep="\t", header=None, names=["length", "freq"])
    
    # Normalize reference distribution to match query size
    query_size = query_dist["freq"].sum()
    ref_dist["freq"] = ref_dist["freq"] * (query_size / ref_dist["freq"].sum())

    # Compute sampling probabilities
    merged = pd.merge(query_dist, ref_dist, on="length", how="outer").fillna(0)
    merged["sampling_prob"] = merged["freq_y"] / merged["freq_x"]
    
    # Load query BED file
    query_bed = pd.read_csv(query_file, sep="\t", header=None, names=["chrom", "start", "end"])
    query_bed["fragment_length"] = query_bed["end"] - query_bed["start"]
    
    # Sample query BED file
    sampled_rows = []
    for length, prob in merged[["length", "sampling_prob"]].values:
        rows = query_bed[query_bed["fragment_length"] == length]
        sample_size = int(min(len(rows), len(rows) * prob))
        sampled_rows.append(rows.sample(n=sample_size, replace=False))
    
    return pd.concat(sampled_rows)

if __name__ == "__main__":
    query_dist_file = sys.argv[1]
    ref_dist_file = sys.argv[2]
    query_file = sys.argv[3]
    output_file = sys.argv[4]

    sampled_df = resample_query(query_dist_file, ref_dist_file, query_file)
    sampled_df.drop(columns=["fragment_length"]).to_csv(output_file, sep="\t", index=False, header=False)
