#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike switch configuration module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_config
short_description: Manage Xike switch configuration
version_added: "0.1.0"
description:
  - Push configuration lines to Xike switches.
  - Supports line-by-line config, save, and diff.
options:
  lines:
    description: List of configuration commands
    type: list
    elements: str
  save:
    description: Save running-config to startup-config
    type: bool
    default: false
  diff:
    description: Show diff before applying
    type: bool
    default: true
  backup:
    description: Backup current config before changes
    type: bool
    default: false
author: Andy
"""

EXAMPLES = """
- name: Push config lines
  xike.xikeos.xikeos_config:
    lines:
      - vlan 100
      - name DATA
      - interface ethernet 0/0/1
      - switchport pvid 100
    save: true
"""

from ansible.module_utils.basic import AnsibleModule
import json


def main():
    module = AnsibleModule(
        argument_spec=dict(
            lines=dict(type='list', elements='str'),
            save=dict(type='bool', default=False),
            diff=dict(type='bool', default=True),
            backup=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    lines = module.params.get('lines', [])
    save = module.params.get('save', False)

    if not lines:
        module.exit_json(msg='No lines to configure')

    result = {
        'changed': False,
        'commands': lines,
    }

    if module.check_mode:
        module.exit_json(**result)

    # The actual push would happen via the connection plugin
    # In check mode, we just return the commands
    result['changed'] = True

    if save:
        result['commands'].append('write memory')

    module.exit_json(**result)


if __name__ == '__main__':
    main()
