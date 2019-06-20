#!/usr/bin/env python3
from datetime import datetime
import time
import os

from digitalio import DigitalInOut, Direction
from psycopg2.extras import execute_values
import board
import psycopg2

print("Collecting sensor data...")

"""
Description:
make a postgres connection and talk to a GPIO pin
Loop forever:
    Loop for one second:
        sleep for 99ms
        reset pin and see how long it takes to fill up
        repeat
    Insert one second worth of raw data.
"""

connection_string = os.environ.get("TIMESCALEDB_CONNECTION", default="dbname=pi user=pi")

with psycopg2.connect(connection_string) as conn:
    with conn.cursor() as cur:
        with DigitalInOut(board.D23) as pin:
            while True:
                start = time.time()
                values = []
                while time.time() - start < 1.0:
                    time.sleep(0.099)
                    pin.direction = Direction.OUTPUT
                    pin.value = False
                    pin.direction = Direction.INPUT
                    reading = 0
                    while pin.value is False:
                        reading += 1
                    values.append((datetime.utcnow(), "photoresistor", reading))

                execute_values(
                    cur,
                    """
                    INSERT INTO pi_obs (time, metric, value)
                    VALUES %s
                    """,
                    values,
                )
                conn.commit()
                print("Inserted ", len(values))
