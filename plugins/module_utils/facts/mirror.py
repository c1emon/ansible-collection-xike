"""Facts parser for Xike OS 'show mirror group' output."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re


def parse_mirror_group(output):
    """
    Parse 'show mirror group' output and return mirror group facts.

    Expected output format:
        Mirror Group 1
          Source Interface     Direction
          -------------------- -----------
          ethernet 0/0/1       both
          ethernet 0/0/2       ingress
          cpu                   egress
          Destination Interface: ethernet 0/0/10

    Returns:
        list of dict, each with keys: group_id, source_interfaces, destination_interface
    """
    groups = []

    if not output:
        return groups

    lines = output.strip().splitlines()

    current_group = None
    section = None  # 'source', 'destination', or None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and separator lines
        if not stripped or re.match(r'^[-=]+$', stripped):
            continue

        # Match group header: "Mirror Group <id>" or "Mirror Group: <id>"
        group_match = re.match(r'^Mirror\s+Group\s*:?\s*(\d+)', stripped, re.IGNORECASE)
        if group_match:
            # Save previous group if any
            if current_group is not None:
                groups.append(current_group)
            current_group = {
                "group_id": int(group_match.group(1)),
                "source_interfaces": [],
                "destination_interface": None,
            }
            section = None
            continue

        if current_group is None:
            continue

        # Match section headers
        if re.match(r'^Source\s+Interface', stripped, re.IGNORECASE):
            section = "source"
            continue
        if re.match(r'^Destination\s+Interface', stripped, re.IGNORECASE):
            section = "destination"
            continue

        # Parse source interface lines
        if section == "source":
            # Skip the separator line under the header
            if re.match(r'^[-]+', stripped):
                continue
            # Source line: "ethernet 0/0/1  both" or "cpu  ingress"
            src_match = re.match(
                r'^(\S+(?:\s+\S+)?)\s+(ingress|egress|both)\s*$',
                stripped,
                re.IGNORECASE,
            )
            if src_match:
                current_group["source_interfaces"].append({
                    "name": src_match.group(1).strip(),
                    "direction": src_match.group(2).lower(),
                })

        # Parse destination interface
        if section == "destination":
            # Format: "Destination Interface: ethernet 0/0/10" or just "ethernet 0/0/10"
            dest_match = re.match(
                r'^(?:Destination\s+Interface\s*:?\s*)?(\S+(?:\s+\S+)?)\s*$',
                stripped,
                re.IGNORECASE,
            )
            if dest_match:
                current_group["destination_interface"] = dest_match.group(1).strip()
                section = None

        # Also handle "Destination Interface: ethernet 0/0/10" on a single line
        dest_inline = re.match(
            r'^Destination\s+Interface\s*:?\s*(\S+(?:\s+\S+)?)\s*$',
            stripped,
            re.IGNORECASE,
        )
        if dest_inline:
            current_group["destination_interface"] = dest_inline.group(1).strip()
            section = None

    # Don't forget the last group
    if current_group is not None:
        groups.append(current_group)

    return groups


def get_facts(facts_module, connection, command="show mirror group all"):
    """
    Get mirror group facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands
        command: The command to run (default: show mirror group all)

    Returns:
        dict: Mirror group facts
    """
    cmd = command

    try:
        stdout = connection.get(command=cmd)
    except Exception:
        return {"mirror_groups": []}

    groups = parse_mirror_group(stdout)

    return {
        "mirror_groups": groups,
    }
