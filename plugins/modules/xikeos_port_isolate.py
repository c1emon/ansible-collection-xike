#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS port isolation resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_port_isolate
short_description: Manage port isolation groups on Xike OS switches
version_added: "0.1.0"
description:
  - This module currently only supports C(state=rendered) to generate CLI
    commands for port isolation groups; it does not connect to or apply
    configuration on the device.
  - C(present) and C(absent) are documented for future lifecycle support but
    are currently unsupported and fail when configuration is supplied.
  - Configure port isolation groups on Xike OS devices.
  - Ports in the same isolation group cannot communicate with each other,
    but can communicate with ports outside the group.
options:
  config:
    description:
      - Port isolation group configuration.
      - Defines the group ID and member interfaces.
    type: dict
    suboptions:
      group_id:
        description: Port isolation group ID (numeric identifier).
        type: int
        required: true
      members:
        description:
          - List of member interfaces in the isolation group.
          - Use C(all) to add all ports, or specify individual Ethernet ports
            like C(ethernet 0/0/1).
        type: list
        elements: str
        default: []
  state:
    description:
      - State of the port isolation group configuration.
      - C(rendered) - Generates CLI commands only.
      - C(present) and C(absent) are currently unsupported and fail when
        configuration is supplied.
    type: str
    choices: ['present', 'absent', 'rendered']
    default: present
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Render port isolation commands with members
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/1
        - ethernet 0/0/2
        - ethernet 0/0/3
    state: rendered

- name: Render port isolation commands for all ports
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 2
      members:
        - all
    state: rendered

- name: Render port isolation commands with specific members
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/2
    state: rendered

- name: Render port isolation commands for a group
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
    state: rendered
"""

RETURN = """
changed:
  description: Whether the module changed the device configuration.
  returned: always
  type: bool
commands:
  description: CLI commands rendered for the device.
  returned: always
  type: list
  sample:
    - interface port-isolate group 1
    - switchport ethernet 0/0/1
    - switchport ethernet 0/0/2
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from typing import Any, Mapping

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render port-isolation CLI commands for the requested state."""
    commands = []
    group_id = config.get("group_id")

    if group_id is None:
        return commands

    members = config.get("members") or []

    if state == "present":
        if members:
            # Enter port-isolate group mode and add members
            commands.append(
                "interface port-isolate group {gid}".format(gid=group_id)
            )
            for member in members:
                member_lower = member.strip().lower()
                if member_lower == "all":
                    commands.append("switchport all")
                else:
                    commands.append(
                        "switchport {member}".format(member=member)
                    )
            commands.append("exit")

    elif state == "absent":
        if members:
            # Remove specific members
            commands.append(
                "interface port-isolate group {gid}".format(gid=group_id)
            )
            for member in members:
                member_lower = member.strip().lower()
                if member_lower == "all":
                    commands.append("no switchport all")
                else:
                    commands.append(
                        "no switchport {member}".format(member=member)
                    )
            commands.append("exit")
        else:
            # Remove the entire group
            commands.append(
                "no interface port-isolate group {gid}".format(gid=group_id)
            )

    return commands


def main() -> None:
    """Run the port isolation module entry point."""
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                group_id=dict(
                    type="int",
                    required=True,
                ),
                members=dict(
                    type="list",
                    elements="str",
                    default=[],
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

    exit_rendered_or_fail(module, "xikeos_port_isolate", config, state, get_commands, "present")


if __name__ == "__main__":
    main()
