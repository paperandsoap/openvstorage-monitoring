# Statsmonkey

Statsmonkey is a internally written script which gathers statistics from various OVS components and puts them into an InfluxDB. It consists of 2 parts:

* Environment-wide statistics
* Host-specific statistics

## Configuration

The default configuration file for statsmonkey can be found in _/etc/statsmonkey/statsmonkey.conf_:

```
[statsmonkey]
transport: influxdb
host: 10.100.197.106
port: 8086
group: gph
database: statistics
user: admin
password: admin                                                                                       
plugins: /etc/statsmonkey/plugins
```

There is also an option to let statsmonkey send the statistics via redis. In that case, chance transport to 'redis'.

## Environment-wide statistics

One part of statsmonkey has been written as a celery scheduled task executed by celery beat. This way the script will be executed on a regular basis on a random node in the cluster. The celery-part of statsmonkey will use the framework to gather as much information as possible about the environment's components:

* Backend status and size
* vDisk statistics
* Disk status and safety
* vPool statistics

By default, statistics are gathered every minute.

## Host-specific statistics

As the celery tasks can be executed on a different node each time it's executed, we need a 2nd way to gather statistics for all host-specific statistics:

* Memory and CPU usage
* Network throughput
* Alba proxy status

For these metrics, a cronjob is installed which will execute statsmonkey.py every minute. Statsmonkey has been written in such a way that all scripts are loaded as plugins. All you need to do is drop the plugin in the correct directory and let it spit out the data in the correct format. The correct format (JSON) looks like this:

```
[
    {
        "tags": {"server": "hostname01"},
        "measurement": "host_stats",
        "fields": {
            "swap_used": 0,
            "packets_sent": 121972902, 
            "packets_recv": 166987953, 
            "bytes_recv": 62985734466, 
            "cpu_percent": 5.7, 
            "mem_free": 1123221504, 
            "swap_free": 0, 
            "bytes_sent": 13665266017, 
            "errout": 0, 
            "mem_used": 7249801216, 
            "mem_free_perc": 28.5, 
            "swap_free_perc": 0.0,
            "errin": 0}
    }
]
```

You can specify a number of tags to differentiate on which object/server/application the measurements apply. The 'measurement' field specifiec in which 'table' in influxdb your results will end up. The 'fields' will be the columns for that table. You can repeat JSON-arrays to send more statistics in 1 go.

# Sources

* https://github.com/openvstorage/openvstorage-monitoring/tree/master/roles/statsmonkey