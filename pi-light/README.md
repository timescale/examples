# Raspberry Pi Light Sensor

This example will read data from a light sensor (wired to a Raspberry Pi device) and send that
data to a TimescaleDB instance (hosted by Timescale Cloud). 

## The Cloud (Timescale Cloud)

Prepare TimescaleDB instance by creating the pi schema

    psql postgres://USERNAME:PASSWORD@HOST:PORT/defaultdb?sslmode=require -f ./pi-schema.sql

Prepare Grafana instance by creating a datasource

   Login to Grafana > Configuration > Data Sources > Add data source > PostgreSQL

Create Grafana dashboard

   Login to Grafana > Dashboard > Import > ./grafana.json

## The Edge (Raspberry Pi)

On device, install [PostgreSQL Database Adapter](https://github.com/psycopg/psycopg2) for python

    sudo apt-get install libpq-dev
    pip3 install psycopg2

On device, install [CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) libraries

    pip3 install adafruit-blinka
    
Copy python script to device

    scp ./photoresistor.py pi@10.0.1.14:/home/pi

Copy systemd started setup in place (be sure to set the TIMESCALEDB_CONNECTION string to reach your TimescaleDB instance)

    scp ./pi_photoresistor.service /etc/systemd/system
    
On device, start the service

    sudo systemctl start pi_photoresistor.service
