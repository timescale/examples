/* Enable the TimscaleDB extension */
CREATE EXTENSION IF NOT EXISTS timescaledb;

/* 
Turn the 'stocks2' table into a hypertable.
This is important to be able to make use of TimescaleDB features later on.
*/
SELECT create_hypertable('stocks2', 'stock_datetime');