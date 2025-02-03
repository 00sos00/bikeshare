Python with the `pandas` library is used here because it's fast and easy to use.

The processing stage begins by combining each csv file into one data frame. Then, two new columns are added, `month` and `daytime`. After that, the data is grouped by four categories:
* Rider type (`member_casual` column)
* Ride type
* Ride month
* Ride day time

Then a sample is taken from each group and then merged to form a big sample that is 10% of the original data size.

Now that the data is nicely sampled and merged, it could probably use some cleaning...

First, duplicates are removed based on the `ride_id` column. Then, the following columns are dropped because they are irrelevant to the business problem:
* ride_id
* start_station_name
* start_station_id
* end_station_name
* end_station_id

Also, rows with null values are removed. And finally, data values should be consistent so the only columns that were checked are `rideable_type` and `member_casual` because they contains categorical values.

At the end, the cleaned data is written to a new csv file which will then be imported into a relational database for further analysis using SQL.