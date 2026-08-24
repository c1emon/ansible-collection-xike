#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        description:
          - LACP mode (only valid when mode is dynamic).
          - Set to C(null) to remove an existing LACP mode configuration.
        type: str
        choices: ['active', 'passive']
  state:
    description:
      - Desired state of the configuration.
      - C(merged) - Add configured members and scalar fields without removing existing members.
      - C(replaced) - Synchronize explicitly declared fields for the listed eth-trunks only.
      - C(gathered) - Gather interface state without changing the device.
      - C(rendered) - Render CLI commands without connecting to the device.
    type: str
    default: merged
    choices: ['merged', 'replaced', 'gathered', 'rendered']
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Create static eth-trunk 1 with two members
  c1emon.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 1
        mode: static
        members:
          - "0/0/1"
          - "0/0/2"
    state: merged

- name: Create dynamic eth-trunk with LACP active
  c1emon.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 2
        mode: dynamic
        lacp_mode: active
        members:
          - "0/0/3"
          - "0/0/4"
    state: merged

- name: Replace eth-trunk 1 mode, LACP, and members
  c1emon.xikeos.xikeos_lag_interfaces:
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
changed:
  description: Whether the module changed the device configuration.
  returned: always
  type: bool
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
  returned: when I(state) is C(merged), C(replaced), or C(rendered)
  type: list
  sample:
    - interface eth-trunk 1
    - link-aggregation mode static
    - link-aggregation members ethernet 0/0/1
    - link-aggregation members ethernet 0/0/2
