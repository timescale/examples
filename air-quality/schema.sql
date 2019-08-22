CREATE DATABASE airquality;

\c airquality

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE measurement_types (
  parameter_id SERIAL PRIMARY KEY,
  parameter TEXT NOT NULL,
  unit TEXT NOT NULL,
  UNIQUE(parameter, unit)
);

CREATE TABLE locations (
  location_id SERIAL PRIMARY KEY,
  city_name TEXT NOT NULL,
  country_name TEXT NOT NULL,
  location_name TEXT NOT NULL,
  UNIQUE(city_name, location_name, country_name)
);

CREATE TABLE measurements (
  time TIMESTAMPTZ,
  parameter_id INTEGER REFERENCES measurement_types(parameter_id),
  location_id INTEGER REFERENCES locations(location_id),
  value FLOAT
);

CREATE TABLE temp_measurements (
  time TIMESTAMPTZ,
  parameter_id INTEGER REFERENCES measurement_types(parameter_id),
  location_id INTEGER REFERENCES locations(location_id),
  value FLOAT
);

SELECT create_hypertable('measurements', 'time');
