create table ride (
	member_casual varchar(25),
	rideable_type varchar(25),
	started_at datetime,
	ended_at datetime,
	distance_meters float
);

load data infile "cleaned_merged.csv"
into table ride
fields terminated by ','
lines terminated by '\n'
ignore 1 rows;

