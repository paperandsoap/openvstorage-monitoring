# Logstash

Logstash is a redis consumer that will read log messages from redis and put them into elasticsearch.

## Configuration

You'll find the configuration in _/etc/logstash/_. There are 2 main parts in the logstash configuration: logstash itself and OVS patterns. The patterns are regular expressions to match dates, timestamps and application names.

The following commands might come in handy:

```
service logstash status
service logstash start
service logstash stop
```

Logstash's log files is located in: _/var/log/logstash/_

## Sources

* https://www.elastic.co/products/logstash