#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS L2 Interfaces resource module with hybrid support."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
# pylint: disable=unsupported-binary-operation

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
    description:
      - Desired state of the configuration.
      - C(merged) - Create or update interface config as specified.
      - C(replaced) - Replace existing interface config with specified config.
      - C(gathered) - Gather interface state without changing the device.
      - C(rendered) - Render CLI commands without connecting to the device.
    type: str
    default: merged
    choices: ['merged', 'replaced', 'gathered', 'rendered']
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Configure access port
  c1emon.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: access
        access_vlan: 100
    state: merged

- name: Configure trunk port
  c1emon.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/2
        mode: trunk
        trunk_allowed_vlan: "10,20,30"
    state: merged

- name: Configure hybrid port (Xike unique feature)
  c1emon.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/3
        mode: hybrid
        pvid: 100
        hybrid_untagged_vlan: "10,20"
        hybrid_tagged_vlan: "30,40"
    state: merged

- name: Replace all L2 interface configs
  c1emon.xikeos.xikeos_l2_interfaces:
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
    - interface ethernet 0/0/1
    - switchport link-type access
    - switchport pvid 100
gathered:
  description: Interface state gathered from the device when I(state) is C(gathered).
  returned: when I(state) is C(gathered)
  type: dict
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.l2_interfaces import (
    L2InterfacesFacts,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    load_config,
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
    plan_operations,
    seal_resource_plan,
)
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule as AnsibleModuleType

L2InterfaceConfig = dict[str, Any]
L2InterfaceState = dict[str, L2InterfaceConfig]
L2_FIELDS = (
    "mode",
    "pvid",
    "access_vlan",
    "trunk_allowed_vlan",
    "hybrid_untagged_vlan",
    "hybrid_tagged_vlan",
)
L2_POLICY = ResourcePolicy(
    identity=("name",),
    fields={
        field: FieldPolicy(kind="scalar", removal_supported=False)
        for field in L2_FIELDS
    },
)


def parse_vlan_str(vlan_str: object) -> str | None:
    """Parse VLAN string like '10,20,30' or 'all' into a normalized format."""
    if not vlan_str:
        return None
    vlan_str = str(vlan_str).strip()
    if vlan_str.lower() == "all":
        return "all"
    return vlan_str


def _normalize_l2_resource(config: L2InterfaceConfig) -> L2InterfaceConfig:
    normalized = {
        field: value
        for field, value in config.items()
        if field in ("name",) + L2_FIELDS and value is not None
    }
    if "name" not in normalized:
        raise ReconciliationInputError("L2 interface configuration is missing name")
    if normalized.get("pvid") is not None and normalized.get("access_vlan") is not None:
        if normalized["pvid"] != normalized["access_vlan"]:
            raise ReconciliationInputError(
                "pvid and access_vlan must match when both are supplied"
            )
    return normalized


def _normalize_l2_state(state: L2InterfaceState) -> L2InterfaceState:
    return {
        name: _normalize_l2_resource({"name": name, **config})
        for name, config in state.items()
    }


def _desired_l2_map(config_list: list[L2InterfaceConfig]) -> L2InterfaceState:
    desired: L2InterfaceState = {}
    for config in config_list:
        normalized = _normalize_l2_resource(config)
        name = normalized["name"]
        if name in desired:
            raise ReconciliationInputError(
                "duplicate L2 interface config: {0}".format(name)
            )
        desired[name] = normalized
    return desired


def _render_l2_operation(operation: Operation) -> list[str]:
    name = dict(operation.resource)["name"]
    if operation.action != "set_field":
        raise ReconciliationInputError(
            "unsupported L2 interface operation: {0}".format(operation)
        )
    no_or_set = {
        "mode": "switchport link-type {0}".format(operation.value),
        "pvid": "switchport pvid {0}".format(operation.value),
        "access_vlan": "switchport pvid {0}".format(operation.value),
        "trunk_allowed_vlan": "no switchport trunk allowed vlan"
        if operation.value == ""
        else "switchport trunk allowed vlan {0}".format(operation.value),
        "hybrid_untagged_vlan": "no switchport hybrid untagged vlan"
        if operation.value == ""
        else "switchport hybrid untagged vlan {0}".format(operation.value),
        "hybrid_tagged_vlan": "no switchport hybrid tagged vlan"
        if operation.value == ""
        else "switchport hybrid tagged vlan {0}".format(operation.value),
    }
    if operation.field not in no_or_set:
        raise ReconciliationInputError(
            "unsupported L2 interface field: {0}".format(operation.field)
        )
    return ["interface {0}".format(name), no_or_set[operation.field]]


def build_lifecycle_plan(
    config_list: list[L2InterfaceConfig],
    state: str,
    existing_config: L2InterfaceState,
) -> ResourcePlan:
    current = _normalize_l2_state(existing_config)
    desired = _desired_l2_map(config_list)
    operations = plan_operations(current, desired, state, L2_POLICY)
    return seal_resource_plan(
        current, operations, L2_POLICY, _render_l2_operation, state
    )


def build_commands(
    config: L2InterfaceConfig,
    state: str,
    existing_config: L2InterfaceState,
) -> list[str]:
    """Build a sealed one-resource CLI plan for compatibility callers."""
    return list(build_lifecycle_plan([config], state, existing_config).commands)


def build_lifecycle_commands(
    config_list: list[L2InterfaceConfig],
    state: str,
    existing_config: L2InterfaceState,
) -> list[str]:
    """Build commands for all requested L2 interface configs."""
    return list(build_lifecycle_plan(config_list, state, existing_config).commands)


def build_after_state(
    before: L2InterfaceState,
    desired: list[L2InterfaceConfig],
    state: str,
) -> L2InterfaceState:
    """Build the expected normalized L2 interface state after lifecycle execution."""
    return build_lifecycle_plan(desired, state, before).after


def gather_l2_interfaces(module: "AnsibleModuleType") -> L2InterfaceState:
    """Gather L2 interface facts required for idempotent diffing."""
    return gather_with_error_boundary(
        module,
        lambda: L2InterfacesFacts(module).get_facts(),
        "failed to gather L2 interface facts",
        "l2_interfaces",
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
                    mode=dict(type="str", choices=["access", "trunk", "hybrid"]),
                    access_vlan=dict(type="int"),
                    trunk_allowed_vlan=dict(type="str"),
                    hybrid_untagged_vlan=dict(type="str"),
                    hybrid_tagged_vlan=dict(type="str"),
                    pvid=dict(type="int"),
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
        gather=gather_l2_interfaces,
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
