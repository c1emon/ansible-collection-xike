#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike switch command module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time
from typing import Any

DOCUMENTATION = """
module: xikeos_command
short_description: Run commands on Xike switches
version_added: "0.1.0"
description:
  - Execute show commands on Xike switches and return output.
  - Read-only by default; mutating/destructive commands are blocked unless C(unsafe_allow_mutating_commands=true).
  - When the unsafe override is enabled and guarded commands are executed, the module may report C(changed=true).
options:
  commands:
    description: List of commands to execute
    type: list
    elements: str
    required: true
  wait_for:
    description: Conditions that must match command output before the module succeeds.
    type: list
    elements: str
    required: false
  match:
    description: Whether all or any wait conditions must match.
    type: str
    choices: ['all', 'any']
    default: all
  retries:
    description: Number of times to evaluate wait conditions.
    type: int
    default: 10
  interval:
    description: Seconds to wait between retries.
    type: int
    default: 1
  unsafe_allow_mutating_commands:
    description:
      - Intentionally unsafe override that allows known mutating/destructive commands.
      - Defaults to false so this module blocks those commands by default.
      - Enabling this option can cause the module to return C(changed=true).
    type: bool
    default: false
author: clemon
"""

EXAMPLES = """
- name: Show version
  c1emon.xikeos.xikeos_command:
    commands:
      - show version
      - show vlan
  register: result

- debug:
    var: result.stdout

- name: Allow a guarded command explicitly
  c1emon.xikeos.xikeos_command:
    commands:
      - write memory
    unsafe_allow_mutating_commands: true
  register: saved
"""

RETURN = """
changed:
  description: Whether the module executed guarded mutating/destructive commands.
  type: bool
  returned: always
commands:
  description: Commands submitted to the device.
  type: list
  elements: str
  returned: always
stdout:
  description: Redacted command output, with sensitive values masked.
  type: list
  elements: str
  returned: always
stdout_lines:
  description: Redacted command output split into lines, with sensitive values masked.
  type: list
  elements: list
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.errors import XikeOSError
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.safety import (
    find_mutating_commands,
    redact_value,
)


def _condition_matches(condition: str, stdout: list[str]) -> bool:
    """Evaluate a small mainstream-compatible subset of wait_for expressions."""
    text = to_text(condition, errors='surrogate_or_strict').strip()
    if not text:
        return True
    negated = False
    if text.startswith('not '):
        negated = True
        text = text[4:].strip()
    result_index = 0
    result_match = None
    import re
    result_match = re.match(r"result\[(\d+)\]\s+(contains|==|!=|matches)\s+(.+)", text)
    if result_match:
        result_index = int(result_match.group(1))
        operator = result_match.group(2)
        expected = result_match.group(3).strip().strip('"\'')
    else:
        operator = 'contains'
        expected = text
    actual = stdout[result_index] if result_index < len(stdout) else ''
    if operator == 'contains':
        matched = expected in actual
    elif operator == '==':
        matched = actual == expected
    elif operator == '!=':
        matched = actual != expected
    else:
        matched = re.search(expected, actual, re.M) is not None
    return not matched if negated else matched


def _conditions_satisfied(conditions: list[str], stdout: list[str], match: str) -> tuple[bool, list[str]]:
    """Return wait_for status and conditions that are still unsatisfied."""
    failed = [condition for condition in conditions if not _condition_matches(condition, stdout)]
    if match == 'any':
        return len(failed) < len(conditions), failed
    return not failed, failed


def _split_lines(output: Any) -> list[str]:
    """Split any command output into normalized text lines."""
    return to_text(output, errors='surrogate_or_strict').splitlines()


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            commands=dict(type='list', elements='str', required=True),
            wait_for=dict(type='list', elements='str', default=[]),
            match=dict(type='str', choices=['all', 'any'], default='all'),
            retries=dict(type='int', default=10),
            interval=dict(type='int', default=1),
            unsafe_allow_mutating_commands=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    commands = module.params['commands']
    unsafe_commands = find_mutating_commands(commands)
    if unsafe_commands and not module.params.get('unsafe_allow_mutating_commands'):
        module.fail_json(
            msg='mutating/destructive commands are blocked by default in xikeos_command',
            commands=unsafe_commands,
        )
        return
    if unsafe_commands:
        module.warn('unsafe_allow_mutating_commands enabled for guarded commands: {0}'.format(', '.join(unsafe_commands)))
        if module.check_mode:
            module.exit_json(
                changed=True,
                commands=commands,
                stdout=[],
                stdout_lines=[],
            )
            return

    stdout = []
    failed_conditions = []
    wait_for = module.params.get('wait_for') or []
    retries = module.params.get('retries', 10)
    interval = module.params.get('interval', 1)
    try:
        for attempt in range(retries):
            stdout = run_commands(module, commands, check_rc=True)
            stdout = [to_text(item, errors='surrogate_or_strict') for item in stdout]
            if not wait_for:
                break
            satisfied, failed_conditions = _conditions_satisfied(wait_for, stdout, module.params.get('match'))
            if satisfied:
                failed_conditions = []
                break
            if attempt < retries - 1:
                time.sleep(interval)
    except XikeOSError as exc:
        module.fail_json(msg='command execution failed', commands=commands, error=str(exc), detail=getattr(exc, 'detail', None), context=getattr(exc, 'context', 'command'))
        return
    except Exception as exc:
        module.fail_json(msg='command execution failed', commands=commands, error=to_text(exc), context='command')

    if failed_conditions:
        module.fail_json(
            msg='one or more wait_for conditions were not satisfied',
            failed_conditions=failed_conditions,
            stdout=redact_value(stdout),
        )
        return

    result = {
        'changed': bool(unsafe_commands),
        'commands': commands,
        'stdout': redact_value(stdout),
        'stdout_lines': redact_value([_split_lines(item) for item in stdout]),
    }

    module.exit_json(**result)


if __name__ == '__main__':
    main()
