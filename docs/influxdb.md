# InfluxDB

InfluxDB is an open source database specifically designed to handle time series data with high availability and high performance requirements. 

## Configuration

We're running quite the standard configuration which comes with the installation. You can find the configuration file in _/etc/influxdb/influxdb.conf_. 

The following commands might come in handy:

```
service influxdb status
service influxdb start
service influxdb stop
```

If you point your browser to http://<nodeip>:8083/ you can find the admin GUI of InfluxDB and you can execute raw queries onto the database.

Influxdb's log files is located in: _/var/log/influxdb/influxd.log_

## Sources

https://influxdata.com/