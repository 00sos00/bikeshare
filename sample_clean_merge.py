import os
import pandas as pd
from numpy import round, sin, cos, atan2, pow, sqrt, radians

def month(row):
    return row["started_at"].month

def daytime(row):
    hour = row["started_at"].hour
    if 5 <= hour < 12: return "Morning"
    elif 12 <= hour < 17: return "Afternoon"
    elif 17 <= hour < 22: return "Evening"
    else: return "Night"

dfs = []
datadir = "./data"
for filename in os.listdir(datadir):
    if not filename.endswith(".csv"): continue
    print(f"Loading {filename}")
    dfs.append(pd.read_csv(datadir + "/" + filename))
raw_merged = pd.concat(dfs)
raw_merged["started_at"] = pd.to_datetime(raw_merged["started_at"], format="ISO8601")
raw_merged["month"] = raw_merged.apply(month, axis=1)
raw_merged["daytime"] = raw_merged.apply(daytime, axis=1)
groups = raw_merged.groupby(["member_casual", "rideable_type", "month", "daytime"])
print("Grouping done.")

sampled_dfs = []
target_perc = 0.1
total_target_rows = target_perc * raw_merged.shape[0]
for g, group_df in groups:
    print("Sampling group:", g)
    group_row_num = group_df.shape[0]
    original_group_proportion = group_row_num / raw_merged.shape[0]
    new_group_row_num = original_group_proportion * total_target_rows
    group_df.drop(columns=["month", "daytime"], inplace=True)
    sampled_dfs.append(group_df.sample(n=int(round(new_group_row_num))))

raw_merged = pd.concat(sampled_dfs)

print()
print("Cleaning time...")
raw_merged.drop_duplicates(subset=["ride_id"], inplace=True)
print("Duplicates removed.")
raw_merged.drop(columns=[
    "ride_id",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id"
], inplace=True)
print("Dropped irrelevant columns")
# dropna returns a new dataframe so don't forget 'inplace'
raw_merged.dropna(inplace=True)
print("Dropped rows with nulls")

# Check for consistency
#print(raw_merged["rideable_type"].unique())
#print(raw_merged["member_casual"].unique())

# Reposition column
memcas = raw_merged.pop("member_casual")
raw_merged.insert(0, "member_casual", memcas)
print("Repositioned 'member_casual' column")

# Might as well convert lats and longs to actual distance
# By using The Haversine formula.
distance_column = []
for i, r in raw_merged.iterrows():
    lat1 = r["start_lat"]
    lng1 = r["start_lng"]
    lat2 = r["end_lat"]
    lng2 = r["end_lng"]

    a = (pow(sin(radians(lat2 - lat1) / 2), 2) +
        cos(lat1) *
        cos(lat2) *
        pow(sin(radians(lng2 - lng1) / 2), 2))
    if a <= 0: c = 0
    else: c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = 6371000 * c
    distance_column.append(d)
raw_merged.drop(columns=["start_lat", "start_lng", "end_lat", "end_lng"], inplace=True)
raw_merged["distance_meters"] = distance_column
print("Created new 'distance' column")

raw_merged.to_csv("cleaned_merged.csv", index=False)

print("Sampling & Merging done successfully.")

