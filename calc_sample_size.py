import os
import pandas as pd
from math import floor

n = 0
data_dir = "data/"
for filename in os.listdir(data_dir):
	if not filename.endswith(".csv"): continue
	df = pd.read_csv(data_dir + filename)
	print(f"Loading {filename} with {df.shape[0]} rows")
	n += df.shape[0]

# Divide by 12 here because we read 12 months
avg_rows = floor(n / 12)
print(f"Average amount of rows: {avg_rows}")
perc = 20
sample_size = perc / 100 * avg_rows
print(f"Final sample size per month: {sample_size}")