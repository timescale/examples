var pg = require('pg');

var config = {
    database: "defaultdb",
    host: "YOUR-SERVICE.a.timescaledb.io",
    password: "YOUR-PASSWORD",
    port: 26479,
    ssl: "require",
    user: "YOUR-USER",
};

var client = new pg.Client(config);

client.connect(function (err) {
    if (err)
        throw err;
    client.query('SELECT 1 AS value', [], function (err, result) {
        if (err)
            throw err;

        console.log(result.rows[0]);
        client.end(function (err) {
            if (err)
                throw err;
        });
    });
});