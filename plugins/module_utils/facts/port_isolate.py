"""Facts parser for Xike OS 'show port-isolate group' output."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type
# pylint: disable=unsupported-binary-operation

from typing import Any

import re


def parse_port_isolate_group(output: str | None) -> list[dict[str, Any]]:
    """
    Parse 'show port-isolate group' output and return port isolation facts.

    Expected output format:
        Port-isolate Group: 1
          Members:
            ethernet 0/0/1
            ethernet 0/0/2
            ethernet 0/0/3

        Port-isolate Group: 2
          Members:
            all

    Returns:
        list of dict, each with keys: group_id, members
    """
    groups = []

    if not output:
        return groups

    lines = output.strip().splitlines()

    current_group = None
    in_members = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and separator lines
        if not stripped or re.match(r'^[-=]+$', stripped):
            # Empty line between groups
            if current_group is not None and in_members:
                in_members = False
            continue

        # Match group header: "Port-isolate Group: <id>"
        group_match = re.match(
            r'^Port[-\s]?isolate\s+Group\s*:?\s*(\d+)',
            stripped,
            re.IGNORECASE,
        )
        if group_match:
            # Save previous group
            if current_group is not None:
                groups.append(current_group)
            current_group = {
                "group_id": int(group_match.group(1)),
                "members": [],
            }
            in_members = False
            continue

        if current_group is None:
            continue

        # Match "Members:" header
        if re.match(r'^Members\s*:?\s*$', stripped, re.IGNORECASE):
            in_members = True
            continue

        # Parse member lines (indented under Members:)
        if in_members:
            # Skip dashes
            if re.match(r'^[-]+$', stripped):
                continue
            # Member can be "all" or "ethernet 0/0/1"
            member_match = re.match(r'^(\S+(?:\s+\S+)?)\s*$', stripped)
            if member_match:
                member = member_match.group(1).strip()
                current_group["members"].append(member)

    # Save the last group
    if current_group is not None:
        groups.append(current_group)

    return groups


def get_facts(
    facts_module: Any,
    connection: Any,
    command: str = "show port-isolate group",
) -> dict[str, list[dict[str, Any]]]:
    """
    Get port isolation group facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands
        command: The command to run (default: show port-isolate group)

    Returns:
        dict: Port isolation group facts
    """
    cmd = command

    try:
        stdout = connection.get(command=cmd)
    except Exception:
        return {"port_isolate_groups": []}

    groups = parse_port_isolate_group(stdout)

    return {
        "port_isolate_groups": groups,
    }
