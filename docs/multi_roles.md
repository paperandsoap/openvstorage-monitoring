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

ops_servers.yml:
```
---
# file: ops_servers.yml

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
  redis_ip: 127.0.0.1
  redis_password: a_very_long_password
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

ansible command:
```
ansible-playbook -i inventory setup.yml --limit ops01 -u root -k
```