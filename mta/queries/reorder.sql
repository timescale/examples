-- Count of all observations for a given route
-- Impact of on-disk ordering, see "shared hit blocks" and "shared read blocks"
--
-- Note: already run
--   SELECT reorder_chunk('_timescaledb_internal._hyper_1_41_chunk', 'idx_mta_route_id');

-- explain (analyze, buffers)
SELECT count(1)
FROM mta
WHERE time between '2019-03-05 0:00' AND '2019-03-05 23:59'
AND route_id = 'S86';