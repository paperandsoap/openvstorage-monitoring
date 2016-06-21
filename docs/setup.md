# Setup.yml

Setup.yml contains all the playbooks, ops_servers.yml, monitor_servers.yml,....

```
---
# file: setup.yml

- include: ops_servers.yml
- include: monitor_servers.yml
- include: controller_servers.yml
- include: compute_servers.yml
- include: storage_servers.yml
- include: hyperconverged_servers.yml
- include: data_servers.yml
- include: graph_servers.yml
- include: elk_servers.yml
- include: switches.yml
```