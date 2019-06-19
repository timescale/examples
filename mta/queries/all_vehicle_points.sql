SELECT
    st_collect (geom), route_id
FROM
    mta
WHERE
    time > now() - interval '1 day'
    AND vid = 'MTA NYCT_1062'
GROUP BY route_id