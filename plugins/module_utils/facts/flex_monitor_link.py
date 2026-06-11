"""Flex-Link and Monitor-Link facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

import re

from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


def _parse_port_spec(text: str | None) -> dict[str, str] | None:
    """Parse a port spec string like 'eth 0/0/1' or 'eth-trunk 1' into a dict."""
    if not text:
        return None
    text = text.strip()
    match = re.match(r"^(eth-trunk|eth)\s+(\S+)$", text, re.IGNORECASE)
    if match:
        return {"type": match.group(1).lower(), "id": match.group(2)}
    return None


def parse_flex_link_output(output: str | None) -> list[dict[str, Any]]:
    """
    Parse 'show flex-link group' output and return Flex-Link facts.

    Returns a list of Flex-Link group dicts.
    """
    groups: list[dict[str, Any]] = []
    current_group: dict[str, Any] | None = None

    if output is None or output == "":
        return groups

    lines = output.strip().split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Group header: "Flex-Link Group 1"
        match = re.match(r"Flex-Link\s+Group\s+(\d+)", stripped, re.IGNORECASE)
        if match:
            if current_group:
                groups.append(current_group)
            current_group = {"group_id": int(match.group(1))}
            continue

        if not current_group:
            continue

        # Master port
        match = re.match(r"Master[- ]Port\s*:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            current_group["master_port"] = _parse_port_spec(match.group(1))
            continue

        # Slave port
        match = re.match(r"Slave[- ]Port\s*:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            current_group["slave_port"] = _parse_port_spec(match.group(1))
            continue

        # Preemption mode
        match = re.match(r"Preemption\s+Mode\s*:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            current_group["preemption_mode"] = match.group(1).lower()
            continue

    if current_group:
        groups.append(current_group)

    return groups


def parse_monitor_link_output(output: str | None) -> list[dict[str, Any]]:
    """
    Parse 'show monitor-link group' output and return Monitor-Link facts.

    Returns a list of Monitor-Link group dicts.
    """
    groups: list[dict[str, Any]] = []
    current_group: dict[str, Any] | None = None

    if output is None or output == "":
        return groups

    lines = output.strip().split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Group header: "Monitor-Link Group 1"
        match = re.match(r"Monitor-Link\s+Group\s+(\d+)", stripped, re.IGNORECASE)
        if match:
            if current_group:
                groups.append(current_group)
            current_group = {
                "group_id": int(match.group(1)),
                "downlink_ports": [],
            }
            continue

        if not current_group:
            continue

        # Uplink port
        match = re.match(r"Uplink[- ]Port\s*:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            current_group["uplink_port"] = _parse_port_spec(match.group(1))
            continue

        # Downlink port(s)
        match = re.match(r"Downlink[- ]Port(?:s)?\s*:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            # Could be comma-separated list
            ports_str = match.group(1).strip()
            for port_text in ports_str.split(","):
                port_spec = _parse_port_spec(port_text.strip())
                if port_spec:
                    current_group["downlink_ports"].append(port_spec)
            continue

    if current_group:
        groups.append(current_group)

    return groups


def get_facts(connection: Any) -> dict[str, list[dict[str, Any]]]:
    """
    Get Flex-Link and Monitor-Link facts from the device.

    Args:
        connection: The connection object to run commands

    Returns:
        dict: Flex-Link and Monitor-Link facts
    """
    facts: dict[str, Any] = {
        "flex_links": [],
        "monitor_links": [],
    }

    # Get Flex-Link facts
    try:
        stdout = connection.get(command="show flex-link group")
        facts["flex_links"] = parse_flex_link_output(stdout)
    except Exception:
        pass

    # Get Monitor-Link facts
    try:
        stdout = connection.get(command="show monitor-link group")
        facts["monitor_links"] = parse_monitor_link_output(stdout)
    except Exception:
        pass

    return facts
