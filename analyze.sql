-- remove any trips that were below 60 seconds in length
-- (potentially false starts or users trying to re-dock a bike to ensure it was secure)
-- Max distance is 70km according to divvy
delete from ride
where
	time_to_sec(timediff(ended_at, started_at)) < 60 or
	distance_meters > 70000;

select
	member_casual,
	time_to_sec(timediff(ended_at, started_at)) / 60 as dur_mins,
	distance_meters
from ride
order by distance_meters desc;

with rides as (
	select
		member_casual,
		rideable_type,
		count(*) as rides_num
	from ride
	group by member_casual, rideable_type
	order by member_casual
)
select
	*,
	sum(rides_num) over(partition by member_casual) as total_rides
from rides;

select
	month(started_at) as month,
	member_casual,
	count(*) rides_num,
	round(
		avg(time_to_sec(timediff(ended_at, started_at)) / 60)
	) as avg_ride_time_mins
from ride
group by month(started_at), member_casual
order by month(started_at);

select
	member_casual,
	round(avg(distance_meters)) as avg_distance
from ride
group by member_casual;

