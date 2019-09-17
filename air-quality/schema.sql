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

-- Continuous Aggregates Example

CREATE VIEW measurements_15min
WITH (timescaledb.continuous)
AS
SELECT
  time_bucket('15 minute', time) as bucket,
  parameter_id,
  avg(value) as avg,
  max(value) as max,
  min(value) as min
FROM
  measurements
GROUP BY bucket, parameter_id;

CREATE VIEW measurements_hourly
WITH (timescaledb.continuous)
AS
SELECT
  time_bucket('1 hour', time) as bucket,
  parameter_id,
  avg(value) as avg,
  max(value) as max,
  min(value) as min
FROM
  measurements
GROUP BY bucket, parameter_id;

CREATE VIEW measurements_daily
WITH (timescaledb.continuous)
AS
SELECT
  time_bucket('1 day', time) as bucket,
  parameter_id,
  avg(value) as avg,
  max(value) as max,
  min(value) as min
FROM
  measurements
GROUP BY bucket, parameter_id;

CREATE VIEW shorter_lag_daily
WITH (timescaledb.continuous, timescaledb.refresh_lag = '1 day', timescaledb.refresh_interval = '2 hour')
AS
SELECT
  time_bucket('1 day', time) as bucket,
  parameter_id,
  avg(value) as avg,
  max(value) as max,
  min(value) as min
FROM
  measurements
GROUP BY bucket, parameter_id;

CREATE VIEW no_lag_daily
WITH (timescaledb.continuous, timescaledb.refresh_lag = '- 1 day', timescaledb.refresh_interval = '2 hour')
AS
SELECT
  time_bucket('1 day', time) as bucket,
  parameter_id,
  avg(value) as avg,
  max(value) as max,
  min(value) as min
FROM
  measurements
GROUP BY bucket, parameter_id;
