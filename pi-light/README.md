Hello World...I have seen the light.


## The Edge

Load python script on Pi

    scp ./examples/pi-light/photoresistor.py pi@10.0.1.14:/tmp



## The Cloud

Prepare Database

    psql -h placeholder.timescaledb.op -d demopi -U pi -p 5432 -a -q -f ./schema.sql
