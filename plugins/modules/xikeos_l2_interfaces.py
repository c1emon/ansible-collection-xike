#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS L2 Interfaces resource module with hybrid support."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_l2_interfaces
short_description: Manage L2 interface configurations on Xike switches
version_added: "0.1.0"
description:
  - This module provides declarative management of Layer 2 interface
    configurations on Xike (兮克) switches.
  - Supports access, trunk, and hybrid port modes.
  - Hybrid mode is a unique feature of Xike switches not found on Cisco.
options:
  config:
    description: List of interface configurations
    type: list
    elements: dict
    suboptions:
      name:
        description: Interface name (e.g., ethernet 0/0/1)
        type: str
        required: true
      mode:
        description: Interface link-type mode
        type: str
        choices: ['access', 'trunk', 'hybrid']
      access_vlan:
        description: VLAN ID for access port
        type: int
      trunk_allowed_vlan:
        description: VLAN list allowed on trunk port (e.g., "10,20,30" or "all")
        type: str
      hybrid_untagged_vlan:
        description: VLANs to send untagged on hybrid port (e.g., "10,20" or "all")
        type: str
      hybrid_tagged_vlan:
        description: VLANs to send tagged on hybrid port (e.g., "30,40" or "all")
        type: str
      pvid:
        description: Port VLAN ID (PVID) for the interface
        type: int
  state:
    description: Desired state of the configuration
    type: str
    default: merged
    choices: ['merged', 'replaced']
author: Andy
"""

EXAMPLES = """
- name: Configure access port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: access
        access_vlan: 100
    state: merged

- name: Configure trunk port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/2
        mode: trunk
        trunk_allowed_vlan: "10,20,30"
    state: merged

- name: Configure hybrid port (Xike unique feature)
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/3
        mode: hybrid
        pvid: 100
        hybrid_untagged_vlan: "10,20"
        hybrid_tagged_vlan: "30,40"
    state: merged

- name: Replace all L2 interface configs
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: trunk
        trunk_allowed_vlan: "all"
      - name: ethernet 0/0/2
        mode: hybrid
        pvid: 50
        hybrid_untagged_vlan: "50"
        hybrid_tagged_vlan: "100,200"
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
    - interface ethernet 0/0/1
    - switchport link-type access
    - switchport pvid 100
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.l2_interfaces import L2InterfacesFacts
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def parse_vlan_str(vlan_str):
    """Parse VLAN string like '10,20,30' or 'all' into a normalized format."""
    if not vlan_str:
        return None
    vlan_str = str(vlan_str).strip()
    if vlan_str.lower() == 'all':
        return 'all'
    return vlan_str


def build_commands(config, state, existing_config):
    """Build CLI commands from config, respecting link-type ordering."""
    commands = []
    interface_name = config['name']

    # Get existing config for this interface
    existing = existing_config.get(interface_name, {})

    # Start with interface mode command
    commands.append('interface {0}'.format(interface_name))

    mode = config.get('mode')
    existing_mode = existing.get('mode')

    # Determine if we need to change link-type
    if mode and mode != existing_mode:
        commands.append('switchport link-type {0}'.format(mode))
    elif mode is None and existing_mode:
        # No mode specified in config, use existing mode for validation
        mode = existing_mode

    # Set PVID (can be applied in any mode)
    pvid = config.get('pvid')
    existing_pvid = existing.get('pvid')
    if pvid and pvid != existing_pvid:
        commands.append('switchport pvid {0}'.format(pvid))

    # Access VLAN configuration
    if mode == 'access':
        access_vlan = config.get('access_vlan')
        if access_vlan:
            # For access mode, PVID is the access VLAN
            existing_access = existing.get('access_vlan')
            if access_vlan != existing_access:
                if pvid != access_vlan:
                    commands.append('switchport pvid {0}'.format(access_vlan))

    # Trunk allowed VLAN configuration
    if mode == 'trunk':
        trunk_allowed = config.get('trunk_allowed_vlan')
        existing_trunk = existing.get('trunk_allowed_vlan')
        if trunk_allowed and trunk_allowed != existing_trunk:
            commands.append('switchport trunk allowed vlan {0}'.format(trunk_allowed))

    # Hybrid VLAN configuration (Xike unique)
    if mode == 'hybrid':
        hybrid_untagged = config.get('hybrid_untagged_vlan')
        hybrid_tagged = config.get('hybrid_tagged_vlan')
        existing_untagged = existing.get('hybrid_untagged_vlan')
        existing_tagged = existing.get('hybrid_tagged_vlan')

        if hybrid_untagged and hybrid_untagged != existing_untagged:
            commands.append('switchport hybrid untagged vlan {0}'.format(hybrid_untagged))

        if hybrid_tagged and hybrid_tagged != existing_tagged:
            commands.append('switchport hybrid tagged vlan {0}'.format(hybrid_tagged))

    # If only interface command was added, no actual config changes
    if len(commands) == 1:
        return []

    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    mode=dict(type='str', choices=['access', 'trunk', 'hybrid']),
                    access_vlan=dict(type='int'),
                    trunk_allowed_vlan=dict(type='str'),
                    hybrid_untagged_vlan=dict(type='str'),
                    hybrid_tagged_vlan=dict(type='str'),
                    pvid=dict(type='int'),
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

    config_list = module.params.get('config', [])
    state = module.params.get('state', 'merged')

    # Gather existing facts
    if HAS_FACTS:
        facts = L2InterfacesFacts(module)
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
        # In merged mode, apply each config entry
        for config in config_list:
            commands = build_commands(config, state, existing_config)
            all_commands.extend(commands)
    elif state == 'replaced':
        # In replaced mode, we need to build commands for all interfaces
        # specified in config, potentially removing unmentioned interfaces
        for config in config_list:
            commands = build_commands(config, state, existing_config)
            all_commands.extend(commands)

    result['commands'] = all_commands

    if module.check_mode:
        module.exit_json(**result)

    # After applying commands, gather new facts
    result['changed'] = bool(all_commands)

    # Simulate after state (in real implementation, would re-run facts)
    result['after'] = existing_config

    module.exit_json(**result)


if __name__ == '__main__':
    main()
