# host_vars

After you've configured the inventory file, you need to define some host vars. Host vars are only used for the Check_MK hosts (master and slaves). In the directory host_vars, you need to create a file with the same name as your Check_MK hostname defined in the inventory file.

An example will clarify:

inventory:
```
[check_mk_master]
mon01 ansible_host=<ip>

[check_mk_slaves]
mon02 ansible_host=<ip>
```

host_vars' directory structure:
```
├── host_vars
│   ├── mon01
│   └── mon02
```

When you configure the host vars for the master Check_MK node you need to add a site variable. The site variable is used to browse to the correct Check_MK agent.

Example: http://mon01_ip/monitor/
```
---
# file: host_vars/mon01

site: monitor
```

The slave check node needs 3 variables: site, location and livestatus_port. If you want 2 Check_MKs on the same node you need to change the default livestatus port (6557) to another one. The site variable is used to browse to the correct Check_MK agent.

Example: http://mon02_ip/slave/
```
---
# file: host_vars/mon02

site: slave
location: Europe
livestatus_port: 6557
```