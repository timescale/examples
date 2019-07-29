"""airquality_ingest.py

Assumes the schema as specified in schema.sql.
"""

import requests
import time
import datetime
import psycopg2
from pgcopy import CopyManager

URL_CITIES = "https://api.openaq.org/v1/locations"
URL_MEASUREMENTS = "https://api.openaq.org/v1/measurements"
# WARNING: in the real world, make this an environment variable
CONNECTION = "host=localhost dbname=airquality user=postgres"
POLL_INTERVAL = 300
# Make global dicts to cache meta data
measurements_dict = {}
locations_dict = {}

# Make the actual API request
def make_request(url, params):
    r = requests.get(url, params=params)
    # If no valid reponse from the API, print error and retry
    while not r:
        print("API is not returning a 200 response")
        time.sleep(5)
        r = requests.get(url, params=params)
    return r

# Iterate through paginated API responses
def iterate_request(url, params):
    r = make_request(url, params)
    meta = r.json()['meta']
    num_pages = int(meta['found'] / meta['limit'] + 1)
    dataset = r.json()['results']
    for i in range(2, num_pages+1):
        params['page'] = i
        r = make_request(url, params)
        print("Requesting page " + str(i) + " of " + str(num_pages) + " from API")
        dataset = dataset + r.json()['results']
    return dataset

# Parse all measurements from dataset returned by iterate_request
def parse_measurements(country_name, conn):
    url = URL_MEASUREMENTS
    params = {}
    params['limit'] = 10000
    params['country'] = country_name
    dataset = iterate_request(url, params)
    request = list()
    for entry in dataset:
        parameter = entry['parameter']
        unit = entry['unit']
        parameter_id = 0
        measurements_cache_result = measurements_dict.get(parameter)
        # Measurement found in cached dict, so use the associated measurement_id
        if measurements_cache_result:
            parameter_id = measurements_cache_result[0]
            print("Found "+ str(parameter_id) +" in measurements cache")
        # Measurement not found in cached dict, so need to update metadata table
        else:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO measurement_types (parameter, unit) VALUES (%s, %s) ON CONFLICT DO NOTHING", (parameter, unit))
                conn.commit()
                cursor.execute("SELECT * FROM measurement_types WHERE parameter = %s AND unit = %s", (parameter, unit))
                parameter_id = cursor.fetchall()[0][0]
                cursor.close()
                measurements_dict[parameter] = [parameter_id, unit]
                print("Updated measurements cache")
            except (Exception, psycopg2.Error) as error:
                print("Error thrown while trying to update measurement_types table")
        city_name = entry['city']
        location_name = entry['location']
        city_and_location = city_name + ' ' + location_name
        location_id = 0
        locations_cache_result = locations_dict.get(city_and_location)
        # Location found in cached dict, so use the associated city_id
        if locations_cache_result:
            location_id = locations_cache_result
            print("Found "+ str(location_id) +" in locations cache")
        # Location not found in cached dict, so need to update metadata table
        else:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO locations (city_name, location_name, country_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (city_name, location_name, country_name))
                conn.commit()
                cursor.execute("SELECT * FROM locations WHERE city_name = %s AND location_name = %s AND country_name = %s", (city_name, location_name, country_name))
                location_id = cursor.fetchall()[0][0]
                cursor.close()
                locations_dict[city_and_location] = location_id
                print("Updated locations cache")
            except (Exception, psycopg2.Error) as error:
                print("Error thrown while trying to update measurement_types table")
        timestamp = datetime.datetime.strptime(entry['date']['utc'],'%Y-%m-%dT%H:%M:%S.%fZ')
        value = entry['value']
        request.append((timestamp,parameter_id,location_id, value))
    cols = ('time', 'parameter_id', 'location_id','value')
    mgr = CopyManager(conn, 'measurements', cols)
    mgr.copy(request)
    conn.commit()

if __name__ == "__main__":
    # Populate dict variables when program initialized
    measurements_dict = {}
    locations_dict = {}
    with psycopg2.connect(CONNECTION) as conn:
        # Populate dict variables when program is initialized
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM measurement_types")
            for row in cursor.fetchall():
                measurements_dict[row[1]] = [row[0], row[2]]
            cursor.execute("SELECT * FROM locations")
            for row in cursor.fetchall():
                locations_dict[row[1]+' '+row[3]] = row[0]
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error thrown while trying to populate cache")
        print("Finished populating cache")
        while True:
            parse_measurements('GB', conn)
            print("SLEEPING FOR " + str(POLL_INTERVAL))
            time.sleep(POLL_INTERVAL)
