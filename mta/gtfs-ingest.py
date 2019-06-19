#!/usr/bin/env python
"""gtfs-ingest.py

Load a GTFS feed into a PostgreSQL database with PostGIS and TimescaleDB.

Assumes the schema:

    CREATE TABLE mta (
        vid text,
        time timestamptz,
        route_id text,
        bearing numeric,
        geom geometry(POINT, 4326));

and converted to a TimescaleDB hypertable. 

    SELECT create_hypertable('mta', 'time');

example GTFS entity

    id: "MTABC_6048"
    vehicle {
      trip {
        trip_id: "22504538-LGPA9-LG_A9-Weekday-10"
        start_date: "20190108"
        route_id: "Q53+"
        direction_id: 0
      }
      position {
        latitude: 40.71529006958008
        longitude: -73.8602294921875
        bearing: 134.45303344726562
      }
      timestamp: 1547004538
      stop_id: "553375"
      vehicle {
        id: "MTABC_6048"
      }
    }

Full spec https://github.com/google/transit/blob/master/gtfs-realtime/spec/en/reference.md#element-index
"""

from datetime import timedelta, datetime
import time
import os

from google.transit import gtfs_realtime_pb2 as gtfs
import requests
import requests_cache
import psycopg2
from psycopg2.extras import execute_values


def parse_vehicles(feed):
    """Given a GTFS feed, return a generator of 5-element tuples,
    each matching the following insert statement

    INSERT INTO mta (vid, time, route_id, bearing, geom)
    VALUES  (...);
    """

    for entity in list(feed.entity):
        value = datetime.fromtimestamp(entity.vehicle.timestamp)
        timestamp = value.strftime('%d %B %Y %H:%M:%S')
        yield (
            entity.id,
            timestamp,
            entity.vehicle.trip.route_id,
            entity.vehicle.position.bearing,
            "SRID=4326;POINT( %f %f )" % (
                entity.vehicle.position.longitude,
                entity.vehicle.position.latitude))


# Required Environment Variables
API_KEY = os.environ['MTA_API_KEY']
CONNECTION = os.environ['MTA_CONNECTION']

# Global config
# Using http://bustime.mta.info/wiki/Developers/Index
URL = f"http://gtfsrt.prod.obanyc.com/vehiclePositions?key={API_KEY}"
POLLING_INTERVAL = 85  # seconds
requests_cache.install_cache('.gtfs-cache', expire_after=timedelta(seconds=POLLING_INTERVAL))


if __name__ == "__main__":
    with psycopg2.connect(CONNECTION) as conn:
        while True:
            with conn.cursor() as cursor:
                response = requests.get(URL)
                feed = gtfs.FeedMessage()
                feed.ParseFromString(response.content)

                # performant way to batch inserts
                # see http://initd.org/psycopg/docs/extras.html#psycopg2.extras.execute_batch
                start = time.time()
                execute_values(
                    cursor,
                    "INSERT INTO mta (vid, time, route_id, bearing, geom)"
                    "VALUES %s", parse_vehicles(feed))
                conn.commit()
                end = time.time()

                nrows = len(feed.entity)
                print(f"INSERTED {nrows} rows at {end}, (elapsed: {end - start})")
                time.sleep(POLLING_INTERVAL)
