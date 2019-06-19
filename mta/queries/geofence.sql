set timezone to 'est';
--
-- What bus routes pass near 355 Madison Ave each hour?
--


WITH geofence AS (
    SELECT buffer_meters(-74.00482, 40.7233, 200) AS buffer
)
SELECT
    time_bucket_gapfill('1 hour', time) AS hour,
    array_agg(DISTINCT route_id) AS nearby_routes
FROM
    mta,
    geofence
WHERE
    time BETWEEN now() - interval '5 days' AND now()
    AND st_intersects(buffer, mta.geom)
GROUP BY
    hour;

