set timezone to 'est';
--
-- Hourly count of the number vehicles on a given route
--
SELECT
    count(distinct vid) as n_vehicles,
    time_bucket('1 hour', time) AS hour
FROM
    mta
WHERE
    time between '2019-03-05' AND '2019-03-06'
    AND route_id = 'M100'
GROUP BY
    hour;

