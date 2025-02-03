import os
import pandas as pd
from tqdm import tqdm
from numpy import round, sin, cos, atan2, pow, sqrt, radians

def month(row):
    return row["started_at"].month

def daytime(row):
    hour = row["started_at"].hour
    if 5 <= hour < 12: return "Morning"
    elif 12 <= hour < 19: return "Afternoon"
    elif 19 <= hour <= 23: return "Evening"
    else: return "Night"

dfs = []
datadir = "./data"
for filename in tqdm(os.listdir(datadir), "Loading files"):
    if not filename.endswith(".csv"): continue
    dfs.append(pd.read_csv(datadir + "/" + filename))
merged_df = pd.concat(dfs)
merged_df["started_at"] = pd.to_datetime(merged_df["started_at"], format="ISO8601")
merged_df["ended_at"] = pd.to_datetime(merged_df["ended_at"], format="ISO8601")
merged_df["month"] = merged_df.apply(month, axis=1)
merged_df["daytime"] = merged_df.apply(daytime, axis=1)
print("Grouping...")
groups = merged_df.groupby(["member_casual", "rideable_type", "month", "daytime"])
print("Grouping done.")
sample_size_perc = 0.1
sampled_dfs = []
merged_df_rows_num = merged_df.shape[0]
total_target_rows_num = sample_size_perc * merged_df_rows_num
for g, group_df in tqdm(groups, "Sampling"):
    print("Sampling group:", g)
    group_rows_num = group_df.shape[0]
    original_group_perc = group_rows_num / merged_df_rows_num
    new_group_rows_num = original_group_perc * total_target_rows_num
    group_df.drop(columns=["month", "daytime"], inplace=True)
    sampled_dfs.append(group_df.sample(n=int(round(new_group_rows_num))))

merged_df = pd.concat(sampled_dfs)
print("Sampling done.")
print()

print("Cleaning...")
merged_df.drop_duplicates(subset=["ride_id"], inplace=True)
print("Duplicates removed.")
merged_df.drop(columns=[
    "ride_id",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id"
], inplace=True)
print("Dropped irrelevant columns")
# dropna returns a new dataframe so don't forget 'inplace'
merged_df.dropna(inplace=True)
print("Dropped rows with nulls")

# Check for consistency
#print(merged_df["rideable_type"].unique())
#print(merged_df["member_casual"].unique())

# Reposition column
memcas = merged_df.pop("member_casual")
merged_df.insert(0, "member_casual", memcas)
print("Repositioned 'member_casual' column")

# Might as well convert lats and longs to actual distance
# By using The Haversine formula.
distance_column = []
for i, r in tqdm(merged_df.iterrows(), "Creating distance column"):
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
merged_df.drop(columns=["start_lat", "start_lng", "end_lat", "end_lng"], inplace=True)
merged_df["distance_meters"] = distance_column
print("Created new 'distance' column")

# Remove any trips that were below 60 seconds in length
# (potentially false starts or users trying to re-dock a bike to ensure it was secure)
# Max distance is 70km according to divvy
print("Removing trips below 60 seconds or above 70km")
merged_df = merged_df[
    (merged_df["distance_meters"] > 0) &
    (merged_df["distance_meters"] <= 70000) &
    ((merged_df["ended_at"] - merged_df["started_at"]).dt.seconds > 60)
]

merged_df.to_csv("sampled_cleaned.csv", index=False)
print("Sampling & Cleaning done successfully.")