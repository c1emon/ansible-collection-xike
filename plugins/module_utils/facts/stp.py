#!/usr/bin/python
# -*- coding: utf-8 -*-

"""STP facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


def parse_stp_brief(output):
    """
    Parse 'show stp interface brief' output and return STP facts.

    Expected output format:
    STP status: ENABLED
    STP mode: RSTP
    Bridge ID: 0000.001a.2b3c.4d5e
    Bridge Priority: 32768
    Hello Time: 2 sec
    Forward Delay: 15 sec
    Max Age: 20 sec
    Pathcost Standard: dot1d-1998
    BPDU Guard: Disabled
    BPDU Filter: Disabled
    """
    facts = {}

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # STP mode
        match = re.match(r"^STP mode:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["stp_mode"] = match.group(1).lower()
            continue

        # Bridge priority
        match = re.match(r"^Bridge Priority:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["priority"] = int(match.group(1))
            continue

        # Hello time
        match = re.match(r"^Hello Time:\s*(\d+)\s*sec", stripped, re.IGNORECASE)
        if match:
            facts["hello_time"] = int(match.group(1))
            continue

        # Forward delay
        match = re.match(r"^Forward Delay:\s*(\d+)\s*sec", stripped, re.IGNORECASE)
        if match:
            facts["forward_time"] = int(match.group(1))
            continue

        # Max age
        match = re.match(r"^Max Age:\s*(\d+)\s*sec", stripped, re.IGNORECASE)
        if match:
            facts["max_age"] = int(match.group(1))
            continue

        # Pathcost standard
        match = re.match(r"^Pathcost Standard:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["pathcost_standard"] = match.group(1)
            continue

        # BPDU Guard
        match = re.match(r"^BPDU Guard:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["bpdu_guard"] = match.group(1).lower() == "enabled"
            continue

        # BPDU Filter
        match = re.match(r"^BPDU Filter:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["bpdu_filter"] = match.group(1).lower() == "enabled"
            continue

    return facts


def parse_mstp_brief(output):
    """
    Parse 'show mstp instance brief' output and return MSTP facts.

    Expected output format:
    MST Region Name: MY_REGION
    Revision Level: 1
    Instance  VLANs              Priority
    --------  -----------------  --------
    0         1-100              32768
    1         10,20,30           8192
    2         100,200            16384
    """
    facts = {}
    instances = []

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # MST region name
        match = re.match(r"^MST Region Name:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            facts["region_name"] = match.group(1).strip()
            continue

        # Revision level
        match = re.match(r"^Revision Level:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["revision"] = int(match.group(1))
            continue

        # Skip header lines
        if stripped.upper().startswith("INSTANCE"):
            continue
        if stripped.startswith("---") or stripped.startswith("--------"):
            continue

        # Parse instance data lines
        # Format: instance_id  vlan_range  priority
        match = re.match(r"^(\d+)\s+([\d,\-\s]+)\s+(\d+)", stripped)
        if match:
            instance_id = int(match.group(1))
            vlan_str = match.group(2).strip()
            priority = int(match.group(3))

            # Parse VLAN ranges (e.g., "1-100", "10,20,30", "1-50,100-200")
            vlans = parse_vlan_ranges(vlan_str)

            instances.append({
                "instance_id": instance_id,
                "priority": priority,
                "vlans": vlans,
            })

    if instances:
        facts["instances"] = instances

    return facts


def parse_vlan_ranges(vlan_str):
    """
    Parse VLAN range string into a list of VLAN IDs.

    Supports formats like:
    - "100" -> [100]
    - "1-5" -> [1, 2, 3, 4, 5]
    - "1-3,5,7-9" -> [1, 2, 3, 5, 7, 8, 9]
    """
    vlans = []

    # Split by comma
    parts = vlan_str.split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Check for range (e.g., "1-5")
        range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", part)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            vlans.extend(range(start, end + 1))
        else:
            # Single VLAN
            try:
                vlans.append(int(part))
            except ValueError:
                continue

    return sorted(set(vlans))


def parse_pvst_brief(output):
    """
    Parse 'show pvst instance brief' output and return PVST facts.

    Expected output format:
    Instance  VLAN    Priority
    --------  ------  --------
    10        10      32768
    20        20      32768
    """
    facts = {}
    instances = []

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header lines
        if stripped.upper().startswith("INSTANCE"):
            continue
        if stripped.startswith("---") or stripped.startswith("--------"):
            continue

        # Parse instance data lines
        match = re.match(r"^(\d+)\s+(\d+)\s+(\d+)", stripped)
        if match:
            instance_id = int(match.group(1))
            vlan_id = int(match.group(2))
            priority = int(match.group(3))

            instances.append({
                "instance_id": instance_id,
                "vlan_id": vlan_id,
                "priority": priority,
            })

    if instances:
        facts["instances"] = instances

    return facts


def get_facts(facts_module, connection):
    """
    Get STP facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands

    Returns:
        dict: STP facts
    """
    stp_facts = {}
    mstp_facts = {}
    pvst_facts = {}

    # Get STP basic info
    try:
        stdout = connection.get(command="show stp interface brief")
        stp_facts = parse_stp_brief(stdout)
    except Exception:
        pass

    # Get MSTP instance info
    try:
        stdout = connection.get(command="show mstp instance brief")
        mstp_facts = parse_mstp_brief(stdout)
    except Exception:
        pass

    # Get PVST instance info
    try:
        stdout = connection.get(command="show pvst instance brief")
        pvst_facts = parse_pvst_brief(stdout)
    except Exception:
        pass

    # Merge MSTP into stp_facts
    if mstp_facts:
        stp_facts["mstp"] = mstp_facts

    # Merge PVST into stp_facts
    if pvst_facts:
        stp_facts["pvst"] = pvst_facts

    return {
        "stp": stp_facts,
    }
