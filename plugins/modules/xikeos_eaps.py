#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS EAPS resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping

DOCUMENTATION = """
module: xikeos_eaps
short_description: Manage EAPS (Ethernet Automatic Protection Switching) on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of EAPS (Ethernet Automatic
    Protection Switching) domains on Xike OS devices.
  - Supports configuration of EAPS domains, control VLANs, ring roles,
    work modes, and ring enable/disable states.
options:
  domain_id:
    description:
      - EAPS domain identifier.
    type: int
    required: true
  control_vlan:
    description:
      - VLAN ID used as the control VLAN for the EAPS domain.
    type: int
  rings:
    description:
      - List of ring configurations for this EAPS domain.
    type: list
    elements: dict
    suboptions:
      ring_id:
        description: Ring identifier.
        type: int
        required: true
      role:
        description: Role of this node in the ring.
        type: str
        choices: ['master', 'transit']
      enabled:
        description: Enable or disable this ring.
        type: bool
        default: true
  work_mode:
    description:
      - EAPS work mode.
    type: str
    choices: ['eips-subring', 'rrpp', 'standard']
  state:
    description:
      - State of the EAPS configuration.
      - C(present) - Creates or updates the EAPS domain.
      - C(absent) - Removes the EAPS domain.
    type: str
    choices: ['present', 'absent', 'rendered']
    default: present
author: Andy
"""

EXAMPLES = """
- name: Configure EAPS domain 1 with standard mode
  c1emon.xikeos.xikeos_eaps:
    domain_id: 1
    control_vlan: 100
    work_mode: standard
    rings:
      - ring_id: 1
        role: master
        enabled: true
      - ring_id: 2
        role: transit
        enabled: true
    state: present

- name: Configure EAPS domain 2 with RRPP mode
  c1emon.xikeos.xikeos_eaps:
    domain_id: 2
    control_vlan: 200
    work_mode: rrpp
    rings:
      - ring_id: 1
        role: master
        enabled: true
    state: present

- name: Remove EAPS domain 1
  c1emon.xikeos.xikeos_eaps:
    domain_id: 1
    state: absent
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - eaps
    - eaps domain 1
    - control-vlan 100
    - work-mode standard
    - ring 1 enable
    - ring 1 role master
    - ring 2 enable
    - ring 2 role transit
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render EAPS CLI commands for the requested configuration state."""
    commands = []

    domain_id = config.get("domain_id")
    if domain_id is None:
        return commands

    if state == "absent":
        commands.append("eaps")
        commands.append(f"no eaps domain {domain_id}")
        return commands

    # Enter EAPS global mode
    commands.append("eaps")

    # Enter EAPS domain mode
    commands.append(f"eaps domain {domain_id}")

    # Control VLAN
    control_vlan = config.get("control_vlan")
    if control_vlan is not None:
        commands.append(f"control-vlan {control_vlan}")

    # Work mode
    work_mode = config.get("work_mode")
    if work_mode:
        commands.append(f"work-mode {work_mode}")

    # Rings
    rings = config.get("rings", [])
    for ring in rings:
        ring_id = ring.get("ring_id")
        if ring_id is None:
            continue

        role = ring.get("role")
        enabled = ring.get("enabled", True)

        if enabled is True:
            commands.append(f"ring {ring_id} enable")
        elif enabled is False:
            commands.append(f"ring {ring_id} disable")

        if role:
            commands.append(f"ring {ring_id} role {role}")

    return commands


def main() -> None:
    """Run the EAPS module entry point."""
    module_args = dict(
        domain_id=dict(
            type="int",
            required=True,
        ),
        control_vlan=dict(
            type="int",
        ),
        rings=dict(
            type="list",
            elements="dict",
            options=dict(
                ring_id=dict(
                    type="int",
                    required=True,
                ),
                role=dict(
                    type="str",
                    choices=["master", "transit"],
                ),
                enabled=dict(
                    type="bool",
                    default=True,
                ),
            ),
        ),
        work_mode=dict(
            type="str",
            choices=["eips-subring", "rrpp", "standard"],
        ),
        state=dict(
            type="str",
            choices=["present", "absent", "rendered"],
            default="present",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    state = module.params.get("state", "present")

    config = {}
    for key in ("domain_id", "control_vlan", "rings", "work_mode"):
        val = module.params.get(key)
        if val is not None:
            config[key] = val

    exit_rendered_or_fail(module, "xikeos_eaps", config, state, get_commands, "present")


if __name__ == "__main__":
    main()
