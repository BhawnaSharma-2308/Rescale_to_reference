import pandas as pd
import sys

def compute_fragment_length(bed_file):
    # Compute fragment lengths from BED file
    df = pd.read_csv(bed_file, sep="\t", header=None, names=["chrom", "start", "end"])
    df["fragment_length"] = df["end"] - df["start"]
    return df["fragment_length"]

if __name__ == "__main__":
    query_file = sys.argv[1]
    output_file = sys.argv[2]

    fragment_lengths = compute_fragment_length(query_file)
    distribution = fragment_lengths.value_counts(normalize=True).sort_index()

    # Save distribution to file
    distribution.to_csv(output_file, sep="\t", header=False)
