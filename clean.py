import pandas as pd
from math import sin, cos, atan2, pow, sqrt, radians

print("Loading raw data...")
raw_merged = pd.read_csv("raw_merged.csv")
raw_merged.drop_duplicates(subset=["ride_id"], inplace=True)
raw_merged.drop(columns=[
    "ride_id",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id"
], inplace=True)
# dropna returns a new dataframe so don't forget 'inplace'
raw_merged.dropna(inplace=True)

# Check for consistency
#print(raw_merged["rideable_type"].unique())
#print(raw_merged["member_casual"].unique())

# Reposition column
memcas = raw_merged.pop("member_casual")
raw_merged.insert(0, "member_casual", memcas)

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
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = 6371000 * c
    distance_column.append(d)
raw_merged.drop(columns=["start_lat", "start_lng", "end_lat", "end_lng"], inplace=True)
raw_merged["distance_meters"] = distance_column

raw_merged.to_csv("cleaned_merged.csv", index=False)

print("Data cleaning done successfuly.")