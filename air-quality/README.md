# Air Quality Collection - Sample Application

This folder contains a sample application that demonstrates how users might choose
to collect air quality information. We leverage the Open AQ Platform API (https://docs.openaq.org/)
to collect and store data in TimescaleDB.

## Requirements
- A working instance of [TimescaleDB](https://docs.timescale.com)
- Python3 environment
- Install python dependencies with `pip install -r requirements.txt`

## Content
The files in this directory and how they're used:

* `airquality_ingest.py`: Python script to read data from Open AQ Platform API and insert them into TimescaleDB.
* `schema.sql`: Data definition (DDL) to create the necessary tables & hypertables.
* `grafana.json`: Grafana dashboard configuration.
* `requirements.txt`: Python dependency requirements.
* `sample.json`: Sample json output from the Open AQ Platform API.

## Getting Started
0. Create a TimescaleDB and Grafana instance
1. Update `airquality_ingest.py` with your TimescaleDB connection string
2. Install necessary packages as listed in `requirements.txt`
3. Initialize your TimescaleDB database with the schemas specified in `schema.sql`
4. Run `python airquality_ingest.py` to start the ingestion
5. Create Grafana instance and import dashboard `Login to Grafana > Dashboard > Import > ./grafana.json`

