#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike switch interfaces resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_interfaces
short_description: Manage Xike switch interfaces
version_added: "0.1.0"
description:
  - Configure Ethernet interfaces on Xike switches.
  - Supports merged and replaced states.
options:
  config:
    description: List of interface configurations
    type: list
    elements: dict
    suboptions:
      name:
        description: Interface name (e.g. ethernet 0/0/1)
        type: str
        required: true
      description:
        description: Interface description string
        type: str
      speed:
        description: Interface speed
        type: str
        choices: ['10', '100', '1000', '10000', 'auto']
      duplex:
        description: Interface duplex mode
        type: str
        choices: ['auto', 'full', 'half']
      enabled:
        description: Admin state of the interface (false = shutdown)
        type: bool
        default: true
      mtu:
        description: MTU size
        type: int
  state:
    description: Desired state
    type: str
    choices: ['merged', 'replaced']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Configure interface ethernet 0/0/1
  xike.xikeos.xikeos_interfaces:
    config:
      - name: ethernet 0/0/1
        description: Uplink to core
        speed: 1000
        duplex: full
        enabled: true
        mtu: 1500
    state: merged

- name: Replace all interface config
  xike.xikeos.xikeos_interfaces:
    config:
      - name: ethernet 0/0/2
        speed: auto
        duplex: auto
        enabled: false
    state: replaced
"""

RETURN = """
commands:
  description: CLI commands sent to the device
  returned: always
  type: list
  sample:
    - interface ethernet 0/0/1
    - description Uplink to core
    - speed 1000
    - duplex full
    - mtu 1500
    - no shutdown
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xike.xikeos.plugins.module_utils.facts.interfaces import InterfacesFacts
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.lifecycle import run_resource_module_lifecycle

# Reuse constants from module_utils
SPEED_OPTIONS = ['10', '100', '1000', '10000', 'auto']
DUPLEX_OPTIONS = ['auto', 'full', 'half']


def build_interface_commands(cfg):
    """Generate CLI commands for a single interface config entry."""
    name = cfg['name']
    commands = [
        'interface {name}'.format(name=name),
    ]

    # Description
    desc = cfg.get('description')
    if desc is not None:
        if desc:
            commands.append('description {desc}'.format(desc=desc))
        else:
            # Empty string means remove description
            commands.append('no description')

    # Speed
    speed = cfg.get('speed')
    if speed is not None:
        commands.append('speed {speed}'.format(speed=speed))

    # Duplex
    duplex = cfg.get('duplex')
    if duplex is not None:
        commands.append('duplex {duplex}'.format(duplex=duplex))

    # MTU
    mtu = cfg.get('mtu')
    if mtu is not None:
        commands.append('mtu {mtu}'.format(mtu=mtu))

    # Enabled / shutdown
    enabled = cfg.get('enabled')
    if enabled is not None:
        if enabled:
            commands.append('no shutdown')
        else:
            commands.append('shutdown')

    return commands


def _normalize_interface_config(cfg):
    normalized = dict(cfg)
    if 'shutdown' in normalized and 'enabled' not in normalized:
        normalized['enabled'] = not normalized.get('shutdown')
    return normalized


def build_commands(config_list, state, existing_config):
    commands = []
    for cfg in config_list:
        desired = _normalize_interface_config(cfg)
        existing = _normalize_interface_config(existing_config.get(desired['name'], {}))
        changed_cfg = {'name': desired['name']}
        for field in ('description', 'speed', 'duplex', 'enabled', 'mtu'):
            if field in desired and desired.get(field) != existing.get(field):
                changed_cfg[field] = desired.get(field)
        if len(changed_cfg) > 1:
            commands.extend(build_interface_commands(changed_cfg))
    return commands


def build_after_state(before, desired, state):
    after = {name: _normalize_interface_config(value) for name, value in before.items()}
    if state == 'replaced':
        after = {}
    for cfg in desired:
        normalized = _normalize_interface_config(cfg)
        current = after.get(normalized['name'], {'name': normalized['name']})
        current.update(normalized)
        after[normalized['name']] = current
    return after


def gather_interfaces(module):
    try:
        return InterfacesFacts(module).get_facts()
    except Exception as exc:
        module.fail_json(msg='failed to gather interface facts: {0}'.format(exc))
        return {}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    description=dict(type='str', default=None),
                    speed=dict(type='str', choices=SPEED_OPTIONS, default=None),
                    duplex=dict(type='str', choices=DUPLEX_OPTIONS, default=None),
                    enabled=dict(type='bool', default=True),
                    mtu=dict(type='int', default=None),
                ),
            ),
            state=dict(
                type='str',
                choices=['merged', 'replaced'],
                default='merged',
            ),
        ),
        supports_check_mode=True,
    )

    config = module.params.get('config', []) or []
    state = module.params.get('state', 'merged')
    run_resource_module_lifecycle(
        module=module,
        config=config,
        state=state,
        gather=gather_interfaces,
        build_commands=build_commands,
        build_after=build_after_state,
        mutating_states=('merged', 'replaced'),
        rendered_states=(),
        apply_config=load_config,
        gather_after_apply=True,
    )


if __name__ == '__main__':
    main()
