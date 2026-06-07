#!/usr/bin/python
# -*- coding: utf-8 -*-

"""VLAN facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.xike.xikeos.plugins.module_utils.facts.ttp_parser import (
    parse_ttp_template,
)
from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


VLAN_BRIEF_TEMPLATE = "show_vlan_brief.ttp"


def parse_vlan_brief(output):
    """
    Parse 'show vlan brief' output and return VLAN facts.

    Expected output format:
    VLAN Name                             Status    Ports
    ---- -------------------------------- --------- -------------------------------
    1    default                          active    e0/0/1, e0/0/2
    100  DATA                             active
    """
    if not output:
        return []

    vlans = []
    rows = parse_ttp_template(output, VLAN_BRIEF_TEMPLATE, result_key="vlans")

    for row in rows:
        line = row.get("row") if isinstance(row, dict) else row
        if not line:
            continue
        vlan = parse_vlan_line(line.strip())
        if vlan:
            vlans.append(vlan)

    return vlans


def parse_vlan_line(line):
    """
    Parse a single VLAN line from 'show vlan brief' output.

    Example line:
    1    default                          active    e0/0/1, e0/0/2
    """
    # Match VLAN ID (digits at start)
    match = re.match(r"^(\d+)\s+(.+)$", line)
    if not match:
        return None

    vlan_id = int(match.group(1))
    rest = match.group(2)

    # Try to split by multiple spaces to get name, status, and ports
    # The format is typically: VLAN_NAME  STATUS  PORTS
    # But name can have spaces in some implementations

    # Split by double or more spaces
    parts = re.split(r"\s{2,}", rest.strip())

    if len(parts) >= 1:
        name = parts[0].strip()
    else:
        name = ""

    if len(parts) >= 2:
        status = parts[1].strip()
    else:
        status = "active"

    if len(parts) >= 3:
        ports_str = parts[2].strip()
        # Clean up trailing commas
        ports_str = ports_str.rstrip(",").strip()
        ports = [p.strip() for p in ports_str.split(",") if p.strip()]
    else:
        ports = []

    return {
        "vlan_id": vlan_id,
        "name": name,
        "state": status,
        "status": status,
        "ports": ports,
    }


def get_facts(facts_module, connection, command="show vlan brief"):
    """
    Get VLAN facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands
        command: The command to run (default: show vlan brief)

    Returns:
        dict: VLAN facts
    """
    # Build the command using command map if available
    cmd = command

    # Run the command
    try:
        stdout = connection.get(command=cmd)
    except Exception:
        # If command fails, return empty facts
        return {"vlans": []}

    # Parse the output
    vlans = parse_vlan_brief(stdout)

    return {
        "vlans": vlans,
    }
