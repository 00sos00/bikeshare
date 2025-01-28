import os
import pandas as pd

dfs = []
datadir = "./data"
sample_size_per_month = 97676
for filename in os.listdir(datadir):
    if not filename.endswith(".csv"): continue
    print(f"Loading {filename}")
    month_data = pd.read_csv(datadir + "/" + filename)
    samp = month_data.sample(n=sample_size_per_month)
    dfs.append(samp)

raw_merged = pd.concat(dfs)
raw_merged.to_csv("raw_merged.csv", index=False)

print("Sampling & Merging done successfully.")

