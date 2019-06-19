# MTA Bus Demo

This project is a demo implementation of a TimescaleDB-backed database to ingest and query real-time mass transit information from the New York Metropolitan Transportation Authority (MTA).

![img](./imgs/bus1.png)

## Installation

* Set up PostgreSQL with TimescaleDB and PostGIS extensions.
* Install Python 3.6
* Install python dependencies with `pip install -r requirements.txt`
  - Uses Google’s GTFS realtime protobuf spec and related python lib for parsing.
  - Uses psycopg2 batch inserts for efficiency.

## Usage

First, create the database, users and tables as required. See Data Model below.

Run `python3 gtfs-ingest.py` and the script will run indefinitely, polling the MTA data feed at
regular intervals and inserting the data into our table.

The deployment-specific variables must be set as environment variables. The required
variables are:

```bash
# Obtain a key from http://bustime.mta.info/wiki/Developers/Index
export MTA_API_KEY = 'abc-123'
export MTA_CONNECTION = "host=localhost dbname=mta user=mta"
python3 gtfs-ingest.py
```

## Dataset

We’ll be using the SIRI Real-Time API and the OneBusAway "Discovery" API provided by the MTA. See http://bustime.mta.info/wiki/Developers/Index for details.

This should be generalizable to other transit systems using the General Transit Feed Specification or GTFS (see https://developers.google.com/transit/gtfs-realtime/)


## Data Model

DDL:

```sql
CREATE EXTENSION timescaledb;
CREATE EXTENSION postgis;
CREATE TABLE mta (
    vid text,
    time timestamptz,
    route_id text,
    bearing numeric,
    geom geometry(POINT, 4326));

SELECT create_hypertable('mta', 'time');

CREATE INDEX idx_mta_geom ON mta USING GIST (geom);
CREATE INDEX idx_mta_route_id ON mta USING btree (route_id);
```

### spatial data

In order to answer certain questions, we need additional geographic data from the MTA defining the bus route.
The goal is to implement a traffic anomaly detection system capable of alerting stakeholders when any bus deviates from it’s scheduled route. This information could be used to detect traffic problems in nearly real time - useful to logistics, law enforcement and transportation planners to identify traffic situations or adjust routing strategies.

* download bus routes shapefile from http://web.mta.info/developers/developer-data-terms.html#data.
* Importing the MTA bus routes with a LineString geometry.

```bash
shp2pgsql -s 4326 "NYCT Bus Routes" public.bus_routes | psql -U mta -d mta -h localhost`
```

* Buffer the route line to get a polygon for each route to add a small margin of error for point location imprecision. (+/- 0.0002 decimal degrees or ~16 meters at 45N latitude)

```sql
CREATE TABLE route_geofences AS
  SELECT route_id,
         St_buffer(St_collect(geom), 0.0002) AS geom
  FROM   bus_routes
  GROUP  BY route_id;  
```

## Queries

### Example 1: Vehicles off-route in the last 15 minutes

```sql
--
-- Vehicles off-route in the last 15 minutes
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
AND NOT
  st_within(bus.geom, route.geom)
```

The red dots are observations not within the route in yellow.

![img](./imgs/bus2.png)

### Example 2: What bus routes pass near 100 6th Ave each hour?

```sql
--
-- What bus routes pass near 100 6th Ave each hour?
--
SELECT
    time_bucket_gapfill(
        '1 hour',
        time,
        '2019-01-20 09:00',
        '2019-01-25 09:00') as bucket,
    array_agg(distinct route_id) as nearby_routes
FROM
	mta
WHERE
	time between '2019-01-20 09:00' and '2019-01-25 09:00'
	AND
	-- Search within ~160 meters of this building
  st_dwithin('SRID=4326;POINT(-74.00482 40.7233)', mta.geom, 0.002)
GROUP BY
  bucket;
```

### Example 3:  What is the hourly bus traffic on the M100 route?

```sql
--
-- What is the hourly bus traffic on the M100 route?
--
SELECT
    time_bucket_gapfill(
        '1 hour',
        time,
        '2019-01-23 09:00',
        '2019-01-25 09:00') as bucket,
    coalesce(count(distinct vid), 0) as n_unique_vehicles
FROM
    mta
WHERE
    time between '2019-01-23 09:00' and '2019-01-25 09:00'
AND
    route_id = 'M100'
GROUP BY
    bucket;
```
