# group_vars

**No changes are needed on the group vars**

Each group will have there own beaver config, statsmonkey group and plugins.

For example the controller group uses the beaver_ctl.conf.j2 config file, group name is ctl and the plugin host_data.

```
---
# file: group_vars/ctl

beaver_conf: beaver_ctl.conf.j2
statsmonkey_group: ctl
statsmonkey_plugins:
   - host_data
```