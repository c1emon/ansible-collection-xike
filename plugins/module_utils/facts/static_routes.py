# -*- coding: utf-8 -*-

"""Static routes facts for Xike OS."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from typing import Any, Optional, TYPE_CHECKING

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.errors import (
    XikeOSFactsError,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    run_commands,
)

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule

RouteRecord = dict[str, Any]


class StaticRoutesFacts(object):
    """Gather static route facts from Xike OS devices."""

    def __init__(self, module: "AnsibleModule") -> None:
        self.module = module
        self.facts: dict[str, list[RouteRecord]] = {"static_routes": []}
        self._get_facts()

    def _get_facts(self) -> None:
        """Parse static route information.

        Executes 'show ip route' on the device and parses static routes.
        Also executes 'show ipv6 route' if IPv6 is supported.
        """
        commands = ["show ip route", "show ipv6 route"]
        try:
            stdout = run_commands(self.module, commands, check_rc=True) or []
            ipv4_output = to_text(
                stdout[0] if len(stdout) > 0 else "", errors="surrogate_or_strict"
            )
            ipv6_output = to_text(
                stdout[1] if len(stdout) > 1 else "", errors="surrogate_or_strict"
            )
            self.facts["static_routes"].extend(
                parse_show_ip_route(ipv4_output, route_type="ipv4")
            )
            self.facts["static_routes"].extend(
                parse_show_ip_route(ipv6_output, route_type="ipv6")
            )
        except Exception as exc:
            raise XikeOSFactsError(
                "failed to gather static route facts",
                detail=to_text(exc),
                context="static_routes",
            ) from exc


def parse_show_ip_route(output: str, route_type: str = "ipv4") -> list[RouteRecord]:
    """
    Parse 'show ip route' or 'show ipv6 route' output.

    Expected output formats:

    IPv4 (show ip route):
    Codes: C - connected, S - static, R - RIP, O - OSPF ...

    Destination/Mask    Proto  Pre  Cost  NextHop         Interface
    ---------------------------------------------------------------
    0.0.0.0/0           Static 60   0     10.0.0.1        Vlan10
    192.168.100.0/24    Static 60   0     10.0.0.2        Vlan20
    10.10.0.0/16        Static 1    0     10.0.0.3

    Or alternate format:
    S    0.0.0.0/0 [1/0] via 10.0.0.1
    S    192.168.100.0/24 [60/0] via 10.0.0.2

    IPv6 (show ipv6 route):
    S    ::/0 [1/0] via fe80::1, Vlan10
    S    2001:db8::/32 [1/0] via 2001:db8::1
    """
    routes: list[RouteRecord] = []
    if not output:
        return routes

    lines = output.strip().split("\n")

    # Try format 1: table format (Destination/Mask ... NextHop ...)
    # Try format 2: Cisco-style "S ... via ..." format

    # First, check for table format
    table_routes = _parse_table_format(lines, route_type)
    if table_routes:
        return table_routes

    # Try Cisco-style format
    cisco_routes = _parse_cisco_style(lines, route_type)
    if cisco_routes:
        return cisco_routes

    # Try simple "Static" keyword format
    simple_routes = _parse_simple_format(lines, route_type)
    return simple_routes


def _parse_table_format(lines: list[str], route_type: str) -> list[RouteRecord]:
    """Parse table-style 'show ip route' output."""
    routes: list[RouteRecord] = []
    header_found = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header lines
        if "Destination" in stripped or "Proto" in stripped:
            header_found = True
            continue
        if stripped.startswith("---") or stripped.startswith("==="):
            continue
        if stripped.lower().startswith("codes") or stripped.lower().startswith("route"):
            continue

        if not header_found:
            # Also try matching data lines without header
            route = _parse_route_line(stripped, route_type)
            if route:
                routes.append(route)
        else:
            route = _parse_route_line(stripped, route_type)
            if route:
                routes.append(route)

    return routes


def _parse_cisco_style(lines: list[str], route_type: str) -> list[RouteRecord]:
    """Parse Cisco-style 'S ... via ...' output."""
    routes: list[RouteRecord] = []

    # Pattern: S    192.168.1.0/24 [60/0] via 10.0.0.1
    # Pattern: S    0.0.0.0/0 [1/0] via 10.0.0.1, Vlan10
    pattern = re.compile(
        r"^S\s+"
        r"(\S+)"  # destination/mask
        r"(?:\s+\[(\d+)/(\d+)\])?"  # optional [admin/metric]
        r"\s+via\s+"
        r"(\S+)"  # next_hop (first via)
        r"(?:,\s*(\S+))?"  # optional interface
    )

    for line in lines:
        stripped = line.strip()
        match = pattern.match(stripped)
        if match:
            dest_mask = match.group(1)
            next_hop = match.group(4).rstrip(",")
            distance = int(match.group(2)) if match.group(2) is not None else 1

            destination, mask = _split_dest_mask(dest_mask)

            routes.append(
                {
                    "destination": destination,
                    "mask": mask,
                    "next_hop": next_hop,
                    "distance": distance,
                    "route_type": route_type,
                }
            )

    return routes


def _parse_simple_format(lines: list[str], route_type: str) -> list[RouteRecord]:
    """Parse simple route format with 'Static' keyword."""
    routes: list[RouteRecord] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        route = _parse_route_line(stripped, route_type)
        if route:
            routes.append(route)

    return routes


def _parse_route_line(line: str, route_type: str) -> Optional[RouteRecord]:
    """Parse a single route data line."""
    # Try to match various formats:
    # 1. 0.0.0.0/0 Static 60 0 10.0.0.1 Vlan10
    # 2. 0.0.0.0/0 Static 60 0 10.0.0.1
    # 3. 192.168.1.0 255.255.255.0 Static 60 0 10.0.0.1

    parts = line.split()
    if len(parts) < 3:
        return None

    # Skip non-route lines (headers, codes, etc.)
    skip_keywords = ["codes", "route", "destination", "proto", "---", "===", "total"]
    if any(parts[0].lower().startswith(kw) for kw in skip_keywords):
        return None

    # Determine if it's a route line
    # Check if first part looks like an IP/prefix or has 'Static' keyword
    has_static = "static" in line.lower()

    if not has_static:
        # Check if first part looks like a network
        dest_part = parts[0]
        if not _looks_like_network(dest_part):
            return None

    # Try format: dest/mask [proto] distance cost next_hop [interface]
    # or: dest mask [proto] distance cost next_hop [interface]
    dest_mask = parts[0]
    destination, mask = _split_dest_mask(dest_mask)

    # Look for Static keyword and find next_hop
    next_hop = None
    distance = 1

    for i, part in enumerate(parts):
        if part.lower() == "static":
            # After Static: distance cost next_hop [interface]
            remaining = parts[i + 1 :]
            if len(remaining) >= 3:
                try:
                    distance = int(remaining[0])
                except ValueError:
                    distance = 1
                # next_hop is typically after metric
                next_hop = remaining[2] if len(remaining) > 2 else remaining[-1]
                # Clean interface names from next_hop
                next_hop = next_hop.rstrip(",")
                if _looks_like_ip(next_hop):
                    break
            elif len(remaining) >= 1:
                next_hop = remaining[-1].rstrip(",")
                break

    # If no Static keyword found, try to find next_hop by position
    if next_hop is None and len(parts) >= 2:
        for part in parts[1:]:
            if _looks_like_ip(part):
                next_hop = part.rstrip(",")
                break

    if not next_hop or not _looks_like_ip(next_hop):
        return None

    return {
        "destination": destination,
        "mask": mask,
        "next_hop": next_hop,
        "distance": distance,
        "route_type": route_type,
    }


def _split_dest_mask(dest_mask: str) -> tuple[str, str]:
    """Split destination/mask into separate destination and mask.

    Handles formats:
    - '192.168.1.0/24' -> ('192.168.1.0', '255.255.255.0')
    - '192.168.1.0 255.255.255.0' -> ('192.168.1.0', '255.255.255.0')
    - '0.0.0.0/0' -> ('0.0.0.0', '0.0.0.0')
    - '2001:db8::/32' -> ('2001:db8::', '32')
    """
    if "/" in dest_mask:
        parts = dest_mask.rsplit("/", 1)
        destination = parts[0]
        prefix = parts[1]

        # Convert prefix to mask if it's IPv4
        if _is_ipv4(destination):
            mask = _prefix_to_ipv4_mask(int(prefix))
        else:
            mask = prefix

        return destination, mask

    # Try to split by space (two parts: dest and mask)
    parts = dest_mask.split()
    if len(parts) == 2:
        return parts[0], parts[1]

    # Single part - assume it's the destination, use default mask
    return dest_mask, ""


def _prefix_to_ipv4_mask(prefix_len: int) -> str:
    """Convert CIDR prefix length to dotted-decimal mask."""
    if prefix_len == 0:
        return "0.0.0.0"
    if prefix_len >= 32:
        return "255.255.255.255"

    mask_bits = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return ".".join(str((mask_bits >> (8 * i)) & 0xFF) for i in range(3, -1, -1))


def _is_ipv4(addr: str) -> bool:
    """Check if an address looks like IPv4."""
    parts = addr.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


def _looks_like_ip(addr: str) -> bool:
    """Check if a string looks like an IP address."""
    if ":" in addr:
        # IPv6
        return True
    parts = addr.split(".")
    if len(parts) == 4:
        return all(p.isdigit() for p in parts)
    return False


def _looks_like_network(net: str) -> bool:
    """Check if a string looks like a network destination."""
    if "/" in net:
        parts = net.rsplit("/", 1)
        return _looks_like_ip(parts[0])

    parts = net.split(".")
    if len(parts) == 4:
        return all(p.isdigit() for p in parts)

    return False


def parse_running_config(
    config_text: str, route_type: str = "ipv4"
) -> list[RouteRecord]:
    """Parse static routes from running-config output.

    Looks for lines like:
        ip route 0.0.0.0 0.0.0.0 10.0.0.1
        ip route 192.168.100.0 255.255.255.0 10.0.0.2 10
        ipv6 route 2001:db8::/32 2001:db8::1

    Args:
        config_text: Output from 'show running-config'
        route_type: 'ipv4' or 'ipv6'

    Returns:
        list: Parsed static route entries
    """
    routes: list[RouteRecord] = []

    for line in config_text.splitlines():
        line = line.strip()

        if route_type == "ipv4" and line.startswith("ip route "):
            # Format: ip route <network> <mask> <next_hop> [distance]
            parts = line.split()
            if len(parts) >= 5:
                routes.append(
                    {
                        "destination": parts[2],
                        "mask": parts[3],
                        "next_hop": parts[4],
                        "distance": int(parts[5]) if len(parts) > 5 else 1,
                        "route_type": "ipv4",
                    }
                )
        elif route_type == "ipv6" and line.startswith("ipv6 route "):
            # Format: ipv6 route <network>/<len> <next_hop>
            parts = line.split()
            if len(parts) >= 4:
                dest_prefix = parts[2]
                if "/" in dest_prefix:
                    dest, prefix = dest_prefix.rsplit("/", 1)
                else:
                    dest = dest_prefix
                    prefix = "128"
                routes.append(
                    {
                        "destination": dest,
                        "mask": prefix,
                        "next_hop": parts[3],
                        "distance": 1,
                        "route_type": "ipv6",
                    }
                )

    return routes
