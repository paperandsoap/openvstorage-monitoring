# Grafana

Grafana is an open source time series based graphing tool.

## Configuration

Grafana's configuration can be found in _/etc/grafana/grafana.ini_. This configures the grafana server. The internal configuration of grafana however is stored into an SQLite database file located in _/var/lib/grafana/grafana.db_. Grafana has no API, but if you're clever enough, you can grasp through grafana's internal configuration structure to configure things without using the GUI.
 
The following commands might come in handy:

```
service grafana-server status
service grafana-server start
service grafana-server stop
```

Grafana's log file is located in _/var/log/grafana/grafana.log_.

## Screenshots

![Grafana-host_overview](images/host_overview.png "Host overview")
![Grafana-vdisk_overview](images/vdisk_overview.png "vDisk overview")

## Sources

* http://grafana.org/