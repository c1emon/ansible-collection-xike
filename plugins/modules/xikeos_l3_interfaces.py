#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS L3 Interfaces resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_l3_interfaces
short_description: Manage L3 interface (VLAN interface) IP configurations on Xike switches
version_added: "0.1.0"
description:
  - This module provides declarative management of Layer 3 VLAN interface
    IP configurations on Xike (兮克) switches.
  - Manages IPv4 and IPv6 addresses on VLAN interfaces.
  - Xike uses 'interface vlan-interface <id>' syntax (not 'interface Vlan<id>').
options:
  config:
    description: List of VLAN interface configurations
    type: list
    elements: dict
    suboptions:
      name:
        description: VLAN interface name (e.g., 'vlan-interface 1')
        type: str
        required: true
      ipv4:
        description: List of IPv4 addresses to configure
        type: list
        elements: dict
        suboptions:
          address:
            description: IPv4 address (e.g., '192.168.1.1')
            type: str
            required: true
          subnet_mask:
            description: Subnet mask (e.g., '255.255.255.0')
            type: str
            required: true
      ipv6:
        description: List of IPv6 addresses to configure
        type: list
        elements: dict
        suboptions:
          address:
            description: IPv6 address with prefix length (e.g., '2001:db8::1/64')
            type: str
            required: true
  state:
    description: Desired state of the configuration
    type: str
    default: merged
    choices: ['merged', 'replaced']
author: Andy
"""

EXAMPLES = """
- name: Configure IPv4 address on VLAN interface
  xike.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 100
        ipv4:
          - address: 192.168.100.1
            subnet_mask: 255.255.255.0
    state: merged

- name: Configure IPv4 and IPv6 on VLAN interface
  xike.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 1
        ipv4:
          - address: 10.0.0.1
            subnet_mask: 255.255.255.0
        ipv6:
          - address: 2001:db8::1/64
    state: merged

- name: Replace all L3 interface configs
  xike.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 10
        ipv4:
          - address: 172.16.0.1
            subnet_mask: 255.255.0.0
    state: replaced
"""

RETURN = """
before:
  description: The configuration prior to the module execution
  returned: when I(state) is C(merged) or C(replaced)
  type: dict
after:
  description: The configuration after the module execution
  returned: when I(state) is C(merged) or C(replaced)
  type: dict
commands:
  description: The set of commands pushed to the device
  returned: always
  type: list
  sample:
    - interface vlan-interface 100
    - ip address 192.168.100.1 255.255.255.0
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.l3_interfaces import (
        L3InterfacesFacts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def build_commands(config, existing_config):
    """Build CLI commands for a single interface config entry.

    Args:
        config: dict with 'name', 'ipv4', 'ipv6'
        existing_config: dict of current interface configs keyed by name

    Returns:
        list: CLI commands to apply
    """
    commands = []
    interface_name = config['name']
    existing = existing_config.get(interface_name, {'ipv4': [], 'ipv6': []})

    # Build desired state
    desired_ipv4 = config.get('ipv4') or []
    desired_ipv6 = config.get('ipv6') or []

    existing_ipv4 = existing.get('ipv4', [])
    existing_ipv6 = existing.get('ipv6', [])

    # Normalize for comparison
    desired_ipv4_set = {(a['address'], a['subnet_mask']) for a in desired_ipv4}
    existing_ipv4_set = {(a['address'], a.get('subnet_mask', '')) for a in existing_ipv4}

    desired_ipv6_set = {a['address'] for a in desired_ipv6}
    existing_ipv6_set = {a['address'] for a in existing_ipv6}

    # Compute addresses to add and remove
    ipv4_to_add = desired_ipv4_set - existing_ipv4_set
    ipv4_to_remove = existing_ipv4_set - desired_ipv4_set
    ipv6_to_add = desired_ipv6_set - existing_ipv6_set
    ipv6_to_remove = existing_ipv6_set - desired_ipv6_set

    if not ipv4_to_add and not ipv4_to_remove and not ipv6_to_add and not ipv6_to_remove:
        return []

    commands.append('interface {0}'.format(interface_name))

    # Remove old IPv4 addresses
    for addr, mask in ipv4_to_remove:
        commands.append('no ip address {0} {1}'.format(addr, mask))

    # Add new IPv4 addresses
    for addr, mask in ipv4_to_add:
        commands.append('ip address {0} {1}'.format(addr, mask))

    # Remove old IPv6 addresses
    for addr in ipv6_to_remove:
        commands.append('no ipv6 address {0}'.format(addr))

    # Add new IPv6 addresses
    for addr in desired_ipv6_set - existing_ipv6_set:
        commands.append('ipv6 address {0}'.format(addr))

    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    ipv4=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            address=dict(type='str', required=True),
                            subnet_mask=dict(type='str', required=True),
                        ),
                    ),
                    ipv6=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            address=dict(type='str', required=True),
                        ),
                    ),
                ),
            ),
            state=dict(
                type='str',
                default='merged',
                choices=['merged', 'replaced'],
            ),
        ),
        supports_check_mode=True,
    )

    config_list = module.params.get('config', []) or []
    state = module.params.get('state', 'merged')

    # Gather existing facts
    if HAS_FACTS:
        facts = L3InterfacesFacts(module)
        existing_config = facts.get_facts()
    else:
        existing_config = {}

    result = {
        'changed': False,
        'commands': [],
        'before': existing_config,
    }

    all_commands = []

    if state == 'merged':
        for config in config_list:
            commands = build_commands(config, existing_config)
            all_commands.extend(commands)
    elif state == 'replaced':
        for config in config_list:
            commands = build_commands(config, existing_config)
            all_commands.extend(commands)

    result['commands'] = all_commands

    if module.check_mode:
        module.exit_json(**result)

    result['changed'] = bool(all_commands)
    result['after'] = existing_config

    module.exit_json(**result)


if __name__ == '__main__':
    main()
