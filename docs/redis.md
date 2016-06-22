# Redis

Redis is an open source in-memory data structure store. We'll be using it as a message broker. Redis is basically a queue where log file messages are being put in on one end by beaver and are being popped out on the other end by logstash.

## Configuration

You can find the Redis configuration file in _/etc/redis/redis.conf_. We're running redis with the default configuration, except for 3 parameters:

* requirepass: a password chosen by you
* maxmemory: the maximum amount of  (eg: 3072mb)
* max_memory_policy: the policy on how redis should respond when maxmemory is reached. We recommend allkeys-random

The following commands might come in handy:

```
service redis-server status
service redis-server start
service redis-server stop
```

You can find the log file at _/var/log/redis/redis-server.log_.

## Sources

* http://redis.io/