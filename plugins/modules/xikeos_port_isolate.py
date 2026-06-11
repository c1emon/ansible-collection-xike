#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS port isolation resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping

DOCUMENTATION = """
module: xikeos_port_isolate
short_description: Manage port isolation groups on Xike OS switches
version_added: "0.1.0"
description:
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
  state:
    description:
      - State of the port isolation group configuration.
      - C(present) - Creates or updates the port isolation group.
      - C(absent) - Removes the port isolation group or specified members.
    type: str
    choices: ['present', 'absent', 'rendered']
    default: present
author: Andy
"""

EXAMPLES = """
- name: Create a port isolation group with members
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/1
        - ethernet 0/0/2
        - ethernet 0/0/3
    state: present

- name: Add all ports to an isolation group
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 2
      members:
        - all
    state: present

- name: Remove specific members from an isolation group
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/2
    state: absent

- name: Delete a port isolation group
  c1emon.xikeos.xikeos_port_isolate:
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
    - interface port-isolate group 1
    - switchport ethernet 0/0/1
    - switchport ethernet 0/0/2
"""

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
