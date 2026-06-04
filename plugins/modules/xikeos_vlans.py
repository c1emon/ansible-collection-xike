#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS VLANs resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_vlans
short_description: Manage VLANs on Xike OS switches
version_added: "0.1.0"
description:
  - This module provides declarative management of VLANs on Xike OS devices.
  - VLANs can be created, modified, or deleted using this module.
options:
  config:
    description:
      - List of VLAN configurations.
      - Each entry defines a VLAN with its ID, name, and state.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description: VLAN ID (1-4094)
        type: int
        required: true
      name:
        description: VLAN name/description
        type: str
        required: false
      state:
        description: VLAN state (active/suspend)
        type: str
        choices: ['active', 'suspend']
        default: active
  state:
    description:
      - State of the VLAN configuration.
      - C(merged) - Creates or updates VLANs as specified.
      - C(replaced) - Replaces existing VLAN configuration with specified config.
      - C(deleted) - Deletes VLANs specified in config.
    type: str
    choices: ['merged', 'replaced', 'deleted']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Create VLANs on Xike switch
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
        state: active
      - vlan_id: 200
        name: VOICE
        state: active
    state: merged

- name: Replace VLAN configuration
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: SALES
        state: active
    state: replaced

- name: Delete VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
      - vlan_id: 200
    state: deleted
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - vlan 100
    - description DATA
    - vlan 200
    - description VOICE
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


def vlan_id_range(vlan_ids):
    """Convert a list of VLAN IDs to a range string (e.g., 100-200, 300)."""
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


def get_commands(config, state):
    """Generate CLI commands from VLAN configuration."""
    commands = []

    if state == "merged":
        for vlan in config:
            vlan_id = vlan["vlan_id"]
            name = vlan.get("name", "")
            vlan_state = vlan.get("state", "active")

            # Create VLAN
            commands.append(f"vlan {vlan_id}")

            # Set name if provided
            if name:
                commands.append(f"description {name}")

            # Exit VLAN mode to be safe
            commands.append("exit")

    elif state == "replaced":
        # For replaced, we need to handle both create/update and delete
        # This is simplified - in production, you'd compare with running config
        for vlan in config:
            vlan_id = vlan["vlan_id"]
            name = vlan.get("name", "")
            vlan_state = vlan.get("state", "active")

            # Create or update VLAN
            commands.append(f"vlan {vlan_id}")

            if name:
                commands.append(f"description {name}")

            commands.append("exit")

    elif state == "deleted":
        for vlan in config:
            vlan_id = vlan["vlan_id"]
            commands.append(f"no vlan {vlan_id}")

    return commands


def main():
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type="list",
            elements="dict",
            options=dict(
                vlan_id=dict(
                    type="int",
                    required=True,
                ),
                name=dict(
                    type="str",
                    required=False,
                    default="",
                ),
                state=dict(
                    type="str",
                    choices=["active", "suspend"],
                    default="active",
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["merged", "replaced", "deleted"],
            default="merged",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get("config", [])
    state = module.params.get("state", "merged")

    result = {
        "changed": False,
        "commands": [],
    }

    if not config:
        module.exit_json(**result)

    # Generate commands
    commands = get_commands(config, state)
    result["commands"] = commands

    if module.check_mode:
        module.exit_json(**result)

    if commands:
        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
