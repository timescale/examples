# Air Quality Collection - Sample Application

This folder contains a sample application that demonstrates how users might choose
to collect air quality information. We leverage the Open AQ Platform API (https://docs.openaq.org/)
to collect and store data in TimescaleDB.

## Requirements
- A working instance of TimescaleDB 1.4
- Python3 environment

## Getting Started
1. Update airquality_ingest.py with your TimescaleDB connection string
2. Install necessary packages as listed in requirements.txt
3. Initialize your TimescaleDB database with the schemas specified in `schema.sql`
4. Run `python airquality_ingest.py`
