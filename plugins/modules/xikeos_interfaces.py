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

    if not config:
        module.exit_json(msg='No interface configuration provided', changed=False)

    all_commands = []

    for cfg in config:
        cmds = build_interface_commands(cfg)
        all_commands.extend(cmds)

    result = {
        'changed': False,
        'commands': all_commands,
    }

    if module.check_mode:
        module.exit_json(**result)

    # Non-reference module: report planned commands; execution will be added in a follow-up refactor.
    result['changed'] = True
    module.exit_json(**result)


if __name__ == '__main__':
    main()
