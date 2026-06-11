#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS port mirroring resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping

DOCUMENTATION = """
module: xikeos_mirror
short_description: Manage port mirroring on Xike OS switches
version_added: "0.1.0"
description:
  - Configure port mirroring (mirror groups) on Xike OS devices.
  - Add or remove source interfaces and destination interfaces for mirror groups.
options:
  config:
    description:
      - Mirror group configuration.
      - Defines the mirror group ID, source interfaces, and destination interface.
    type: dict
    suboptions:
      group_id:
        description: Mirror group ID (numeric identifier).
        type: int
        required: true
      source_interfaces:
        description:
          - List of source interfaces to mirror traffic from.
          - Each entry specifies an interface name and direction.
        type: list
        elements: dict
        suboptions:
          name:
            description:
              - Interface name, e.g. C(ethernet 0/0/1) or C(cpu).
            type: str
            required: true
          direction:
            description: Traffic direction to mirror.
            type: str
            choices: ['ingress', 'egress', 'both']
            default: both
      destination_interface:
        description:
          - Destination interface for mirrored traffic.
          - Must be an Ethernet interface, e.g. C(ethernet 0/0/1).
        type: str
  state:
    description:
      - State of the mirror group configuration.
      - C(present) - Creates or updates the mirror group.
      - C(absent) - Removes the mirror group or specified source interfaces.
    type: str
    choices: ['present', 'absent', 'rendered']
    default: present
author: clemon
"""

EXAMPLES = """
- name: Create a mirror group with source and destination
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: ethernet 0/0/1
          direction: both
        - name: ethernet 0/0/2
          direction: ingress
      destination_interface: ethernet 0/0/10
    state: present

- name: Add a CPU source to an existing mirror group
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: cpu
          direction: both
    state: present

- name: Remove a specific source interface from a mirror group
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: ethernet 0/0/2
    state: absent

- name: Delete an entire mirror group
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
    state: absent
"""

RETURN = """
commands:
  description: CLI commands sent to the device
  returned: always
  type: list
  sample:
    - mirror group 1 source-interface ethernet 0/0/1 both
    - mirror group 1 source-interface ethernet 0/0/2 ingress
    - mirror group 1 destination-interface ethernet 0/0/10
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def _format_port(port_spec: Mapping[str, str] | None) -> str | None:
    """Format a port spec into the CLI form used by mirror commands."""
    if not port_spec:
        return None
    return "{0} {1}".format(port_spec["type"], port_spec["id"])


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render mirror-group CLI commands for the requested state."""
    commands = []
    group_id = config.get("group_id")

    if group_id is None:
        return commands

    source_interfaces = config.get("source_interfaces") or []
    destination_interface = config.get("destination_interface")

    if state == "present":
        # Add source interfaces
        for src in source_interfaces:
            name = src.get("name")
            direction = src.get("direction", "both")
            if not name:
                continue
            if name.lower() == "cpu":
                commands.append(
                    "mirror group {gid} source-interface cpu {dir}".format(
                        gid=group_id, dir=direction
                    )
                )
            else:
                commands.append(
                    "mirror group {gid} source-interface {name} {dir}".format(
                        gid=group_id, name=name, dir=direction
                    )
                )

        # Set destination interface
        if destination_interface:
            commands.append(
                "mirror group {gid} destination-interface {name}".format(
                    gid=group_id, name=destination_interface
                )
            )

    elif state == "absent":
        if source_interfaces:
            # Remove specific source interfaces
            for src in source_interfaces:
                name = src.get("name")
                if not name:
                    continue
                if name.lower() == "cpu":
                    commands.append(
                        "no mirror group {gid} source-interface cpu".format(
                            gid=group_id
                        )
                    )
                else:
                    commands.append(
                        "no mirror group {gid} source-interface {name}".format(
                            gid=group_id, name=name
                        )
                    )
        elif destination_interface:
            # Remove destination interface
            commands.append(
                "no mirror group {gid} destination-interface {name}".format(
                    gid=group_id, name=destination_interface
                )
            )
        else:
            # Remove all source interfaces and destination
            # When no specific items given, remove the whole group's config
            commands.append(
                "no mirror group {gid} source-interface cpu".format(gid=group_id)
            )
            commands.append(
                "no mirror group {gid} destination-interface ethernet 0/0/1".format(
                    gid=group_id
                )
            )

    return commands


def main() -> None:
    """Run the port mirroring module entry point."""
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                group_id=dict(
                    type="int",
                    required=True,
                ),
                source_interfaces=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        name=dict(
                            type="str",
                            required=True,
                        ),
                        direction=dict(
                            type="str",
                            choices=["ingress", "egress", "both"],
                            default="both",
                        ),
                    ),
                ),
                destination_interface=dict(
                    type="str",
                    default=None,
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["present", "absent", "rendered"],
            default="present",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ("state", "present", ["config"]),
        ],
        supports_check_mode=True,
    )

    config = module.params.get("config") or {}
    state = module.params.get("state", "present")

    exit_rendered_or_fail(module, "xikeos_mirror", config, state, get_commands, "present")


if __name__ == "__main__":
    main()
