# Inventory

**Do not delete or edit the group names (the sections in brackets).**

Ansible works against multiple systems in your infrastructure at the same time. It does so by selecting hosts listed inside Ansible’s inventory file.

This is the template of the inventory file:

```
# file: inventory

[operation]
ops01 ansible_host=<ip>

[check_mk_master]
mon01 ansible_host=<ip>

[check_mk_slaves]
mon02 ansible_host=<ip>

[monitoring:children]
check_mk_master
check_mk_slaves

[redis]
red01 ansible_host=<ip>

[grafana]
gra01 ansible_host=<ip>

[elk]
elk01 ansible_host=<ip>

# hyperscale environment
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

# only used when you have an accelerated backend
[volumedrivernodes]
perf01 ansible_host=<ip>

# hyperconverged environment
[hyperconverged]
node01 ansible_host=<ip>
node02 ansible_host=<ip>
node03 ansible_host=<ip>

# cumulus switches
[switch]
sw01 ansible_host=<ip>
sw02 ansible_host=<ip>
```

**operation** group: Define the deployment node of your setup. min 0, max infinity.
**check_mk_master** group: Define the master check mk node. min 0, max 1 node.
**check_mk_slaves** group: Define the slaves check mk nodes. min 0, max infinity.
**monitoring** group: Parent group from the check mk nodes.
**redis** group: Define the redis node(s). Redis-ha with sentinel is not implemented. min 1, max infinity.
**grafana** group: Define the grafana node. min 0, max infinity.
**elk** group: Define the elk stack. min 0, max infinity. Elk stack cluster not implemented.

## Hyperscale settings
**controllers** group: Define the ovs controllers. min 3, max 3.
**computenodes** group: Define the ovs compute nodes. min 0, max infinity.
**storagenodes** group: Define the ovs storage nodes. min 1, max infinity.

## Hyperscale with accelerated backend settings
**controllers** group: Define the ovs controllers. min 3, max 3.
**computenodes** group: Define the ovs compute nodes. min 0, max infinity.
**storagenodes** group: Define the ovs storage nodes. min 1, max infinity.
**volumedrivernodes** group: Define the volumedriver nodes. min 1, max infinity.

## Hyperconverged settings
**hyperconverged** group: Define the hyperconverged nodes. min 3, max infinity.