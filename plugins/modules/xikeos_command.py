#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike switch command module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_command
short_description: Run commands on Xike switches
version_added: "0.1.0"
description:
  - Execute show commands on Xike switches and return output.
  - Read-only module, never changes device state.
options:
  commands:
    description: List of commands to execute
    type: list
    elements: str
    required: true
author: Andy
"""

EXAMPLES = """
- name: Show version
  xike.xikeos.xikeos_command:
    commands:
      - show version
      - show vlan brief
  register: result

- debug:
    var: result.stdout
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            commands=dict(type='list', elements='str', required=True),
        ),
        supports_check_mode=True,
    )

    commands = module.params['commands']

    result = {
        'changed': False,
        'commands': commands,
        'stdout': [],
    }

    module.exit_json(**result)


if __name__ == '__main__':
    main()
