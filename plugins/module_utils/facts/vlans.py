#!/usr/bin/python
# -*- coding: utf-8 -*-

"""VLAN facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.xike.xikeos.plugins.module_utils.facts.textfsm_parser import (
    parse_textfsm_template,
)
from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


SHOW_VLAN_TEMPLATE = "show_vlan.textfsm"


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
    rows = parse_textfsm_template(output, SHOW_VLAN_TEMPLATE)

    for row in rows:
        vlans.append(
            {
                "vlan_id": int(row["vlan_id"]),
                "name": row.get("name") or "",
                "type": row.get("type") or "",
                "media": row.get("media") or "",
                "state": "active",
                "status": "active",
                "ports": _normalize_show_vlan_ports(row.get("ports") or []),
            }
        )

    return vlans


def _normalize_show_vlan_ports(raw_ports):
    ports = []
    for port in raw_ports:
        tagged = port.endswith("(T)")
        name = port[:-3] if tagged else port
        ports.append({"name": name, "tagged": tagged})
    return ports


def get_facts(facts_module, connection, command="show vlan"):
    """
    Get VLAN facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands
        command: The command to run (default: show vlan)

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
    vlans = parse_vlan(stdout)

    return {
        "vlans": vlans,
    }
