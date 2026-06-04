# xike.xikeos Ansible Collection

Ansible Collection for managing **Xike (兮克) switches** with Cisco IOS-like CLI.

## Overview

This collection provides modules, connection plugins, and utilities for automating Xike Ethernet switches. Xike switches use a Cisco IOS-like CLI interface, making this collection compatible with many existing Ansible network automation patterns.

## Installation

### From Ansible Galaxy (once published)

```bash
ansible-galaxy collection install xike.xikeos
```

### From Source

```bash
git clone https://github.com/andy/xike-xikeos.git
cd xike-xikeos
ansible-galaxy collection build
ansible-galaxy collection install xike-xikeos-0.1.0.tar.gz
```

### From local development directory

```bash
ansible-galaxy collection install /path/to/xike-xikeos/
```

## Requirements

- Ansible >= 2.9
- Python >= 3.6

## Usage

### Inventory Example

```yaml
all:
  children:
    xike_switches:
      hosts:
        switch01:
          ansible_host: 192.168.1.100
          ansible_network_os: xike.xikeos
          ansible_user: admin
          ansible_password: secret
          ansible_connection: httpapi
```

### Playbook Example

```yaml
---
- name: Configure Xike Switch
  hosts: xike_switches
  gather_facts: no
  tasks:
    - name: Get switch facts
      xike.xikeos.xikeos_facts:
        gather_subset:
          - interfaces
          - vlans

    - name: Display interface information
      ansible.builtin.debug:
        var: ansible_facts.net_interfaces
```

## Modules

| Module | Description |
|--------|-------------|
| `xikeos_facts` | Gather facts from Xike switches |
| `xikeos_config` | Manage device configuration |
| `xikeos_command` | Run commands on Xike switches |

## Connection Plugin

The collection includes a connection plugin for Xike switches that communicates via SSH with the IOS-like CLI.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/andy/xike-xikeos).

## License

MIT
