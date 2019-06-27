# Clients

Here is a list of client libraries and code examples to connect to a TimescaleDB instance.


| Language | Client | Download |
|---|---|---|
| Go | pq | https://github.com/lib/pq |
| [Java](#java) | JDBC Driver | https://jdbc.postgresql.org/ |
| [Node.js](#nodejs) | pg package | https://www.npmjs.com/package/pg |
| [Python](#python) | psycopg2 | https://pypi.org/project/psycopg2/ |


### Java

Include Maven dependency for PostgreSQL JDBC Driver

    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.2.0</version>
    </dependency>

Sample Java code here.

### Node.js

Install node-postgres [pg](https://www.npmjs.com/package/pg) package:

    npm install pg

Run the [sample](tsdb-node-client.js):

    node tsdb-node-client.js
    
    
### Python

Install Python PostgreSQL Database Adapter [psycopg]( http://initd.org/psycopg/) package:

   	pip install psycopg2

Run the [sample](tsdb-python-client.py):

    python tsdb-python-client.py
    