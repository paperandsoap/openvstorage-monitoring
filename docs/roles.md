# Roles

Roles in Ansible follow the idea of include files and transforms your configuration to clean and reusable abstractions.
They allow you to focus more on the big picture and only dive down into the details when needed.

OVS monitor roles:
```
apache
beaver
check_mk_agent
check_mk_master_server
check_mk_slave_server
common
elk
grafana
health_check
redis
statsmonkey
```

Each role has its own structure.
```
grafana
├── defaults
│   └── main.yml
├── files
│   └── grafana.db
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── tasks
│   ├── grafana.yml
│   ├── influxdb.yml
│   └── main.yml
├── templates
│   ├── 001_grafana.j2
│   ├── grafana.ini.j2
│   └── influxdb.conf.j2
└── vars
    └── main.yml

```

**defaults** are default variables.

**files** are files that will be copied to the node.

**handlers** are actions that are triggered by the playbook. (e.g.: restarting services)

**meta** are role dependencies that allows to automatically pull in other roles when using a role.

**tasks** are commands that are executed in order.

**templates** are processed by the Jinja2 templating language. (variables from the defaults or vars directory will be used)

**vars** are variables that you need to change.