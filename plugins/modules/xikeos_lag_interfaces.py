#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS LAG Interfaces resource module (eth-trunk)."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_lag_interfaces
short_description: Manage LAG (eth-trunk) interface configurations on Xike switches
version_added: "0.1.0"
description:
  - This module provides declarative management of Link Aggregation Group
    (LAG) eth-trunk configurations on Xike (兮克) switches.
  - Supports creating, modifying, and removing eth-trunk bundles with
    static or dynamic (LACP) link aggregation.
options:
  config:
    description: List of eth-trunk configurations
    type: list
    elements: dict
    suboptions:
      name:
        description: Eth-trunk name (e.g., 'eth-trunk 1')
        type: str
        required: true
      mode:
        description: Link aggregation mode
        type: str
        choices: ['static', 'dynamic']
      members:
        description: List of member ethernet port IDs (e.g., ['0/0/1', '0/0/2'])
        type: list
        elements: str
      lacp_mode:
        description: LACP mode (only valid when mode is dynamic)
        type: str
        choices: ['active', 'passive']
  state:
    description: Desired state of the configuration
    type: str
    default: merged
    choices: ['merged', 'replaced']
author: Andy
"""

EXAMPLES = """
- name: Create static eth-trunk 1 with two members
  xike.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 1
        mode: static
        members:
          - "0/0/1"
          - "0/0/2"
    state: merged

- name: Create dynamic eth-trunk with LACP active
  xike.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 2
        mode: dynamic
        lacp_mode: active
        members:
          - "0/0/3"
          - "0/0/4"
    state: merged

- name: Replace eth-trunk configuration
  xike.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 1
        mode: dynamic
        lacp_mode: passive
        members:
          - "0/0/1"
          - "0/0/3"
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
    - interface eth-trunk 1
    - link-aggregation mode static
    - link-aggregation members ethernet 0/0/1
    - link-aggregation members ethernet 0/0/2
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.lifecycle import run_resource_module_lifecycle
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule as AnsibleModuleType

LagInterfaceConfig = dict[str, Any]
LagInterfaceState = dict[str, LagInterfaceConfig]

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.lag_interfaces import (
        LagInterfacesFacts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def _extract_trunk_id(trunk_name: str) -> str:
    """Extract numeric ID from trunk name like 'eth-trunk 1' -> 1."""
    parts = trunk_name.strip().split()
    return parts[-1] if parts else trunk_name


def build_trunk_commands(
    config: LagInterfaceConfig,
    existing_config: LagInterfaceState,
) -> list[str]:
    """Build CLI commands for a single eth-trunk config entry.

    Args:
        config: dict with keys: name, mode, members, lacp_mode
        existing_config: dict of current state keyed by trunk name

    Returns:
        list of CLI command strings (empty if no changes needed)
    """
    commands: list[str] = []
    trunk_name = config['name']
    trunk_id = _extract_trunk_id(trunk_name)
    existing = existing_config.get(trunk_name, {})

    existing_mode = existing.get('mode')
    existing_members = existing.get('members', [])
    existing_lacp = existing.get('lacp_mode')

    mode = config.get('mode')
    members = config.get('members', [])
    lacp_mode = config.get('lacp_mode')

    # Determine if any changes are needed
    mode_changed = mode is not None and mode != existing_mode
    members_set_changed = set(members or []) != set(existing_members or [])
    lacp_changed = lacp_mode is not None and lacp_mode != existing_lacp

    if not mode_changed and not members_set_changed and not lacp_changed:
        return []

    # Enter eth-trunk interface mode
    commands.append('interface eth-trunk {0}'.format(trunk_id))

    # Set link-aggregation mode
    if mode_changed:
        commands.append('link-aggregation mode {0}'.format(mode))

    # Add members (new additions only)
    if members_set_changed:
        desired = set(members or [])
        current = set(existing_members or [])

        # Members to add
        to_add = desired - current
        for port in sorted(to_add):
            commands.append('link-aggregation members ethernet {0}'.format(port))

        # Members to remove
        to_remove = current - desired
        for port in sorted(to_remove):
            commands.append('no link-aggregation members ethernet {0}'.format(port))

    # Set LACP mode
    if lacp_changed:
        if lacp_mode:
            commands.append('lacp mode {0}'.format(lacp_mode))
        else:
            commands.append('no lacp mode')

    return commands


def build_lifecycle_commands(
    config_list: list[LagInterfaceConfig],
    state: str,
    existing_config: LagInterfaceState,
) -> list[str]:
    """Build commands for all requested LAG interface configs."""
    commands: list[str] = []
    for config in config_list:
        commands.extend(build_trunk_commands(config, existing_config))
    return commands


def build_after_state(
    before: LagInterfaceState,
    desired: list[LagInterfaceConfig],
    state: str,
) -> LagInterfaceState:
    """Build the expected normalized LAG interface state after lifecycle execution."""
    after = dict(before)
    if state == 'replaced':
        after = {}
    for config in desired:
        current = dict(after.get(config['name'], {}))
        current.update(config)
        after[config['name']] = current
    return after


def gather_lag_interfaces(module: "AnsibleModuleType") -> LagInterfaceState:
    """Gather LAG interface facts required for idempotent diffing."""
    if not HAS_FACTS:
        module.fail_json(msg='LAG interface facts support is required for diffing')
        return {}
    try:
        return LagInterfacesFacts(module).get_facts()
    except Exception as exc:
        module.fail_json(msg='failed to gather LAG interface facts: {0}'.format(exc))
        return {}


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    mode=dict(type='str', choices=['static', 'dynamic']),
                    members=dict(
                        type='list',
                        elements='str',
                        default=None,
                    ),
                    lacp_mode=dict(type='str', choices=['active', 'passive']),
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
        gather=gather_lag_interfaces,
        build_commands=build_lifecycle_commands,
        build_after=build_after_state,
        mutating_states=('merged', 'replaced'),
        rendered_states=(),
        apply_config=load_config,
        gather_after_apply=True,
    )


if __name__ == '__main__':
    main()
