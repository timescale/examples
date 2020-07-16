-----------------------------------
-- Demo 1
-- 3 day time shift
-----------------------------------
-- What to name the series
SELECT time, ride_count, CASE WHEN step = 0 THEN 'today' ELSE (-interval)::text END AS metric
FROM
-- sub-query to generate the intervals
( SELECT step, (step||'day')::interval AS interval FROM generate_series(0,3) g(step)) g_offsets
JOIN LATERAL (
-- subquery to select the rides 
SELECT
-- adding set interval to time values
  time_bucket('15m',pickup_datetime + interval)::timestamptz AS time, count(*) AS ride_count FROM rides
-- subtract value of interval from time to plot
-- today = 0, 1 day ago = 1, etc
WHERE
  pickup_datetime BETWEEN $__timeFrom()::timestamptz - interval AND $__timeTo()::timestamptz - interval
GROUP BY 1
ORDER BY 1
) l ON true


-----------------------------------
-- Demo 1
-- 7 day time shift
-----------------------------------
SELECT time, ride_count, CASE WHEN step = 0 THEN 'today' ELSE (-interval)::text END AS metric
FROM
( SELECT step, (step||'week')::interval AS interval FROM generate_series(0,1) g(step)) g_offsets
JOIN LATERAL (
SELECT
  time_bucket('15m',pickup_datetime + interval)::timestamptz AS time, count(*) AS ride_count FROM rides
WHERE
  pickup_datetime BETWEEN $__timeFrom()::timestamptz - interval AND $__timeTo()::timestamptz - interval
GROUP BY 1
ORDER BY 1
) l ON true

-----------------------------------
-- Demo 2
-- Auto-changing aggregate queried
-----------------------------------
-- Use Daily aggregate for intervals greater than 14 days
SELECT day as time, ride_count, 'daily' AS metric
FROM rides_daily
WHERE
  $__timeTo()::timestamp - $__timeFrom()::timestamp > '14 days'::interval AND
  $__timeFilter(day)
UNION ALL
-- Use hourly aggregate for intervals between 3 and 14 days
SELECT hour, ride_count, 'hourly' AS metric
FROM rides_hourly
WHERE
  $__timeTo()::timestamp - $__timeFrom()::timestamp BETWEEN '3 days'::interval AND '14 days'::interval AND
  $__timeFilter(hour)
UNION ALL
-- Use raw data (minute intervals) intervals between 0 and 3 days
SELECT * FROM
(
SELECT time_bucket('1m',pickup_datetime) AS time, count(*), 'minute' AS metric
FROM rides
WHERE
  $__timeTo()::timestamp - $__timeFrom()::timestamp < '3 days'::interval AND
  $__timeFilter(pickup_datetime)
GROUP BY 1
) minute
ORDER BY 1;
