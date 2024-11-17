import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_distributions(sampled_bed, ref_dist_file, output_plot):
    # Compute sampled distribution
    sampled_bed = pd.read_csv(sampled_bed, sep="\t", header=None, names=["chrom", "start", "end"])
    sampled_bed["fragment_length"] = sampled_bed["end"] - sampled_bed["start"]
    sampled_dist = sampled_bed["fragment_length"].value_counts(normalize=True).sort_index()

    # Load reference distribution
    ref_dist = pd.read_csv(ref_dist_file, sep="\t", header=None, names=["length", "freq"])
    ref_dist.set_index("length", inplace=True)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(sampled_dist.index, sampled_dist.values, label="Sampled Query", color="blue")
    plt.plot(ref_dist.index, ref_dist["freq"], label="Reference", color="green")
    plt.xlabel("Fragment Length")
    plt.ylabel("Normalized Frequency")
    plt.legend()
    plt.savefig(output_plot)

if __name__ == "__main__":
    sampled_file = sys.argv[1]
    ref_dist_file = sys.argv[2]
    output_plot = sys.argv[3]
    
    plot_distributions(sampled_file, ref_dist_file, output_plot)
