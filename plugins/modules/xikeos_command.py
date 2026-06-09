#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike switch command module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

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
      - show vlan
  register: result

- debug:
    var: result.stdout
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands


def _split_lines(output: Any) -> list[str]:
    """Split any command output into normalized text lines."""
    return to_text(output, errors='surrogate_or_strict').splitlines()


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            commands=dict(type='list', elements='str', required=True),
        ),
        supports_check_mode=True,
    )

    commands = module.params['commands']

    stdout = []
    try:
        stdout = run_commands(module, commands, check_rc=True)
    except Exception as exc:
        module.fail_json(msg='command execution failed', commands=commands, error=to_text(exc))

    stdout = [to_text(item, errors='surrogate_or_strict') for item in stdout]

    result = {
        'changed': False,
        'commands': commands,
        'stdout': stdout,
        'stdout_lines': [_split_lines(item) for item in stdout],
    }

    module.exit_json(**result)


if __name__ == '__main__':
    main()
