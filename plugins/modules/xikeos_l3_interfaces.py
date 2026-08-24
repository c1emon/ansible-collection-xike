#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS L3 Interfaces resource module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: xikeos_l3_interfaces
short_description: Manage L3 interface (VLAN interface) IP configurations on Xike switches
version_added: "0.1.0"
description:
  - This module provides declarative management of Layer 3 VLAN interface
    IP configurations on Xike (兮克) switches.
  - Manages IPv4 and IPv6 addresses on VLAN interfaces.
  - Xike uses 'interface vlan-interface <id>' syntax (not 'interface Vlan<id>').
options:
  config:
    description: List of VLAN interface configurations
    type: list
    elements: dict
    suboptions:
      name:
        description: VLAN interface name (e.g., 'vlan-interface 1')
        type: str
        required: true
      ipv4:
        description: List of IPv4 addresses to configure
        type: list
        elements: dict
        suboptions:
          address:
            description: IPv4 address (e.g., '192.168.1.1')
            type: str
            required: true
          subnet_mask:
            description: Subnet mask (e.g., '255.255.255.0')
            type: str
            required: true
      ipv6:
        description: List of IPv6 addresses to configure
        type: list
        elements: dict
        suboptions:
          address:
            description: IPv6 address with prefix length (e.g., '2001:db8::1/64')
            type: str
            required: true
  state:
    description:
      - Desired state of the configuration.
      - C(merged) - Add configured IPv4 and IPv6 addresses without removing existing addresses.
      - C(replaced) - Synchronize explicitly declared address fields for the listed interfaces only.
      - C(gathered) - Gather interface state without changing the device.
      - C(rendered) - Render CLI commands without connecting to the device.
    type: str
    default: merged
    choices: ['merged', 'replaced', 'gathered', 'rendered']
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Configure IPv4 address on VLAN interface
  c1emon.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 100
        ipv4:
          - address: 192.168.100.1
            subnet_mask: 255.255.255.0
    state: merged

- name: Configure IPv4 and IPv6 on VLAN interface
  c1emon.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 1
        ipv4:
          - address: 10.0.0.1
            subnet_mask: 255.255.255.0
        ipv6:
          - address: 2001:db8::1/64
    state: merged

- name: Replace IPv4 on a specific VLAN interface
  c1emon.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 10
        ipv4:
          - address: 172.16.0.1
            subnet_mask: 255.255.0.0
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
    - interface vlan-interface 100
    - ip address 192.168.100.1 255.255.255.0
gathered:
  description: VLAN interface state gathered from the device when I(state) is C(gathered).
  returned: when I(state) is C(gathered)
  type: dict
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.l3_interfaces import (
    L3InterfacesFacts,
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
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    load_config,
)
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule as AnsibleModuleType

L3InterfaceConfig = dict[str, Any]
L3InterfaceState = dict[str, L3InterfaceConfig]

L3_POLICY = ResourcePolicy(
    identity=("name",),
    fields={
        "ipv4": FieldPolicy(kind="set", identity=("address", "subnet_mask")),
        "ipv6": FieldPolicy(kind="set", identity=("address",)),
    },
)


def _normalize_l3_name(name: str) -> str:
    name = str(name).strip()
    return (
        name if name.startswith("vlan-interface") else "vlan-interface {0}".format(name)
    )


def _normalize_l3_resource(resource: L3InterfaceConfig) -> L3InterfaceConfig:
    normalized: L3InterfaceConfig = {}
    if resource.get("ipv4") is not None:
        normalized["ipv4"] = [dict(address) for address in resource["ipv4"]]
    if resource.get("ipv6") is not None:
        ipv6_addresses = []
        for address in resource["ipv6"]:
            item = dict(address)
            if "subnet" in item and "/" not in str(item.get("address", "")):
                item["address"] = "{0}/{1}".format(item["address"], item["subnet"])
            item.pop("subnet", None)
            ipv6_addresses.append(item)
        normalized["ipv6"] = ipv6_addresses
    return normalized


