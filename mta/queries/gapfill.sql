set timezone to 'est';
--
-- Hourly count of the number vehicles on a given route
-- with gapfill, locf, and interpolate
--
SELECT
	-- 4 ways to handle data gaps
    count(distinct vid) as n_vehicles,
	coalesce(count(distinct vid), 0) as count,
	locf(count(distinct vid)),
	interpolate(count(distinct vid)::real),
    time_bucket_gapfill('1 hour', time) AS hour
FROM
    mta
WHERE
    time between '2019-03-05' AND '2019-03-06'
    AND route_id = 'M100'
GROUP BY
    hour;