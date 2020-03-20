# Example Dashboards for to get started analyzing Prometheus metrics using Timescale and Grafana

### Context and Intended Use

These sample dashboards are from this [tutorial](https://docs.timescale.com/latest/tutorials/tutorial-use-timescale-prometheus-grafana) on how to use Grafana and Timescale to analyze Prometheus metrics from a PostgreSQL database. The tutorial details step by step how to build each sort of visualization. These two sample dashboards are intended to give you (1) a starting point and code recipies for building your own dashboards which visualize Prometheus metrics from your infrastructure and (2) some sample code, recipies and ideas for useful visualizations when monitoring a database instance with Prometheus.

### Short Term Monitoring

This file (shortterm-monitoring.json) contains dashboards to monitor metrics for the short term.

### Long Term Monitoring

This file (longterm-monitoring.json) contains dashboards to monitor metrics for the long term, using Timescale's Continuous Aggregates feature.

### How to upload to Grafana

For each file:
1. Create a new Grafana dashboard
2. Copy and paste the JSON from the file and save the dashboard
3. You should see several panels created, but all of them complaining of no data
4.1 Follow [this tutorial](https://docs.timescale.com/latest/tutorials/tutorial-setup-timescale-prometheus) to setup a monitoring system to create data to populate your dashboards.
4.2 Alternatively, you can follow [this tutorial](https://docs.timescale.com/latest/tutorials/tutorial-use-timescale-prometheus-grafana) and download the sample prometheus metrics dataset at the start of the tutorial.

### Note about metric ids

Note that the metric IDs may be different for your postgreSQL database, there will be a chance they won't match the IDs used to create the dashboard. Should this occur, find the correct ID and substitute it into the query
