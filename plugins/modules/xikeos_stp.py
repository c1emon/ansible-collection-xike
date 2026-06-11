#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS STP resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping, Sequence

DOCUMENTATION = """
module: xikeos_stp
short_description: Manage STP settings on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of Spanning Tree Protocol (STP)
    on Xike OS devices.
  - Supports STP, RSTP, MSTP, PVST, and Rapid-PVST modes.
  - Configures global STP parameters, MSTP regions/instances, and PVST instances.
options:
  config:
    description:
      - STP configuration to apply on the device.
    type: dict
    suboptions:
      stp_mode:
        description: STP protocol mode to enable.
        type: str
        choices: ['stp', 'rstp', 'mstp', 'pvst', 'rapid-pvst']
      priority:
        description: Bridge priority value (0-61440, in steps of 4096).
        type: int
      hello_time:
        description: Hello BPDU interval in seconds (1-10).
        type: int
      forward_time:
        description: Forward delay time in seconds (4-30).
        type: int
      max_age:
        description: Maximum age of BPDU in seconds (6-40).
        type: int
      pathcost_standard:
        description: Path cost calculation standard.
        type: str
        choices: ['dot1d-1998', 'dot1t']
      bpdu_guard:
        description: Enable BPDU guard globally.
        type: bool
      bpdu_filter:
        description: Enable BPDU filter globally.
        type: bool
      mstp:
        description: MSTP-specific configuration.
        type: dict
        suboptions:
          region_name:
            description: MSTP region name.
            type: str
          revision:
            description: MSTP revision level (0-65535).
            type: int
          instances:
            description: List of MSTP instance configurations.
            type: list
            elements: dict
            suboptions:
              instance_id:
                description: MSTP instance ID (0-15).
                type: int
                required: true
              priority:
                description: Priority for this MSTP instance (0-61440).
                type: int
              vlans:
                description: VLANs mapped to this MSTP instance.
                type: list
                elements: int
      pvst:
        description: PVST-specific configuration.
        type: dict
        suboptions:
          instances:
            description: List of PVST instance configurations.
            type: list
            elements: dict
            suboptions:
              instance_id:
                description: PVST instance ID (usually VLAN ID).
                type: int
                required: true
              vlan_id:
                description: VLAN ID for this PVST instance.
                type: int
  state:
    description:
      - State of the STP configuration.
      - C(merged) - Creates or updates STP settings as specified.
      - C(replaced) - Replaces existing STP configuration with specified config.
    type: str
    choices: ['merged', 'replaced', 'rendered']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Enable STP with RSTP mode
  xike.xikeos.xikeos_stp:
    config:
      stp_mode: rstp
      priority: 32768
      hello_time: 2
      forward_time: 15
      max_age: 20
    state: merged

- name: Configure MSTP with region and instances
  xike.xikeos.xikeos_stp:
    config:
      stp_mode: mstp
      mstp:
        region_name: MY_REGION
        revision: 1
        instances:
          - instance_id: 1
            priority: 8192
            vlans: [10, 20, 30]
          - instance_id: 2
            priority: 16384
            vlans: [100, 200]
    state: merged

- name: Configure PVST instances
  xike.xikeos.xikeos_stp:
    config:
      stp_mode: pvst
      pvst:
        instances:
          - instance_id: 10
            vlan_id: 10
          - instance_id: 20
            vlan_id: 20
    state: merged

- name: Enable BPDU guard and set pathcost standard
  xike.xikeos.xikeos_stp:
    config:
      stp_mode: rstp
      bpdu_guard: true
      bpdu_filter: false
      pathcost_standard: dot1t
    state: merged
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - stp
    - stp mode rstp
    - stp priority 32768
    - stp hello-time 2
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def vlan_id_to_ranges(vlan_ids: Sequence[int]) -> str:
    """Convert VLAN IDs into the compact range strings used by STP."""
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
    """Render STP CLI commands for the requested configuration state."""
    commands = []

    if not config:
        return commands

    # Enable STP first
    commands.append("stp")

    stp_mode = config.get("stp_mode")
    if stp_mode:
        commands.append(f"stp mode {stp_mode}")

    priority = config.get("priority")
    if priority is not None:
        commands.append(f"stp priority {priority}")

    hello_time = config.get("hello_time")
    if hello_time is not None:
        commands.append(f"stp hello-time {hello_time}")

    forward_time = config.get("forward_time")
    if forward_time is not None:
        commands.append(f"stp forward-time {forward_time}")

    max_age = config.get("max_age")
    if max_age is not None:
        commands.append(f"stp max-age {max_age}")

    pathcost_standard = config.get("pathcost_standard")
    if pathcost_standard:
        commands.append(f"stp pathcost-standard {pathcost_standard}")

    bpdu_guard = config.get("bpdu_guard")
    if bpdu_guard is True:
        commands.append("stp bpdu-guard")
    elif bpdu_guard is False:
        commands.append("no stp bpdu-guard")

    bpdu_filter = config.get("bpdu_filter")
    if bpdu_filter is True:
        commands.append("stp bpdu-filter")
    elif bpdu_filter is False:
        commands.append("no stp bpdu-filter")

    # MSTP configuration
    mstp = config.get("mstp")
    if mstp:
        region_name = mstp.get("region_name")
        if region_name:
            commands.append(f"mstp region-name {region_name}")

        revision = mstp.get("revision")
        if revision is not None:
            commands.append(f"mstp revision-level {revision}")

        instances = mstp.get("instances", [])
        for inst in instances:
            instance_id = inst.get("instance_id")
            priority = inst.get("priority")
            vlans = inst.get("vlans", [])

            if priority is not None:
                commands.append(f"mstp instance {instance_id} priority {priority}")

            if vlans:
                vlan_str = vlan_id_to_ranges(vlans)
                commands.append(f"mstp instance {instance_id} vlan {vlan_str}")

    # PVST configuration
    pvst = config.get("pvst")
    if pvst:
        instances = pvst.get("instances", [])
        for inst in instances:
            instance_id = inst.get("instance_id")
            vlan_id = inst.get("vlan_id")
            if instance_id is not None and vlan_id is not None:
                commands.append(f"pvst instance {instance_id} vlan {vlan_id}")

    return commands


def main() -> None:
    """Run the STP module entry point."""
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                stp_mode=dict(
                    type="str",
                    choices=["stp", "rstp", "mstp", "pvst", "rapid-pvst"],
                ),
                priority=dict(
                    type="int",
                ),
                hello_time=dict(
                    type="int",
                ),
                forward_time=dict(
                    type="int",
                ),
                max_age=dict(
                    type="int",
                ),
                pathcost_standard=dict(
                    type="str",
                    choices=["dot1d-1998", "dot1t"],
                ),
                bpdu_guard=dict(
                    type="bool",
                ),
                bpdu_filter=dict(
                    type="bool",
                ),
                mstp=dict(
                    type="dict",
                    options=dict(
                        region_name=dict(type="str"),
                        revision=dict(type="int"),
                        instances=dict(
                            type="list",
                            elements="dict",
                            options=dict(
                                instance_id=dict(type="int", required=True),
                                priority=dict(type="int"),
                                vlans=dict(
                                    type="list",
                                    elements="int",
                                ),
                            ),
                        ),
                    ),
                ),
                pvst=dict(
                    type="dict",
                    options=dict(
                        instances=dict(
                            type="list",
                            elements="dict",
                            options=dict(
                                instance_id=dict(type="int", required=True),
                                vlan_id=dict(type="int"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["merged", "replaced", "rendered"],
            default="merged",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get("config", {})
    state = module.params.get("state", "merged")

    exit_rendered_or_fail(module, "xikeos_stp", config, state, get_commands, "merged")


if __name__ == "__main__":
    main()
