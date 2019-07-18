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
"""

from datetime import timedelta, datetime
import time
import os

from google.transit import gtfs_realtime_pb2 as gtfs
import requests
import psycopg2
from psycopg2.extras import execute_values


# Required Environment Variables
API_KEY = os.environ['MTA_API_KEY']
CONNECTION = os.environ['MTA_CONNECTION']


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



# Global config
# Using http://bustime.mta.info/wiki/Developers/Index
URL = f"http://gtfsrt.prod.obanyc.com/vehiclePositions?key={API_KEY}"


def lambda_handler(event, context):
    with psycopg2.connect(CONNECTION) as conn:
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
            
    return {
        'statusCode': 200,
        'body': f"INSERTED {nrows} rows at {end}, (elapsed: {end - start})"
    }
