# *_servers.yml

Each \*_servers.yml contains the hosts, remote_user and roles variables.

**hosts** variable is the host group(s) where this playbook will be used for.

**remote_user** is the remote user who will run all the tasks from the playbook.

**roles** each group have their own roles.

For example compute_servers.yml. This playbook is used by the computenodes.
The external user is root and we want to install the common tasks, beaver, check_mk_agent, health check and statsmonkey.

```
---
# file: compute_servers.yml

- hosts: computenodes
  remote_user: root
  roles:
    - common
    - beaver
    - check_mk_agent
    - health_check
    - statsmonkey
```