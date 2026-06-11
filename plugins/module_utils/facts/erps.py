#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ERPS facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

import re

from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


def parse_erps_brief(output: str | None) -> dict[str, list[dict[str, Any]]]:
    """
    Parse 'show erps' output and return ERPS facts.

    Expected output format:
    ERPS Status: Enabled
    Instance  Control-VLAN  Port0         Port1         Work-Mode     Status
    --------  ------------  ------------  ------------  ------------  ------
    1         100           Eth1/0/1      Eth1/0/2      Revertive     Active
    2         200           Eth-Trunk1    Eth-Trunk2    Non-revertive Active
    """
    facts: dict[str, list[dict[str, Any]]] = {"instances": []}

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header and separator lines
        if stripped.upper().startswith("ERPS STATUS"):
            continue
        if stripped.upper().startswith("INSTANCE"):
            continue
        if stripped.startswith("---") or stripped.startswith("--------"):
            continue

        # Parse instance data lines
        # Format: instance_id  control_vlan  port0  port1  work_mode  status
        match = re.match(
            r"^(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)",
            stripped,
        )
        if match:
            instance_id = int(match.group(1))
            control_vlan = int(match.group(2))
            port0 = match.group(3)
            port1 = match.group(4)
            work_mode = match.group(5).lower().replace("-", "-")

            facts["instances"].append({
                "instance_id": instance_id,
                "control_vlan": control_vlan,
                "port0": port0,
                "port1": port1,
                "work_mode": work_mode,
            })

    return facts


def parse_erps_instance(output: str | None, instance_id: int) -> dict[str, Any]:
    """
    Parse 'show erps instance <id>' output and return detailed ERPS instance facts.

    Expected output format:
    ERPS Instance: 1
    Control-VLAN: 100
    Port0: Ethernet1/0/1 (Owner)
    Port1: Ethernet1/0/2 (Neighbour)
    Work Mode: Revertive
    Ring Status: Enabled
    Protected Instance: 1,2,3
    Guard Timer: 500 cs
    WTR Timer: 5 min
    MEL: 5
    """
    facts: dict[str, Any] = {"instance_id": instance_id}

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Control VLAN
        match = re.match(r"^Control-VLAN:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["control_vlan"] = int(match.group(1))
            continue

        # Port0
        match = re.match(r"^Port0:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            facts["port0"] = match.group(1).strip()
            continue

        # Port1
        match = re.match(r"^Port1:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            facts["port1"] = match.group(1).strip()
            continue

        # Work Mode
        match = re.match(r"^Work Mode:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["work_mode"] = match.group(1).lower().replace(" ", "-")
            continue

        # Ring Status
        match = re.match(r"^Ring Status:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["ring_enable"] = match.group(1).lower() == "enabled"
            continue

        # Protected Instance
        match = re.match(r"^Protected Instance:\s*(.+)", stripped, re.IGNORECASE)
        if match:
            facts["protected_instances"] = match.group(1).strip()
            continue

        # Guard Timer
        match = re.match(r"^Guard Timer:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["guard_timer"] = int(match.group(1))
            continue

        # WTR Timer
        match = re.match(r"^WTR Timer:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["wtr_timer"] = int(match.group(1))
            continue

        # MEL
        match = re.match(r"^MEL:\s*(\d+)", stripped, re.IGNORECASE)
        if match:
            facts["mel"] = int(match.group(1))
            continue

    return facts


def parse_erps_statistics(output: str | None) -> dict[str, list[dict[str, Any]]]:
    """
    Parse 'show erps statistics' output and return ERPS statistics facts.

    Expected output format:
    Instance  Rx-Config  Tx-Config  Rx-Flush  Tx-Flush  Events
    --------  ---------  ---------  --------  --------  ------
    1         1234       5678       90        12        5
    2         100        200        10        3         1
    """
    facts: dict[str, list[dict[str, Any]]] = {"instances": []}

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header and separator lines
        if stripped.upper().startswith("INSTANCE"):
            continue
        if stripped.startswith("---") or stripped.startswith("--------"):
            continue

        # Parse statistics lines
        match = re.match(
            r"^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
            stripped,
        )
        if match:
            facts["instances"].append({
                "instance_id": int(match.group(1)),
                "rx_config": int(match.group(2)),
                "tx_config": int(match.group(3)),
                "rx_flush": int(match.group(4)),
                "tx_flush": int(match.group(5)),
                "events": int(match.group(6)),
            })

    return facts


def get_facts(facts_module: Any, connection: Any) -> dict[str, dict[str, Any]]:
    """
    Get ERPS facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands

    Returns:
        dict: ERPS facts
    """
    erps_facts: dict[str, Any] = {}

    # Get ERPS brief info
    try:
        stdout = connection.get(command="show erps")
        erps_facts = parse_erps_brief(stdout)
    except Exception:
        pass

    # Get detailed info for each instance
    instances = erps_facts.get("instances", [])
    detailed_instances: list[dict[str, Any]] = []
    for inst in instances:
        instance_id = inst.get("instance_id")
        if instance_id is not None:
            try:
                stdout = connection.get(
                    command=f"show erps instance {instance_id}"
                )
                detailed = parse_erps_instance(stdout, instance_id)
                detailed_instances.append(detailed)
            except Exception:
                detailed_instances.append(inst)

    if detailed_instances:
        erps_facts["instances"] = detailed_instances

    # Get ERPS statistics
    try:
        stdout = connection.get(command="show erps statistics")
        erps_facts["statistics"] = parse_erps_statistics(stdout)
    except Exception:
        pass

    return {
        "erps": erps_facts,
    }
