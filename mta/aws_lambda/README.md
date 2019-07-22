# Deploying on AWS Lambda

This document describes how to create and package an AWS Lambda function
that will poll the MTA API once a minute and insert to a TimescaleDB hypertable.

AWS Lambda allows you to run "serverless" functions.
Lambda allows you to forget about server maintenance and scaling. In exchange,
you must package your entire application into a zip bundle according to the
compute environment you're using.

The MTA ingest script is written in python but several of the dependencies
rely on compiled C extensions. These must be compiled against compatible versions
of the AWS Lambda environment; 64-bit RHEL-based linux.

## Approach

1. Create a Docker image based on `amazonlinux` containing the build tools required.
2. Run the Docker container and install the python dependencies into a virtualenv.
3. Still within the docker container, package the contents of the virtualenv along with your python code into a zip file
4. Save zipfile to a mounted volume so that it persists on the host.
5. Upload the zipfile to s3
6. Configure recurring 1 minute trigger
7. Congigure required environment variables

## Details

The lambda function itself is slightly modified from the original ingest script.
Instead of looping indefinitely, it's refactored to run exactly once. The process gets restarted
periodically. See `build/lambda_function.py`

Steps 1-4 can be handled automatically with the Makefile system in this directory.
Running `make` will create the image and run the container, resulting in a zip file on your local machine.

Uploading the zipfile to s3 can be done with `aws s3 cp my.zip s3://bucket/my.zip`

The remaining configuration of the Lambda function is done through the AWS console.
