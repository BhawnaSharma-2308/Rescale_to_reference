import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define input, output, and script
QUERY_FILE = "shuf.a.bed"
REFERENCE_DIST = "reference.hist"
OUTPUT_SAMPLED_FILE = "results/sampled_query.bed"
PLOT_OUTPUT = "results/distribution_comparison.png"

rule all:
    input:
        OUTPUT_SAMPLED_FILE,
        PLOT_OUTPUT

# Step 1: Compute Fragment Length Distribution from Query File
rule compute_query_distribution:
    input:
        "shuf.a.bed"
    output:
        "results/query_distribution.txt"
    script:
        "scripts/compute_query_distribution.py {input} {output}"

# Step 2: Sample Query BED File to Match Reference Distribution
rule resample_query:
    input:
        query_dist="results/query_distribution.txt",
        ref_dist=REFERENCE_DIST,
        query_bed=QUERY_FILE
    output:
        OUTPUT_SAMPLED_FILE
    script:
        "scripts/resample_query.py"

# Step 3: Plot Distributions for Validation
rule plot_distributions:
    input:
        sampled_bed=OUTPUT_SAMPLED_FILE,
        ref_dist=REFERENCE_DIST
    output:
        PLOT_OUTPUT
    script:
        "scripts/plot_distributions.py"
