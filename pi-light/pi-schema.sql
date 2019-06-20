CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE pi_obs(
  time timestamptz,
  metric text,
  value numeric);
  
SELECT create_hypertable('pi_obs', 'time', chunk_time_interval=>'1 week');
