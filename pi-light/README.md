# Raspberry Pi Light Sensor

This example will read data from a light sensor (wired to a Raspberry Pi device) and send that
data to a TimescaleDB instance (hosted by [Timescale Cloud](https://www.timescale.com/cloud)).

## Contents

A brief overview of the files in this directory and how they're used:

* `photoresistor.py`: Python script to read sensor values and insert them into TimescaleDB.
* `pi-schema.sql`: data definition (DDL) to create the necessary hypertables.
* `grafana.json`: Grafana dashboard configuration.
* `pi_photoresistor.service`: systemd service definition to ensure the sensor is restarted on reboot.

## The Cloud ([Timescale Cloud](https://www.timescale.com/cloud))

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

    > The `photoresistor.py` script assumes that you're implementing a pull-down resistor on GPIO pin 23. You'll
    need to modify this depending on the specifics of your own sensor configuration.

Copy systemd started setup in place

    scp ./pi_photoresistor.service /etc/systemd/system

    > Be sure to set the TIMESCALEDB_CONNECTION string to your Service URI "postgres://..." for your TimescaleDB instance.

On device, start the service

    sudo systemctl start pi_photoresistor.service
