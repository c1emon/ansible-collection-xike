"""QinQ facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

import re

from ansible_collections.xike.xikeos.plugins.module_utils.xikeos import (
    COMMAND_MAP,
)


def parse_qinq_output(output: str | None) -> dict[str, Any]:
    """
    Parse 'show qinq' output and return QinQ facts.

    Returns a dict with mode, inner_tpid, outer_tpid, and VLAN rules.
    """
    facts: dict[str, Any] = {
        "mode": None,
        "inner_tpid": None,
        "outer_tpid": None,
        "vlan_inserts": [],
        "vlan_pass_throughs": [],
        "vlan_swaps": [],
    }

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # QinQ mode
        match = re.match(r"qinq\s+mode\s+(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["mode"] = match.group(1)
            continue

        # Inner TPID
        match = re.match(r"qinq\s+inner-tpid\s+(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["inner_tpid"] = match.group(1)
            continue

        # Outer TPID
        match = re.match(r"qinq\s+outer-tpid\s+(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["outer_tpid"] = match.group(1)
            continue

        # VLAN insert: vlan insert <start> <end> <service> [priority]
        match = re.match(
            r"vlan\s+insert\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+(\d+))?",
            stripped,
            re.IGNORECASE,
        )
        if match:
            rule = {
                "start_vlan": int(match.group(1)),
                "end_vlan": int(match.group(2)),
                "service_vlan": int(match.group(3)),
            }
            if match.group(4):
                rule["priority"] = int(match.group(4))
            facts["vlan_inserts"].append(rule)
            continue

        # VLAN pass-through: vlan pass-through <start> <end>
        match = re.match(
            r"vlan\s+pass-through\s+(\d+)\s+(\d+)",
            stripped,
            re.IGNORECASE,
        )
        if match:
            facts["vlan_pass_throughs"].append({
                "start_vlan": int(match.group(1)),
                "end_vlan": int(match.group(2)),
            })
            continue

        # VLAN swap: vlan swap <start> <end> <swap> [priority <value>]
        match = re.match(
            r"vlan\s+swap\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+priority\s+(\d+))?",
            stripped,
            re.IGNORECASE,
        )
        if match:
            rule = {
                "start_vlan": int(match.group(1)),
                "end_vlan": int(match.group(2)),
                "swap_vlan": int(match.group(3)),
            }
            if match.group(4):
                rule["priority"] = int(match.group(4))
            facts["vlan_swaps"].append(rule)
            continue

    return facts


def get_facts(connection: Any) -> dict[str, dict[str, Any]]:
    """
    Get QinQ facts from the device.

    Args:
        connection: The connection object to run commands

    Returns:
        dict: QinQ facts
    """
    try:
        stdout = connection.get(command="show qinq")
    except Exception:
        return {"qinq": {}}

    facts = parse_qinq_output(stdout)
    return {"qinq": facts}
