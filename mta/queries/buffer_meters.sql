create or replace function buffer_meters (lon numeric, lat numeric, meters numeric)
returns geometry as $$
BEGIN
-- Buffers by meters in the spherical mercator projection
-- (not accurate at high latitudes)
RETURN ST_Transform(
    ST_Buffer(
        ST_Transform(
            ST_SetSRID(
				ST_MakePoint(lon, lat),
				4326), -- longitude,latitude
            3857), -- spherical mercator
        meters),
    4326); -- back to latitude, longitude
END;
$$ language plpgsql;

SELECT buffer_meters(-73.97854, 40.75364, 200);