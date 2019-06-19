set timezone to 'EST';
--
-- All data for the last minute
--

SELECT *
FROM mta
WHERE time > now() - interval '1 minute'
ORDER BY time DESC;