def _normalize_l3_state(state: L3InterfaceState) -> L3InterfaceState:
    normalized: L3InterfaceState = {}
    for name, config in (state or {}).items():
        interface_name = _normalize_l3_name(config.get("name", name))
        if interface_name in normalized:
            raise ReconciliationInputError(
                "duplicate L3 interface config: {0}".format(interface_name)
            )
        normalized[interface_name] = _normalize_l3_resource(config)
    return normalized


def _build_l3_state(config_list: list[L3InterfaceConfig]) -> L3InterfaceState:
    desired: L3InterfaceState = {}
    for config in config_list:
        interface_name = _normalize_l3_name(config["name"])
        if interface_name in desired:
            raise ReconciliationInputError(
                "duplicate L3 interface config: {0}".format(interface_name)
            )
        desired[interface_name] = _normalize_l3_resource(config)
    return desired


def _render_l3_operations(operations: list[Operation]) -> list[str]:
    commands: list[str] = []
    current_resource = None

    for operation in operations:
        if operation.resource != current_resource:
            commands.append("interface {0}".format(operation.resource[0][1]))
            current_resource = operation.resource

        if operation.field == "ipv4":
            address = operation.value["address"]
            mask = operation.value["subnet_mask"]
            if operation.action == "add_item":
                commands.append("ip address {0} {1}".format(address, mask))
            elif operation.action == "remove_item":
                commands.append("no ip address {0} {1}".format(address, mask))
            else:
                raise ReconciliationInputError(
                    "unsupported L3 operation: {0}".format(operation.action)
                )
            continue

        if operation.field == "ipv6":
            address = operation.value["address"]
            if operation.action == "add_item":
                commands.append("ipv6 address {0}".format(address))
            elif operation.action == "remove_item":
                commands.append("no ipv6 address {0}".format(address))
            else:
                raise ReconciliationInputError(
                    "unsupported L3 operation: {0}".format(operation.action)
                )
            continue

        raise ReconciliationInputError(
            "unsupported L3 field: {0}".format(operation.field)
        )

    return commands


def _render_l3_operation(operation: Operation) -> list[str]:
    """Render one acknowledged L3 operation for sealed planning."""
    return _render_l3_operations([operation])


def build_lifecycle_plan(
    config_list: list[L3InterfaceConfig],
    state: str,
    existing_config: L3InterfaceState,
) -> ResourcePlan:
    """Build one fully rendered L3 transition without recomputing its diff."""
    before = _normalize_l3_state(existing_config)
    desired = _build_l3_state(config_list)
    operations = plan_operations(before, desired, state, L3_POLICY)
    return seal_resource_plan(
        before, operations, L3_POLICY, _render_l3_operation, state
    )


def build_commands(
    config: L3InterfaceConfig, existing_config: L3InterfaceState
) -> list[str]:
    """Compatibility wrapper around the sealed one-resource plan."""
    return list(build_lifecycle_plan([config], "replaced", existing_config).commands)


def build_lifecycle_commands(
    config_list: list[L3InterfaceConfig],
    state: str,
    existing_config: L3InterfaceState,
) -> list[str]:
    """Build commands for all requested L3 interface configs."""
    return list(build_lifecycle_plan(config_list, state, existing_config).commands)


def build_after_state(
    before: L3InterfaceState,
    desired: list[L3InterfaceConfig],
    state: str,
) -> L3InterfaceState:
    """Build the expected normalized L3 interface state after lifecycle execution."""
    return build_lifecycle_plan(desired, state, before).after


def gather_l3_interfaces(module: "AnsibleModuleType") -> L3InterfaceState:
    """Gather L3 interface facts required for idempotent diffing."""
    return gather_with_error_boundary(
        module,
        lambda: _normalize_l3_state(L3InterfacesFacts(module).get_facts()),
        "failed to gather L3 interface facts",
        "l3_interfaces",
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
                    ipv4=dict(
                        type="list",
                        elements="dict",
                        options=dict(
                            address=dict(type="str", required=True),
                            subnet_mask=dict(type="str", required=True),
                        ),
                    ),
                    ipv6=dict(
                        type="list",
                        elements="dict",
                        options=dict(
                            address=dict(type="str", required=True),
                        ),
                    ),
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
        gather=gather_l3_interfaces,
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
