# Fortigate Python API token generator

This project aim to help system and network administrators in Fortigate firewall configuration automation.

Indeed, to fully automate the deployment of a new Fortigate device, the creation of an API admin token is necessary. This script use python paramiko to do the first power on configuration : 

1. Changing the default password
2. Create an API token (API Administrator and API profile)
3. Upgrade the firmware

 After these step, the fortigate API could be used to do the rest of the configuration.

# Roadmap

- Improve the upgrade method
- Possibility to choose what kind of token create (Read-Only or Read-Write)
 
