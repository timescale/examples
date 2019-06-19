--
-- Vehicles on M routes
-- off-route in the last 15 minutes
-- 
SELECT
  bus.route_id,
  bus.time,
  bus.geom
FROM
  route_geofences AS route 
  JOIN mta AS bus 
  ON (route.route_id = bus.route_id) 
WHERE
  bus.time > now() - interval '15 minutes'
AND
  bus.route_id like 'M%'
AND NOT
  st_within(bus.geom, route.geom)
UNION
select route_id, null, geom from route_geofences where route_id like 'M%';