WITH window_mta AS (
	SELECT
	  time,
	  extract(epoch from (time - lag(time, 1) OVER (ORDER by time asc))) as time_delta,
	  st_distance(
		  st_transform(geom, 3857),  -- transform to a spatial reference system in meters
		  lag(st_transform(geom, 3857), 1) OVER (ORDER by time asc)
	  ) as distance
	FROM MTA
	WHERE time > now() - interval '1 day'
	AND vid = 'MTA NYCT_1062'
)
SELECT time, time_delta, distance, (distance / time_delta) * 2.23694 as mph 
FROM window_mta
WHERE time_delta > 0