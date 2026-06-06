#!/usr/bin/python
# -*- coding: utf-8 -*-

"""VLAN facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


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

    # Split output into lines
    lines = output.strip().split("\n")

    # Find the data rows (skip header lines)
    # Header: VLAN Name ... Status ... Ports
    # Separator: ---- ...
    # Data: 1    default  active  e0/0/1, e0/0/2

    data_started = False
    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip header line (contains "VLAN" and "Name")
        if stripped.upper().startswith("VLAN") and "NAME" in stripped.upper():
            continue

        # Skip separator line (starts with ----)
        if stripped.startswith("---"):
            data_started = True
            continue

        # Parse data line if we've passed the header
        if data_started or re.match(r"^\d+\s", stripped):
            vlan = parse_vlan_line(stripped)
            if vlan:
                vlans.append(vlan)

    return vlans


def parse_vlan(output):
    """
    Parse 'show vlan' output and return VLAN facts.

    Expected output format:
    VLAN Name         Type       Media     Ports
    ---- ------------ ---------- --------- ----------------------------------------
    1    default      Static     ENET      Ethernet1/0/1       Ethernet1/0/2(T)
                                       Ethernet1/0/3(T)    Ethernet1/0/4(T)
    10   dev          Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
    """
    if not output:
        return []

    vlans = []
    current_vlan = None
    data_started = False

    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.upper().startswith("VLAN") and "NAME" in stripped.upper():
            continue
        if stripped.startswith("---"):
            data_started = True
            continue
        if not data_started:
            continue

        vlan_match = re.match(r"^(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s*(.*)$", stripped)
        if vlan_match:
            if current_vlan:
                vlans.append(current_vlan)
            current_vlan = {
                "vlan_id": int(vlan_match.group(1)),
                "name": vlan_match.group(2),
                "type": vlan_match.group(3),
                "media": vlan_match.group(4),
                "state": "active",
                "status": "active",
                "ports": _parse_show_vlan_ports(vlan_match.group(5)),
            }
            continue

        if current_vlan:
            current_vlan["ports"].extend(_parse_show_vlan_ports(stripped))

    if current_vlan:
        vlans.append(current_vlan)

    return vlans


def _parse_show_vlan_ports(text):
    ports = []
    for port in re.findall(r"\S+", text or ""):
        tagged = port.endswith("(T)")
        name = port[:-3] if tagged else port
        ports.append({"name": name, "tagged": tagged})
    return ports


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
