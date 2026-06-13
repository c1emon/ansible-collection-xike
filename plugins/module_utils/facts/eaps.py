#!/usr/bin/python
# -*- coding: utf-8 -*-

"""EAPS facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

import re

def parse_eaps_brief(output: str | None) -> dict[str, list[dict[str, Any]]]:
    """
    Parse 'show eaps' output and return EAPS facts.

    Expected output format:
    EAPS Status: Enabled
    Domain  Control-VLAN  Work-Mode   Status
    ------  ------------  ----------  ------
    1       100           Standard    Active
    2       200           RRPP        Active
    """
    facts: dict[str, list[dict[str, Any]]] = {"domains": []}

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header and separator lines
        if stripped.upper().startswith("EAPS STATUS"):
            continue
        if stripped.upper().startswith("DOMAIN"):
            continue
        if stripped.startswith("---") or stripped.startswith("------"):
            continue

        # Parse domain data lines
        # Format: domain_id  control_vlan  work_mode  status
        match = re.match(r"^(\d+)\s+(\d+)\s+(\S+)\s+(\S+)", stripped)
        if match:
            domain_id = int(match.group(1))
            control_vlan = int(match.group(2))
            work_mode = match.group(3).lower().replace(" ", "-")

            facts["domains"].append({
                "domain_id": domain_id,
                "control_vlan": control_vlan,
                "work_mode": work_mode,
            })

    return facts


def parse_eaps_topology(output: str | None) -> dict[str, list[dict[str, Any]]]:
    """
    Parse 'show eaps topology' output and return EAPS topology facts.

    Expected output format:
    Domain  Ring  Role      Port0         Port1         Status    Enabled
    ------  ----  --------  ------------  ------------  --------  -------
    1       1     Master    Eth1/0/1      Eth1/0/2      Active    Yes
    1       2     Transit   Eth1/0/3      Eth1/0/4      Active    Yes
    2       1     Master    Eth-Trunk1    Eth-Trunk2    Active    No
    """
    facts: dict[str, list[dict[str, Any]]] = {"domains": []}

    if output is None or output == "":
        return facts

    lines = output.strip().split("\n")

    # Temporary structure to group rings by domain
    domain_rings: dict[int, list[dict[str, Any]]] = {}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header and separator lines
        if stripped.upper().startswith("DOMAIN"):
            continue
        if stripped.startswith("---") or stripped.startswith("------"):
            continue

        # Parse topology lines
        match = re.match(
            r"^(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)",
            stripped,
        )
        if match:
            domain_id = int(match.group(1))
            ring_id = int(match.group(2))
            role = match.group(3).lower()
            port0 = match.group(4)
            port1 = match.group(5)
            status = match.group(6).lower()
            enabled = match.group(7).lower() == "yes"

            if domain_id not in domain_rings:
                domain_rings[domain_id] = []

            domain_rings[domain_id].append({
                "ring_id": ring_id,
                "role": role,
                "port0": port0,
                "port1": port1,
                "status": status,
                "enabled": enabled,
            })

    for domain_id, rings in sorted(domain_rings.items()):
        facts["domains"].append({
            "domain_id": domain_id,
            "rings": rings,
        })

    return facts


def parse_eaps_domain_detail(output: str | None, domain_id: int) -> dict[str, Any]:
    """
    Parse detailed EAPS domain info.

    Expected output format:
    EAPS Domain: 1
    Control-VLAN: 100
    Work Mode: Standard
    Ring 1: Enabled, Master, Eth1/0/1 -> Eth1/0/2, Active
    Ring 2: Enabled, Transit, Eth1/0/3 -> Eth1/0/4, Active
    """
    facts: dict[str, Any] = {"domain_id": domain_id}

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

        # Work Mode
        match = re.match(r"^Work Mode:\s*(\S+)", stripped, re.IGNORECASE)
        if match:
            facts["work_mode"] = match.group(1).lower().replace(" ", "-")
            continue

        # Ring entries
        match = re.match(
            r"^Ring\s+(\d+):\s+(\S+),\s+(\S+),\s+(\S+)\s*->\s*(\S+),\s*(\S+)",
            stripped,
            re.IGNORECASE,
        )
        if match:
            ring = {
                "ring_id": int(match.group(1)),
                "enabled": match.group(2).lower() == "enabled",
                "role": match.group(3).lower(),
                "port0": match.group(4),
                "port1": match.group(5),
                "status": match.group(6).lower(),
            }

            if "rings" not in facts:
                facts["rings"] = []
            facts["rings"].append(ring)

    return facts


def get_facts(facts_module: Any, connection: Any) -> dict[str, dict[str, Any]]:
    """
    Get EAPS facts from the device.

    Args:
        facts_module: The facts module instance
        connection: The connection object to run commands

    Returns:
        dict: EAPS facts
    """
    eaps_facts: dict[str, Any] = {}

    # Get EAPS brief info
    try:
        stdout = connection.get(command="show eaps")
        eaps_facts = parse_eaps_brief(stdout)
    except Exception:
        pass

    # Get topology info
    try:
        stdout = connection.get(command="show eaps topology")
        topology = parse_eaps_topology(stdout)
        if topology.get("domains"):
            eaps_facts["topology"] = topology
    except Exception:
        pass

    # Get detailed info for each domain
    domains = eaps_facts.get("domains", [])
    detailed_domains: list[dict[str, Any]] = []
    for domain in domains:
        domain_id = domain.get("domain_id")
        if domain_id is not None:
            try:
                stdout = connection.get(
                    command=f"show eaps domain {domain_id}"
                )
                detailed = parse_eaps_domain_detail(stdout, domain_id)
                detailed_domains.append(detailed)
            except Exception:
                detailed_domains.append(domain)

    if detailed_domains:
        eaps_facts["domains"] = detailed_domains

    return {
        "eaps": eaps_facts,
    }
