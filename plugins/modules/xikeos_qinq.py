#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS QinQ resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping

DOCUMENTATION = """
module: xikeos_qinq
short_description: Manage QinQ configuration on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of QinQ (VLAN stacking)
    on Xike OS devices.
  - Supports configuring QinQ mode, inner/outer TPID, VLAN insert,
    VLAN pass-through, and VLAN swap rules.
options:
  config:
    description:
      - QinQ configuration to apply on the device.
    type: dict
    suboptions:
      mode:
        description: QinQ mode (customer or uplink).
        type: str
        choices: ['customer', 'uplink']
      inner_tpid:
        description: Inner TPID value (e.g. 0x8100).
        type: str
      outer_tpid:
        description: Outer TPID value (e.g. 0x88a8).
        type: str
      vlan_inserts:
        description: List of VLAN insert rules.
        type: list
        elements: dict
        suboptions:
          start_vlan:
            description: Start VLAN ID.
            type: int
            required: true
          end_vlan:
            description: End VLAN ID.
            type: int
            required: true
          service_vlan:
            description: Service (outer) VLAN ID.
            type: int
            required: true
          priority:
            description: Priority value.
            type: int
      vlan_pass_throughs:
        description: List of VLAN pass-through rules.
        type: list
        elements: dict
        suboptions:
          start_vlan:
            description: Start VLAN ID.
            type: int
            required: true
          end_vlan:
            description: End VLAN ID.
            type: int
            required: true
      vlan_swaps:
        description: List of VLAN swap rules.
        type: list
        elements: dict
        suboptions:
          start_vlan:
            description: Start VLAN ID.
            type: int
            required: true
          end_vlan:
            description: End VLAN ID.
            type: int
            required: true
          swap_vlan:
            description: Swap (outer) VLAN ID.
            type: int
            required: true
          priority:
            description: Priority value for the swap rule.
            type: int
  state:
    description:
      - State of the QinQ configuration.
      - C(merged) - Creates or updates QinQ settings as specified.
      - C(replaced) - Replaces existing QinQ configuration with specified config.
      - C(deleted) - Removes QinQ configuration.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'rendered']
    default: merged
author: clemon
"""

EXAMPLES = """
- name: Set QinQ mode to customer with TPIDs
  c1emon.xikeos.xikeos_qinq:
    config:
      mode: customer
      inner_tpid: "0x8100"
      outer_tpid: "0x88a8"
    state: merged

- name: Configure VLAN insert rules
  c1emon.xikeos.xikeos_qinq:
    config:
      vlan_inserts:
        - start_vlan: 100
          end_vlan: 200
          service_vlan: 500
        - start_vlan: 300
          end_vlan: 399
          service_vlan: 600
          priority: 5
    state: merged

- name: Configure VLAN pass-through rules
  c1emon.xikeos.xikeos_qinq:
    config:
      vlan_pass_throughs:
        - start_vlan: 10
          end_vlan: 20
    state: merged

- name: Configure VLAN swap rules
  c1emon.xikeos.xikeos_qinq:
    config:
      vlan_swaps:
        - start_vlan: 100
          end_vlan: 199
          swap_vlan: 900
          priority: 3
    state: merged

- name: Delete QinQ configuration
  c1emon.xikeos.xikeos_qinq:
    config: {}
    state: deleted
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - qinq mode customer
    - qinq inner-tpid 0x8100
    - qinq outer-tpid 0x88a8
    - vlan insert 100 200 500
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render QinQ CLI commands for the requested state."""
    commands = []

    if state == "deleted":
        # Remove all QinQ configuration
        commands.append("no qinq mode")
        commands.append("no qinq inner-tpid")
        commands.append("no qinq outer-tpid")
        return commands

    if not config:
        return commands

    # QinQ mode
    mode = config.get("mode")
    if mode:
        commands.append("qinq mode {0}".format(mode))

    # Inner TPID
    inner_tpid = config.get("inner_tpid")
    if inner_tpid:
        commands.append("qinq inner-tpid {0}".format(inner_tpid))

    # Outer TPID
    outer_tpid = config.get("outer_tpid")
    if outer_tpid:
        commands.append("qinq outer-tpid {0}".format(outer_tpid))

    # VLAN insert rules
    vlan_inserts = config.get("vlan_inserts") or []
    for rule in vlan_inserts:
        start_vlan = rule["start_vlan"]
        end_vlan = rule["end_vlan"]
        service_vlan = rule["service_vlan"]
        priority = rule.get("priority")
        cmd = "vlan insert {0} {1} {2}".format(start_vlan, end_vlan, service_vlan)
        if priority is not None:
            cmd += " {0}".format(priority)
        commands.append(cmd)

    # VLAN pass-through rules
    vlan_pass_throughs = config.get("vlan_pass_throughs") or []
    for rule in vlan_pass_throughs:
        start_vlan = rule["start_vlan"]
        end_vlan = rule["end_vlan"]
        commands.append("vlan pass-through {0} {1}".format(start_vlan, end_vlan))

    # VLAN swap rules
    vlan_swaps = config.get("vlan_swaps") or []
    for rule in vlan_swaps:
        start_vlan = rule["start_vlan"]
        end_vlan = rule["end_vlan"]
        swap_vlan = rule["swap_vlan"]
        priority = rule.get("priority")
        cmd = "vlan swap {0} {1} {2}".format(start_vlan, end_vlan, swap_vlan)
        if priority is not None:
            cmd += " priority {0}".format(priority)
        commands.append(cmd)

    return commands


def main() -> None:
    """Run the QinQ module entry point."""
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                mode=dict(
                    type="str",
                    choices=["customer", "uplink"],
                ),
                inner_tpid=dict(
                    type="str",
                ),
                outer_tpid=dict(
                    type="str",
                ),
                vlan_inserts=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        start_vlan=dict(type="int", required=True),
                        end_vlan=dict(type="int", required=True),
                        service_vlan=dict(type="int", required=True),
                        priority=dict(type="int"),
                    ),
                ),
                vlan_pass_throughs=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        start_vlan=dict(type="int", required=True),
                        end_vlan=dict(type="int", required=True),
                    ),
                ),
                vlan_swaps=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        start_vlan=dict(type="int", required=True),
                        end_vlan=dict(type="int", required=True),
                        swap_vlan=dict(type="int", required=True),
                        priority=dict(type="int"),
                    ),
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["merged", "replaced", "deleted", "rendered"],
            default="merged",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get("config")
    state = module.params.get("state", "merged")

    exit_rendered_or_fail(module, "xikeos_qinq", config, state, get_commands, "merged")


if __name__ == "__main__":
    main()
