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
  - Supports line-by-line config, explicit save, and check mode.
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
    description:
      - Reserved for future diff support.
      - Currently unsupported; setting this option to C(true) fails the module.
    type: bool
    default: false
  backup:
    description:
      - Reserved for future backup support.
      - Currently unsupported; setting this option to C(true) fails the module.
    type: bool
    default: false
author: Andy
"""

EXAMPLES = """
- name: Push config lines
  c1emon.xikeos.xikeos_config:
    lines:
      - vlan 100
      - name DATA
      - interface ethernet 0/0/1
      - switchport pvid 100
    save: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config, run_commands


SAVE_COMMAND = 'write memory'


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            lines=dict(type='list', elements='str'),
            save=dict(type='bool', default=False),
            diff=dict(type='bool', default=False),
            backup=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    lines = module.params.get('lines', [])
    save = module.params.get('save', False)
    diff = module.params.get('diff', False)
    backup = module.params.get('backup', False)

    if diff:
        module.fail_json(msg='diff is not supported by xikeos_config yet')
    if backup:
        module.fail_json(msg='backup is not supported by xikeos_config yet')

    if not lines and not save:
        module.exit_json(changed=False, commands=[], saved=False, msg='No lines to configure')

    result = {
        'changed': bool(lines),
        'commands': list(lines),
        'saved': False,
    }

    if module.check_mode:
        module.exit_json(**result)

    if lines:
        response = load_config(module, lines)
        result['response'] = response.get('response', response) if isinstance(response, dict) else response

    if save and result['changed']:
        run_commands(module, [SAVE_COMMAND], check_rc=True)
        result['commands'].append(SAVE_COMMAND)
        result['saved'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
