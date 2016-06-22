## Ansible structure

{% include "inventory.md" %}
{% include "host_vars.md" %}
{% include "group_vars.md" %}
{% include "setup.md" %}
{% include "servers.md" %}
{% include "roles.md" %}

### Example
```
├── inventory
├── setup.yml
├── compute_servers.yml
├── controller_servers.yml
├── elk_servers.yml
├── grafana_servers.yml
├── hyperconverged_servers.yml
├── monitor_servers.yml
├── operation_servers.yml
├── redis_servers.yml
├── storage_servers.yml
├── switches.yml
├── volumedriver_servers.yml
├── host_vars
│   ├── mon01
│   └── mon02
├── group_vars
│   ├── computenodes
│   ├── controllers
│   ├── elk
│   ├── grafana
│   ├── hyperconverged
│   ├── monitoring
│   ├── operation
│   ├── redis
│   ├── storagenodes
│   ├── switch
│   └── volumedrivernodes
├── roles
    ├── apache
    │   ├── files
    │   │   └── 000-default.conf
    │   └── tasks
    │       └── main.yml
    ├── beaver
    │   ├── files
    │   │   └── beaver.daemon
    │   ├── handlers
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   │   ├── beaver_cmp.conf.j2
    │   │   ├── beaver_ctl.conf.j2
    │   │   ├── beaver_gph.conf.j2
    │   │   ├── beaver_hyperconverged.conf.j2
    │   │   ├── beaver_mon.conf.j2
    │   │   ├── beaver_ops.conf.j2
    │   │   ├── beaver_red.conf.j2
    │   │   ├── beaver_str.conf.j2
    │   │   └── beaver_switch.conf.j2
    │   └── vars
    │       └── main.yml
    ├── check_mk_agent
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   ├── clientside
    │   │   │   ├── backend
    │   │   │   ├── healthcheck
    │   │   │   └── ovs_framework
    │   │   ├── snmpd.conf
    │   │   └── snmpd.rc
    │   └── tasks
    │       └── main.yml
    ├── check_mk_master_server
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   └── serverside
    │   │       ├── backend
    │   │       ├── filesystem
    │   │       ├── healthcheck
    │   │       ├── load
    │   │       ├── memory
    │   │       ├── ovs_framework
    │   │       └── process
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   │   └── my.conf
    │   └── vars
    │       └── main.yml
    ├── check_mk_slave_server
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   └── serverside
    │   │       ├── backend
    │   │       ├── filesystem
    │   │       ├── healthcheck
    │   │       ├── load
    │   │       ├── memory
    │   │       ├── ovs_framework
    │   │       └── process
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   │   └── my.conf
    │   └── vars
    │       └── main.yml
    ├── common
    │   └── tasks
    │       └── main.yml
    ├── elk
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   ├── elasticsearch-logrotate
    │   │   ├── kibana.json
    │   │   ├── kibana-logrotate
    │   │   └── logstash-logrotate
    │   ├── handlers
    │   │   └── main.yml
    │   ├── meta
    │   │   └── main.yml
    │   ├── tasks
    │   │   ├── elasticsearch.yml
    │   │   ├── java.yml
    │   │   ├── kibana.yml
    │   │   ├── logstash.yml
    │   │   └── main.yml
    │   ├── templates
    │   │   ├── 010_kibana.j2
    │   │   ├── elasticsearch-logging.yml.j2
    │   │   ├── elasticsearch.yml.j2
    │   │   ├── logstash-auth.conf.j2
    │   │   ├── logstash-input.conf.j2
    │   │   ├── logstash-kern.conf.j2
    │   │   ├── logstash-libvirtd.conf.j2
    │   │   ├── logstash-output.conf.j2
    │   │   ├── logstash-ovs.conf.j2
    │   │   ├── logstash-redis.conf.j2
    │   │   ├── logstash-switchd.conf.j2
    │   │   ├── logstash-syslog.conf.j2
    │   │   └── ovs-pattern.j2
    │   └── vars
    │       └── main.yml
    ├── grafana
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   └── grafana.db
    │   ├── handlers
    │   │   └── main.yml
    │   ├── meta
    │   │   └── main.yml
    │   ├── tasks
    │   │   ├── grafana.yml
    │   │   ├── influxdb.yml
    │   │   └── main.yml
    │   ├── templates
    │   │   ├── 001_grafana.j2
    │   │   ├── grafana.ini.j2
    │   │   └── influxdb.conf.j2
    │   └── vars
    │       └── main.yml
    ├── health_check
    │   ├── defaults
    │   │   └── main.yml
    │   └── tasks
    │       └── main.yml
    ├── redis
    │   ├── handlers
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   │   └── redis.conf.j2
    │   └── vars
    │       └── main.yml
    └── statsmonkey
        ├── files
        │   ├── alba_proxy_data
        │   ├── host_data
        │   ├── statsmonkey
        │   │   ├── __init__.py
        │   │   └── statsmonkey.py
        │   ├── statsmonkey-logs
        │   └── statsmonkeyscheduledtask.py
        ├── tasks
        │   └── main.yml
        ├── templates
        │   └── statsmonkey.conf.j2
        └── vars
            └── main.yml

```