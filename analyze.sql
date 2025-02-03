-- What is the average ride duration for members vs casuals?
select
	member_casual,
	round(
		avg(time_to_sec(timediff(ended_at, started_at)) / 60)
	) as avg_ride_dur_mins
from ride
group by member_casual;





-- What is the average ride distance for members vs casuals?
select
	member_casual,
	round(avg(distance_meters)) as avg_ride_distance_meters
from ride
group by member_casual;





-- What are the most used bike types for members vs casuals?
select
	member_casual,
	rideable_type,
	count(*) as rides_num
from ride
group by member_casual, rideable_type
order by member_casual, rides_num desc;





-- What are the peak times of the day for members vs casuals?
select
	member_casual,
	(case
		when hour(started_at) >= 5 and hour(started_at) < 12 then "Morning"
		when hour(started_at) >= 12 and hour(started_at) < 19 then "Afternoon"
		when hour(started_at) >= 19 and hour(started_at) < 23 then "Evening"
		else "Night"
	end) as daytime,
	count(*) as rides_num
from ride
group by member_casual, daytime
order by member_casual, rides_num desc;





-- What are the peak months of the year for members vs casuals?
select
	member_casual,
	monthname(started_at) as month_name,
	count(*) as rides_num
from ride
group by member_casual, month_name
order by member_casual, rides_num desc