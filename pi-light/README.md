Hello World...I have seen the light.


## The Cloud (Timescale Cloud)

Prepare TimescaleDB instance by creating the schema

    psql -h placeholder.timescaledb.op -d demopi -U pi -p 5432 -a -q -f ./schema.sql


## The Edge (Raspberry Pi)

On device, install [PostgreSQL Database Adapter](https://github.com/psycopg/psycopg2) for python

    sudo apt-get install libpq-dev
    pip3 install psycopg2

On device, install [CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) libraries

    pip3 install adafruit-blinka
    
Copy python script to device

    scp ./photoresistor.py pi@10.0.1.14:/home/pi


