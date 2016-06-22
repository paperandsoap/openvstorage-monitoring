# What if you have 1 node for multiple roles?

Suppose you want to install redis, check_mk master, elk stack and grafana on one operation node.

An example will clarify:

inventory:
```
# file: inventory

[operation]
ops01 ansible_host=<ip>

[check_mk_master]

[check_mk_slaves]

[monitoring:children]
check_mk_master
check_mk_slaves

[redis]

[grafana]

[elk]

[controllers]
ctl01 ansible_host=<ip>
ctl02 ansible_host=<ip>
ctl03 ansible_host=<ip>

[computenodes]
cmp01 ansible_host=<ip>
cmp02 ansible_host=<ip>

[storagenodes]
str01 ansible_host=<ip>
str02 ansible_host=<ip>
str03 ansible_host=<ip>
str04 ansible_host=<ip>

[volumedrivernodes]

[hyperconverged]

# cumulus switches
[switch]
```

operation_servers.yml:
```
---
# file: operation_servers.yml

- hosts: operation
  remote_user: root
  roles:
    - common
    - beaver
    - check_mk_agent
    - check_mk_master_server
    - redis
    - grafana
    - elk
    - statsmonkey
```

host_vars/ops01:
```
---
# file: host_vars/ops01

site: monitor
```

roles/redis/vars/main.yml:
```
---
# file: roles/redis/vars/main.yml

password: a_very_long_password
max_memory: 1024mb
max_memory_policy: allkeys-random
```

roles/check_mk_master_server/vars/main.yml:
```
---
# file: roles/check_mk_master_server/vars/main.yml

user: mysql_admin_user
password: mysql_very_long_admin_password
```

roles/elk/vars/main.yml:
```
---
# file: roles/elk/vars/main.yml

elk_logstash:
  version: 2.0
  pid_file: /var/run/logstash.pid
  redis_ip: 127.0.0.1
  redis_password: admin
  configs:
    - { src: logstash-input.conf.j2, dest: 100-input.conf }
    - { src: logstash-output.conf.j2, dest: 900-output.conf }
    - { src: logstash-ovs.conf.j2, dest: 500-ovs.conf }
    - { src: logstash-syslog.conf.j2, dest: 501-syslog.conf }
    - { src: logstash-redis.conf.j2, dest: 502-redis.conf }
    - { src: logstash-auth.conf.j2, dest: 503-auth.conf }
    - { src: logstash-kern.conf.j2, dest: 504-kern.conf }
    - { src: logstash-switchd.conf.j2, dest: 505-switchd.conf }
    - { src: logstash-libvirtd.conf.j2, dest: 506-libvirtd.conf }

  patterns:
    - { src: ovs-pattern.j2, dest: ovs}

elk_kibana:
  version: 4.4
  path: /opt/kibana
  port: 5601
```

roles/beaver/vars/main.yml
```
---
# file: roles/beaver/vars/main.yml

redis_url: redis://:a_very_long_password@127.0.0.1:6379
```

roles/grafana/vars/main.yml:
```
---
# file: roles/grafana/vars/main.yml

db_name: "statistics"
db_user: "grafana_user"
db_password: "grafana_user_password"
retention: "7d"
protocol: "https"
port: "443"
```

roles/statsmonkey/vars/main.yml
```
# file: roles/statsmonkey/vars/main.yml

transport: influxdb
host: <host>
port: 8086
database: <db_name>
user: grafana_user
password: grafana_user_password
plugins: /etc/statsmonkey/plugins
```

ansible command:
```
ansible-playbook -i inventory setup.yml --limit ops01 -u root -k
```