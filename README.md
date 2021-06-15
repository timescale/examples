# Example Applications

TimescaleDB.

| Example | Type | Description |
|---|---|---|
| [Crypto Tutorial](https://github.com/timescale/examples/tree/master/crypto_tutorial) | Financial | Sample code and dataset for analyzing cryptocurrency market data|

#### Ingest

- [Kafka](https://streamsets.com/blog/ingesting-data-apache-kafka-timescaledb/)
- [Telegraf](https://docs.timescale.com/latest/tutorials/telegraf-output-plugin)
- [Netdata](https://github.com/mahlonsmith/netdata-timescale-relay)

#### Visualization

- [Grafana](https://docs.timescale.com/latest/using-timescaledb/visualizing-data#grafana)
- [Seeq](https://seeq12.atlassian.net/wiki/spaces/KB/pages/376963207/SQL+Connection+Configuration#SQLConnectionConfiguration-TimescaleDB)
- [Tableau, PowerBI, Others](https://docs.timescale.com/latest/using-timescaledb/visualizing-data#other-viz-tools)

#### Monitoring

- [Prometheus](https://docs.timescale.com/latest/tutorials/prometheus-adapter)
- [Zabbix](https://support.zabbix.com/browse/ZBXNEXT-4868)

# Building application

- install timeScaleDB (postres)
$ brew tap timescale/tap
$ brew install timescaledb
- git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
- sudo chown -R $(whoami) /usr/local/include
$ /usr/local/bin/timescaledb_move.sh
$ timescaledb-tune (y,y,y,y,y,y,y)
# Restart PostgreSQL instance
$ brew services restart postgresql

# Add a superuser postgres:
$ createuser postgres -s

# Check psql version
$ psql --version

# Connect to postres
$ psql -h HOSTNAME -p PORT -U USERNAME -W -d DATABASENAME
# Commands
$ psql **command**
\l	List available databases
\c dbname	Connect to a new database
\dt	List available tables
\d tablename	Describe the details of given table
\dn	List all schemas in the current database
\df	List functions in the current database
\h	Get help on syntax of SQL commands
\?	Lists all psql slash commands
\set	System variables list
\timing	Shows how long a query took to execute
\x	Show expanded query results
\q	Quit psql

# Tutorial 
https://www.youtube.com/watch?v=MFudksxlZjk
https://docs.timescale.com/timescaledb/latest/how-to-guides/connecting/psql/#common-psql-commands

