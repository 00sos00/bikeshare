The processing stage begins by taking a sample from each month csv file.
Because taking all data within each month would slow the analyze stage, sampling is used here.

Python with the `pandas` library is used here because it's fast and easy to use.

The sample size is determined using the following python code:
```python
avg_rows = floor(n / 12)
perc = 20
sample_size = perc / 100 * avg_rows
```
Where:
* `n` is the total number of rows across all 12 months.
* `perc` is the percentage taken from the average. In this case, it's 20% of the average number of rows.

Since the data is distributed randomly in each month, random sampling is used here. Then all samples are combined into 1 data frame that represents the whole year.
```python
samp = month_data.sample(n=sample_size_per_month)
dfs.append(samp)
raw_merged = pd.concat(dfs)
raw_merged.to_csv("raw_merged.csv", index=False)
```
The merged data is written to a separate csv file. This is to make loading the data more convenient for the cleaning phase. Now that the data is nicely sampled and merged, it could probably use some cleaning.

First, duplicates are removed based on the `ride_id` column:
```python
raw_merged = pd.read_csv("raw_merged.csv")
raw_merged.drop_duplicates(subset=["ride_id"], inplace=True)
```

Then, irrelevant columns are dropped:
```python
raw_merged.drop(columns=[  
    "ride_id",  
    "start_station_name",  
    "start_station_id",  
    "end_station_name",  
    "end_station_id"  
], inplace=True)
```

Also, rows with null values are removed:
```python
raw_merged.dropna(inplace=True)
```

And finally, data values should be consistent:
```python
print(raw_merged["rideable_type"].unique())  
print(raw_merged["member_casual"].unique())
```
The only columns that were checked are `rideable_type` and `member_casual` because they contains categorical values.

Notice that `inplace=True` is used across the whole cleaning process. This is to ensure modifications are applied on the original data frame `raw_merged`.

At the end, the cleaned data is written to a new csv file:
```python
raw_merged.to_csv("cleaned_merged.csv", index=False)
```
Which will then be imported into a relational database for further analysis using SQL.