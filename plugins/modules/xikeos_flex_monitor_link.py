#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS Flex-Link and Monitor-Link resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Mapping

DOCUMENTATION = """
module: xikeos_flex_monitor_link
short_description: Manage Flex-Link and Monitor-Link on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of Flex-Link and Monitor-Link
    configurations on Xike OS devices.
  - Flex-Link provides backup link redundancy without STP.
  - Monitor-Link monitors uplink status and triggers downlink failover.
options:
  config:
    description:
      - Configuration to apply on the device.
    type: dict
    suboptions:
      flex_links:
        description: List of Flex-Link group configurations.
        type: list
        elements: dict
        suboptions:
          group_id:
            description: Flex-Link group ID.
            type: int
            required: true
          master_port:
            description: Master port specification.
            type: dict
            suboptions:
              type:
                description: Port type (eth or eth-trunk).
                type: str
                choices: ['eth', 'eth-trunk']
                required: true
              id:
                description: Port or trunk ID.
                type: str
                required: true
          slave_port:
            description: Slave (backup) port specification.
            type: dict
            suboptions:
              type:
                description: Port type (eth or eth-trunk).
                type: str
                choices: ['eth', 'eth-trunk']
                required: true
              id:
                description: Port or trunk ID.
                type: str
                required: true
          preemption_mode:
            description: Preemption mode for the Flex-Link group.
            type: str
            choices: ['role', 'bandwidth']
      monitor_links:
        description: List of Monitor-Link group configurations.
        type: list
        elements: dict
        suboptions:
          group_id:
            description: Monitor-Link group ID.
            type: int
            required: true
          uplink_port:
            description: Uplink port specification.
            type: dict
            suboptions:
              type:
                description: Port type (eth or eth-trunk).
                type: str
                choices: ['eth', 'eth-trunk']
                required: true
              id:
                description: Port or trunk ID.
                type: str
                required: true
          downlink_ports:
            description: List of downlink port specifications.
            type: list
            elements: dict
            suboptions:
              type:
                description: Port type (eth or eth-trunk).
                type: str
                choices: ['eth', 'eth-trunk']
                required: true
              id:
                description: Port or trunk ID.
                type: str
                required: true
  state:
    description:
      - State of the configuration.
      - C(merged) - Creates or updates Flex-Link/Monitor-Link settings.
      - C(replaced) - Replaces existing configuration.
      - C(deleted) - Deletes Flex-Link/Monitor-Link configuration.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'rendered']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Configure Flex-Link group
  c1emon.xikeos.xikeos_flex_monitor_link:
    config:
      flex_links:
        - group_id: 1
          master_port:
            type: eth
            id: "0/0/1"
          slave_port:
            type: eth
            id: "0/0/2"
          preemption_mode: role
    state: merged

- name: Configure Monitor-Link group
  c1emon.xikeos.xikeos_flex_monitor_link:
    config:
      monitor_links:
        - group_id: 1
          uplink_port:
            type: eth
            id: "0/0/1"
          downlink_ports:
            - type: eth
              id: "0/0/2"
            - type: eth
              id: "0/0/3"
    state: merged

- name: Configure Flex-Link with eth-trunk ports
  c1emon.xikeos.xikeos_flex_monitor_link:
    config:
      flex_links:
        - group_id: 2
          master_port:
            type: eth-trunk
            id: "1"
          slave_port:
            type: eth-trunk
            id: "2"
          preemption_mode: bandwidth
    state: merged

- name: Delete Flex-Link and Monitor-Link configuration
  c1emon.xikeos.xikeos_flex_monitor_link:
    config: {}
    state: deleted
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - flex-link group 1
    - master-port eth 0/0/1
    - slave-port eth 0/0/2
    - preemption mode role
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import exit_rendered_or_fail


def _format_port(port_spec: Mapping[str, str] | None) -> str | None:
    """Format a port spec into the CLI form used by link commands."""
    if not port_spec:
        return None
    return "{0} {1}".format(port_spec["type"], port_spec["id"])


def get_commands(config: Mapping[str, Any], state: str) -> list[str]:
    """Render Flex-Link and Monitor-Link CLI commands."""
    commands = []

    if state == "deleted":
        # Delete all flex-link groups
        commands.append("no flex-link group")
        commands.append("no monitor-link group")
        return commands

    if not config:
        return commands

    # Flex-Link configuration
    flex_links = config.get("flex_links", [])
    for fl in flex_links:
        group_id = fl["group_id"]
        commands.append("flex-link group {0}".format(group_id))

        master_port = fl.get("master_port")
        if master_port:
            commands.append("master-port {0}".format(_format_port(master_port)))

        slave_port = fl.get("slave_port")
        if slave_port:
            commands.append("slave-port {0}".format(_format_port(slave_port)))

        preemption_mode = fl.get("preemption_mode")
        if preemption_mode:
            commands.append("preemption mode {0}".format(preemption_mode))

        commands.append("exit")

    # Monitor-Link configuration
    monitor_links = config.get("monitor_links", [])
    for ml in monitor_links:
        group_id = ml["group_id"]
        commands.append("monitor-link group {0}".format(group_id))

        uplink_port = ml.get("uplink_port")
        if uplink_port:
            commands.append("uplink-port {0}".format(_format_port(uplink_port)))

        downlink_ports = ml.get("downlink_ports", [])
        for dl_port in downlink_ports:
            commands.append("downlink-port {0}".format(_format_port(dl_port)))

        commands.append("exit")

    return commands


def main() -> None:
    """Run the Flex-Link and Monitor-Link module entry point."""
    port_spec_args = dict(
        type=dict(type="str", choices=["eth", "eth-trunk"], required=True),
        id=dict(type="str", required=True),
    )

    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                flex_links=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        group_id=dict(type="int", required=True),
                        master_port=dict(type="dict", options=port_spec_args),
                        slave_port=dict(type="dict", options=port_spec_args),
                        preemption_mode=dict(
                            type="str",
                            choices=["role", "bandwidth"],
                        ),
                    ),
                ),
                monitor_links=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        group_id=dict(type="int", required=True),
                        uplink_port=dict(type="dict", options=port_spec_args),
                        downlink_ports=dict(
                            type="list",
                            elements="dict",
                            options=port_spec_args,
                        ),
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

    exit_rendered_or_fail(module, "xikeos_flex_monitor_link", config, state, get_commands, "merged")


if __name__ == "__main__":
    main()
