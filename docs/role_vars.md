# Vars

In the vars directory you need to change the variables. Example:

```
---
# file: roles/grafana/vars/main.yml

db_name: "statistics"
db_user: "grafana"
db_password: "grafana"
retention: "7d"
protocol: "https"
port: "443"
```

You can choose 2 transport layers for Statsmonkey: Redis or InfluxDB.

If you want to configure with Redis your statsmonkey/vars/main.yml will look like:

```
---
# file: roles/statsmonkey/vars/main.yml

transport: redis
host: <host>
port: 6379
database: <db_name>
password: <redis_password>
plugins: /etc/statsmonkey/plugins
```

For InfluxDB:

```
---
# file: roles/statsmonkey/vars/main.yml

transport: influxdb
host: <host>
port: 8086
database: <db_name>
user: <influxdb_username>
password: <influxdb_password>
plugins: /etc/statsmonkey/plugins
```