gathered:
  description: LAG interface state gathered from the device when I(state) is C(gathered).
  returned: when I(state) is C(gathered)
  type: dict
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.lag_interfaces import (
    LagInterfacesFacts,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import (
    gather_with_error_boundary,
    run_resource_module_lifecycle,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.reconcile import (
    FieldPolicy,
    Operation,
    ReconciliationInputError,
    ResourcePlan,
    ResourcePolicy,
    apply_operations_to_state,
    plan_operations,
    seal_resource_plan,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    load_config,
)
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule as AnsibleModuleType

LagInterfaceConfig = dict[str, Any]
LagInterfaceState = dict[str, LagInterfaceConfig]

LAG_POLICY = ResourcePolicy(
    identity=("name",),
    fields={
        "mode": FieldPolicy(kind="scalar", removal_supported=False),
        "lacp_mode": FieldPolicy(kind="scalar", removal_supported=False),
        "members": FieldPolicy(kind="set", identity=()),
    },
)


def _normalize_lag_resource(config: LagInterfaceConfig) -> LagInterfaceConfig:
    """Drop Ansible-inserted None without dropping false/empty values."""
    normalized: LagInterfaceConfig = {"name": config["name"]}
    for field_name in ("mode", "lacp_mode", "members"):
        if config.get(field_name) is not None:
            normalized[field_name] = config[field_name]
    return normalized


def _build_lag_state(config_list: list[LagInterfaceConfig]) -> LagInterfaceState:
    desired: LagInterfaceState = {}
    for config in config_list:
        normalized = _normalize_lag_resource(config)
        trunk_name = normalized["name"]
        if trunk_name in desired:
            raise ReconciliationInputError(
                "duplicate LAG interface config: {0}".format(trunk_name)
            )
        desired[trunk_name] = normalized
    return desired


def _ensure_lag_names(state: LagInterfaceState) -> LagInterfaceState:
    return {
        name: dict(config, name=config.get("name", name))
        for name, config in state.items()
    }


def _normalize_lag_state(state: LagInterfaceState) -> LagInterfaceState:
    return {
        name: _normalize_lag_resource(dict(config, name=config.get("name", name)))
        for name, config in (state or {}).items()
    }


def _render_lag_operations(operations: list[Operation]) -> list[str]:
    commands: list[str] = []
    current_resource = None

    for operation in operations:
        if operation.resource != current_resource:
            commands.append("interface {0}".format(operation.resource[0][1]))
            current_resource = operation.resource

        if operation.field == "mode" and operation.action == "set_field":
            commands.append("link-aggregation mode {0}".format(operation.value))
            continue
        if operation.field == "mode":
            raise ReconciliationInputError(
                "unsupported LAG operation: {0}".format(operation.action)
            )

        if operation.field == "lacp_mode":
            if operation.action == "set_field":
                commands.append("lacp mode {0}".format(operation.value))
            elif operation.action == "unset_field":
                commands.append("no lacp mode")
            else:
                raise ReconciliationInputError(
                    "unsupported LAG operation: {0}".format(operation.action)
                )
            continue

        if operation.field == "members":
            member = operation.value
            if operation.action == "add_item":
                commands.append("link-aggregation members ethernet {0}".format(member))
            elif operation.action == "remove_item":
                commands.append(
                    "no link-aggregation members ethernet {0}".format(member)
                )
            else:
                raise ReconciliationInputError(
                    "unsupported LAG operation: {0}".format(operation.action)
                )
            continue

        raise ReconciliationInputError(
            "unsupported LAG field: {0}".format(operation.field)
        )

    return commands


def _render_lag_operation(operation: Operation) -> list[str]:
    """Render one acknowledged LAG operation for sealed planning."""
    return _render_lag_operations([operation])


def build_lifecycle_plan(
    config_list: list[LagInterfaceConfig],
    state: str,
    existing_config: LagInterfaceState,
) -> ResourcePlan:
    """Build one complete LAG transition without recomputing the diff."""
    before = _normalize_lag_state(existing_config)
    desired = _build_lag_state(config_list)
    operations = plan_operations(before, desired, state, LAG_POLICY)
    plan = seal_resource_plan(
        before, operations, LAG_POLICY, _render_lag_operation, state
    )
    return ResourcePlan(
        plan.operations, plan.commands, _ensure_lag_names(plan.after), plan.changed
    )


def _extract_trunk_id(trunk_name: str) -> str:
    """Extract numeric ID from trunk name like 'eth-trunk 1' -> 1."""
    parts = trunk_name.strip().split()
    return parts[-1] if parts else trunk_name


def build_trunk_commands(
    config: LagInterfaceConfig,
    existing_config: LagInterfaceState,
) -> list[str]:
    """Build replaced-style CLI commands for a single eth-trunk config entry.

    This preserves the legacy direct helper behavior. Lifecycle execution uses
    build_lifecycle_commands() so the requested state controls reconciliation.

    Args:
        config: dict with keys: name, mode, members, lacp_mode
        existing_config: dict of current state keyed by trunk name

    Returns:
        list of CLI command strings (empty if no changes needed)
    """
    desired = _build_lag_state([config])
    operations = plan_operations(
        _normalize_lag_state(existing_config), desired, "replaced", LAG_POLICY
    )
    return _render_lag_operations(operations)


def build_lifecycle_commands(
    config_list: list[LagInterfaceConfig],
    state: str,
    existing_config: LagInterfaceState,
) -> list[str]:
    """Build commands for all requested LAG interface configs."""
    desired = _build_lag_state(config_list)
    operations = plan_operations(
        _normalize_lag_state(existing_config), desired, state, LAG_POLICY
    )
    return _render_lag_operations(operations)


def build_after_state(
    before: LagInterfaceState,
    desired: list[LagInterfaceConfig],
    state: str,
) -> LagInterfaceState:
    """Build the expected normalized LAG interface state after lifecycle execution."""
    desired_state = _build_lag_state(desired)
    normalized_before = _normalize_lag_state(before)
    operations = plan_operations(normalized_before, desired_state, state, LAG_POLICY)
    return _ensure_lag_names(
        apply_operations_to_state(normalized_before, operations, LAG_POLICY)
    )


def gather_lag_interfaces(module: "AnsibleModuleType") -> LagInterfaceState:
    """Gather LAG interface facts required for idempotent diffing."""
    return gather_with_error_boundary(
        module,
        lambda: LagInterfacesFacts(module).get_facts(),
        "failed to gather LAG interface facts",
        "lag_interfaces",
        {},
    )


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type="list",
                elements="dict",
                options=dict(
                    name=dict(type="str", required=True),
                    mode=dict(type="str", choices=["static", "dynamic"]),
                    members=dict(
                        type="list",
                        elements="str",
                        default=None,
                    ),
                    lacp_mode=dict(type="str", choices=["active", "passive"]),
                ),
            ),
            state=dict(
                type="str",
                default="merged",
                choices=["merged", "replaced", "gathered", "rendered"],
            ),
        ),
        supports_check_mode=True,
    )

    config_list = module.params.get("config", []) or []
    state = module.params.get("state", "merged")

    run_resource_module_lifecycle(
        module=module,
        config=config_list,
        state=state,
        gather=gather_lag_interfaces,
        build_commands=build_lifecycle_commands,
        build_after=build_after_state,
        build_plan=build_lifecycle_plan,
        mutating_states=("merged", "replaced"),
        gathered_states=("gathered",),
        rendered_states=("rendered",),
        rendered_current={},
        apply_config=load_config,
        gather_after_apply=True,
    )


if __name__ == "__main__":
    main()
