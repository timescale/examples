#!/usr/bin/env bash
python3 -m venv /tmp/env
source /tmp/env/bin/activate
python3 -m pip install protobuf
python3 -m pip install gtfs-realtime-bindings
python3 -m pip install -U requests psycopg2-binary
rm -f /build/lambda.zip
mkdir /tmp/staging
cd /tmp/staging
cp -r /tmp/env/lib/python3.7/site-packages/* .
cp -r /build/*.py .
zip -r /build/lambda.zip *
