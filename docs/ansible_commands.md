# Ansible commands

Some usefull ansible commands to deploy the ovs monitoring.

Install the common package:
```
ansible-playbook -i inventory setup.yml --tags common -u root -k
```

Once you exchanged your root ssh-keys to the server you no longer needs the *-u root -k* option.

Install all the packages:
```
ansible-playbook -i inventory setup.yml -u root -k
```

Install health_check package on the controller nodes:
```
ansible-playbook -i inventory setup.yml --tags health_check --limit controllers -u root -k
```