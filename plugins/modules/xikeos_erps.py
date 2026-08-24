#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS ERPS (G.8032) resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_erps
short_description: Manage ERPS (G.8032) ring protection on Xike OS devices
version_added: "0.1.0"
description:
  - This module currently only supports C(state=rendered) to generate CLI
    commands for ERPS; it does not connect to or apply configuration on the
    device.
  - Mutating lifecycle states such as C(present) and C(absent) are present in
    the argument schema for future support, but they are currently unsupported
    and fail when configuration is supplied.
  - This module provides declarative management of Ethernet Ring Protection
    Switching (ERPS) as defined in ITU-T G.8032 on Xike OS devices.
  - Supports configuration of ERPS instances, control VLANs, port roles,
    protected instances, and ring protection parameters.
options:
  instance_id:
    description:
      - ERPS instance identifier.
    type: int
    required: true
  control_vlan:
    description:
      - VLAN ID used as the control VLAN for the ERPS instance.
    type: int
  port0:
    description:
      - Configuration for Port0 of the ERPS ring.
      - Format is "ethernet <port-id>" or "eth-trunk <lag-id>" optionally
        followed by a role keyword (neighbour, next-neighbour, owner).
    type: str
  port1:
    description:
      - Configuration for Port1 of the ERPS ring.
      - Format is "ethernet <port-id>" or "eth-trunk <lag-id>" optionally
        followed by a role keyword (neighbour, next-neighbour, owner).
    type: str
  work_mode:
    description:
      - ERPS work mode (revertive or non-revertive).
    type: str
    choices: ['non-revertive', 'revertive']
  protected_instances:
    description:
      - MSTP instances protected by this ERPS instance.
      - Specified as a range string, e.g. "1,2,5-10".
    type: str
  ring_enable:
    description:
      - Enable or disable the ERPS ring.
    type: bool
    default: true
  guard_timer:
    description:
      - Guard timer value in centiseconds (0-3000).
    type: int
  mel:
    description:
      - Management Entity Level (0-7).
    type: int
  wtr_timer:
    description:
      - Wait-to-Restore timer value in minutes (1-120).
    type: int
  state:
    description:
      - State of the ERPS configuration.
      - C(rendered) - Generates CLI commands only.
      - C(present) and C(absent) are currently unsupported and fail when
        configuration is supplied.
    type: str
    choices: ['present', 'absent', 'rendered']
    default: present
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Render ERPS instance 1 commands with control VLAN 100
  c1emon.xikeos.xikeos_erps:
    instance_id: 1
    control_vlan: 100
    port0: "ethernet 1 owner"
    port1: "ethernet 2 neighbour"
    work_mode: revertive
    protected_instances: "1,2,3"
    ring_enable: true
    guard_timer: 500
    wtr_timer: 5
    mel: 5
    state: rendered

- name: Render ERPS instance 2 commands with LAG ports
  c1emon.xikeos.xikeos_erps:
    instance_id: 2
    control_vlan: 200
    port0: "eth-trunk 1 owner"
    port1: "eth-trunk 2 next-neighbour"
    work_mode: non-revertive
    protected_instances: "10-20"
    ring_enable: true
    state: rendered

- name: Render ERPS instance 1 commands
  c1emon.xikeos.xikeos_erps:
    instance_id: 1
    state: rendered
"""

RETURN = """
changed:
  description: Whether the module changed the device configuration.
  returned: always
  type: bool
commands:
  description: List of commands rendered for the device.
  returned: always
  type: list
  sample:
    - erps
    - erps instance 1
    - control-vlan 100
    - port0 ethernet 1 owner
    - port1 ethernet 2 neighbour
    - work-mode revertive
    - protected-instance 1,2,3
    - ring enable
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from typing import Any, Mapping, Sequence

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def vlan_id_to_ranges(vlan_ids: Sequence[int]) -> str:
    """Convert VLAN IDs into the compact ranges used in ERPS commands."""
    if not vlan_ids:
        return ""
    sorted_ids = sorted(set(vlan_ids))
    ranges = []
    start = sorted_ids[0]
    end = sorted_ids[0]

    for vid in sorted_ids[1:]:
        if vid == end + 1:
            end = vid
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = vid
            end = vid

    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ",".join(ranges)


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render ERPS CLI commands for the requested configuration state."""
    commands = []

    instance_id = config.get("instance_id")
    if instance_id is None:
        return commands

    if state == "absent":
        commands.append("erps")
        commands.append(f"no erps instance {instance_id}")
        return commands

    # Enter ERPS global mode
    commands.append("erps")

    # Enter ERPS instance mode
    commands.append(f"erps instance {instance_id}")

    # Control VLAN
    control_vlan = config.get("control_vlan")
    if control_vlan is not None:
        commands.append(f"control-vlan {control_vlan}")

    # Port0
    port0 = config.get("port0")
    if port0:
        commands.append(f"port0 {port0}")

    # Port1
    port1 = config.get("port1")
    if port1:
        commands.append(f"port1 {port1}")

    # Work mode
    work_mode = config.get("work_mode")
    if work_mode:
        commands.append(f"work-mode {work_mode}")

    # Protected instances
    protected_instances = config.get("protected_instances")
    if protected_instances:
        commands.append(f"protected-instance {protected_instances}")

    # Guard timer
    guard_timer = config.get("guard_timer")
    if guard_timer is not None:
        commands.append(f"guard-timer {guard_timer}")

    # MEL
    mel = config.get("mel")
    if mel is not None:
        commands.append(f"mel {mel}")

    # WTR timer
    wtr_timer = config.get("wtr_timer")
    if wtr_timer is not None:
        commands.append(f"wtr-timer {wtr_timer}")

    # Ring enable
    ring_enable = config.get("ring_enable")
    if ring_enable is True:
        commands.append("ring enable")
    elif ring_enable is False:
        commands.append("no ring enable")

    return commands


def main() -> None:
    """Run the ERPS module entry point."""
    module_args = dict(
        instance_id=dict(
            type="int",
            required=True,
        ),
        control_vlan=dict(
            type="int",
        ),
        port0=dict(
            type="str",
        ),
        port1=dict(
            type="str",
        ),
        work_mode=dict(
            type="str",
            choices=["non-revertive", "revertive"],
        ),
        protected_instances=dict(
            type="str",
        ),
        ring_enable=dict(
            type="bool",
            default=True,
        ),
        guard_timer=dict(
            type="int",
        ),
        mel=dict(
            type="int",
        ),
        wtr_timer=dict(
            type="int",
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
    for key in ("instance_id", "control_vlan", "port0", "port1", "work_mode",
                "protected_instances", "ring_enable", "guard_timer", "mel",
                "wtr_timer"):
        val = module.params.get(key)
        if val is not None:
            config[key] = val

    exit_rendered_or_fail(module, "xikeos_erps", config, state, get_commands, "present")


if __name__ == "__main__":
    main()
