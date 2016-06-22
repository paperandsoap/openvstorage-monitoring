# Beaver

Beaver is a python deamon that munches on logs and sends their content to a chosen target. In our case, this target is logstash via a redis queue.

## Configuration

You can find the configuration file in _/etc/beaver/beaver.conf_. An example:

```
[beaver]
transport: redis
redis_url: redis://172.19.10.15:6379
redis_namespace: logs
logstash_version: 1

[/var/log/rabbitmq/*.log]
multiline_regex_before = ^[^=].*
ignore_empty: 1
type: rabbitmq

[/var/log/ovs/*.log]
multiline_regex_before = ^[^\d{4}/\d{2}/\d{1,2}].*
ignore_empty: 1
exclude: (arakoon|extensions|audit_trails|storagerouterclient|support|celery|lib)
type: ovs

[/var/log/ovs/{arakoon,extensions,audit_trails,support,celery,lib}.log]
multiline_regex_before = ^[^\d{4}\-\d{2}\-\d{1,2}].*
ignore_empty: 1
type: ovs2

[var/log/ovs/storagerouterclient.log]
multiline_regex_before = ^[^\d{4}/\d{2}/\d{1,2}].*
ignore_empty: 1
type: ovs3

[/var/log/arakoon/*/*.log]
multiline_regex_before = ^[^\d{4}/\d{2}/\d{1,2}].*
ignore_empty: 1
type: ovs

[/var/log/upstart/*.log]
multiline_regex_before = ^[^\d{4}/\d{2}/\d{1,2}].*
ignore_empty: 1
exclude: (ovs-arakoon*|ovs-scheduled-tasks|ovs-workers)
type: ovs

[/var/log/upstart/{ovs-scheduled-tasks,ovs-workers}.log]
multiline_regex_before = ^[^\[\d{4}/\d{2}/\d{1,2}\]].*
ignore_empty:1
type: ovs4

[/var/log/upstart/ovs-arakoon*.log]
type: ovs-arakoon

[/var/log/kern.log]
type: kern

[/var/log/syslog]
type: syslog

[/var/log/auth.log]
type: auth

[/var/log/libvirt/*.log]
type: libvirtd

[/var/log/nginx/error.log]
type: other
```

The configuration file is quite self-explanatory. The following commands might come in handy:

```
service beaver status
service beaver start
service beaver stop
```

Beaver itself also has a log file: /var/log/beaver/logstash_beaver.log

## Sources

* https://github.com/python-beaver/python-beaver