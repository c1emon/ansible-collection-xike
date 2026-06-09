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
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.lifecycle import run_resource_module_lifecycle
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule as AnsibleModuleType

L3InterfaceConfig = dict[str, Any]
L3InterfaceState = dict[str, L3InterfaceConfig]

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.l3_interfaces import (
        L3InterfacesFacts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def build_commands(config: L3InterfaceConfig, existing_config: L3InterfaceState) -> list[str]:
    """Build CLI commands for a single interface config entry.

    Args:
        config: dict with 'name', 'ipv4', 'ipv6'
        existing_config: dict of current interface configs keyed by name

    Returns:
        list: CLI commands to apply
    """
    commands: list[str] = []
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


def build_lifecycle_commands(
    config_list: list[L3InterfaceConfig],
    state: str,
    existing_config: L3InterfaceState,
) -> list[str]:
    """Build commands for all requested L3 interface configs."""
    commands: list[str] = []
    for config in config_list:
        commands.extend(build_commands(config, existing_config))
    return commands


def build_after_state(
    before: L3InterfaceState,
    desired: list[L3InterfaceConfig],
    state: str,
) -> L3InterfaceState:
    """Build the expected normalized L3 interface state after lifecycle execution."""
    after = dict(before)
    if state == 'replaced':
        after = {}
    for config in desired:
        current = dict(after.get(config['name'], {'ipv4': [], 'ipv6': []}))
        current['ipv4'] = list(config.get('ipv4') or [])
        current['ipv6'] = list(config.get('ipv6') or [])
        after[config['name']] = current
    return after


def gather_l3_interfaces(module: "AnsibleModuleType") -> L3InterfaceState:
    """Gather L3 interface facts required for idempotent diffing."""
    if not HAS_FACTS:
        module.fail_json(msg='L3 interface facts support is required for diffing')
        return {}
    try:
        return L3InterfacesFacts(module).get_facts()
    except Exception as exc:
        module.fail_json(msg='failed to gather L3 interface facts: {0}'.format(exc))
        return {}


def main() -> None:
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

    run_resource_module_lifecycle(
        module=module,
        config=config_list,
        state=state,
        gather=gather_l3_interfaces,
        build_commands=build_lifecycle_commands,
        build_after=build_after_state,
        mutating_states=('merged', 'replaced'),
        rendered_states=(),
        apply_config=load_config,
        gather_after_apply=True,
    )


if __name__ == '__main__':
    main()
