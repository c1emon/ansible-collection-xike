# -*- coding: utf-8 -*-

"""OSPFv2 facts module for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
from typing import Any, TYPE_CHECKING

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule

OSPFProcess = dict[str, Any]
OSPFNeighbor = dict[str, Any]


class Ospfv2Facts(object):
    """Gather OSPFv2 facts from Xike switches.

    Executes 'show ip ospf' and 'show ip ospf neighbor' through the
    network operational command path to parse OSPF state.
    """

    def __init__(self, module: "AnsibleModule") -> None:
        self.module = module
        self.facts: dict[str, Any] = {}
        self._get_facts()

    def _get_facts(self) -> None:
        """Parse OSPFv2 information from the device."""
        self.facts = {
            'processes': {},
        }
        stdout = run_commands(self.module, ['show ip ospf', 'show ip ospf neighbor'], check_rc=True) or []
        summary_output = to_text(stdout[0] if len(stdout) > 0 else '', errors='surrogate_or_strict')
        neighbor_output = to_text(stdout[1] if len(stdout) > 1 else '', errors='surrogate_or_strict')

        self.facts['processes'] = parse_ospf_summary(summary_output)
        self.facts['neighbors'] = parse_ospf_neighbors(neighbor_output)


def parse_ospf_summary(output: str) -> dict[int, OSPFProcess]:
    """Parse 'show ip ospf' output to extract OSPF process info.

    Expected output format (similar to Cisco IOS):

    Routing Process "ospf 1" with ID 1.1.1.1
     Supports only single TOS(TOS0) routes
     It is an area border router
     Start time: 00:00:05.123, Time elapsed: 02:30:15.456
     Router ID advertisement source: Loopback0
     Number of areas in this router is 3. 2 normal 0 stub 0 nssa
     Reference bandwidth unit is 100 mbps
         Area BACKBONE(0)
             Number of interfaces in this area is 2
             Area has no authentication
             SPF algorithm executed 5 times
         Area 1
             Number of interfaces in this area is 1

    Args:
        output: Output from 'show ip ospf'

    Returns:
        dict: Parsed OSPF process info keyed by process ID
    """
    processes: dict[int, OSPFProcess] = {}
    current_process_id = None

    for line in output.splitlines():
        line = line.strip()

        # Match "Routing Process 'ospf <id>' with ID <router-id>"
        m = re.match(
            r'Routing\s+Process\s+["\']?ospf\s+(\d+)["\']?\s+with\s+ID\s+([\d.]+)',
            line, re.IGNORECASE,
        )
        if m:
            pid = int(m.group(1))
            router_id = m.group(2)
            current_process_id = pid
            processes[pid] = {
                'process_id': pid,
                'router_id': router_id,
                'areas': [],
                'networks': [],
                'passive_interfaces': [],
            }
            continue

        # Parse area info: "Area BACKBONE(0)" or "Area 1"
        if current_process_id is not None:
            area_match = re.match(r'Area\s+(?:BACKBONE\()?(\d+)', line, re.IGNORECASE)
            if area_match:
                processes[current_process_id]['areas'].append(
                    {'area_id': area_match.group(1)}
                )

    return processes


def parse_ospf_neighbors(output: str) -> list[OSPFNeighbor]:
    """Parse 'show ip ospf neighbor' output.

    Expected output format:

    Neighbor ID     Pri  State           Dead Time   Address         Interface
    2.2.2.2           1  FULL/BDR        00:00:35    10.0.0.2        vlan-interface 10
    3.3.3.3           1  FULL/DR         00:00:30    10.0.1.2        vlan-interface 20

    Args:
        output: Output from 'show ip ospf neighbor'

    Returns:
        list: List of neighbor dicts
    """
    neighbors: list[OSPFNeighbor] = []
    header_passed = False

    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        # Skip header line
        if 'Neighbor ID' in stripped and 'Interface' in stripped:
            header_passed = True
            continue

        # Skip separator
        if stripped.startswith('---'):
            continue

        if not header_passed:
            continue

        # Parse data line
        # Format: Neighbor_ID Pri State DeadTime Address Interface
        parts = re.split(r'\s{2,}', stripped)
        if len(parts) >= 6:
            neighbor = {
                'neighbor_id': parts[0].strip(),
                'priority': int(parts[1].strip()) if parts[1].strip().isdigit() else 0,
                'state': parts[2].strip(),
                'dead_time': parts[3].strip(),
                'address': parts[4].strip(),
                'interface': parts[5].strip(),
            }
            neighbors.append(neighbor)

    return neighbors


def parse_running_config(config_text: str) -> dict[int, OSPFProcess]:
    """Parse OSPF configuration from running-config output.

    Args:
        config_text: Output from 'show running-config'

    Returns:
        dict: Parsed OSPF configuration keyed by process ID
    """
    processes: dict[int, OSPFProcess] = {}
    current_pid = None
    in_router_ospf = False

    for line in config_text.splitlines():
        line = line.strip()

        # Match "router ospf <process_id>"
        m = re.match(r'^router\s+ospf\s+(\d+)', line, re.IGNORECASE)
        if m:
            current_pid = int(m.group(1))
            in_router_ospf = True
            processes[current_pid] = {
                'process_id': current_pid,
                'router_id': None,
                'networks': [],
                'redistribute': [],
                'default_info_originate': False,
                'default_info_originate_always': False,
                'default_info_originate_metric': None,
                'default_info_originate_metric_type': None,
                'passive_interfaces': [],
            }
            continue

        # Exit router ospf mode on non-indented commands
        if in_router_ospf and line and not line.startswith(' ') and not line.startswith('\t'):
            if not line.startswith('network') and not line.startswith('ospf') and \
               not line.startswith('redistribute') and not line.startswith('default') and \
               not line.startswith('passive'):
                in_router_ospf = False
                current_pid = None
                continue

        if in_router_ospf and current_pid is not None:
            # Parse "ospf router-id <id>"
            rid_match = re.match(r'ospf\s+router-id\s+([\d.]+)', line, re.IGNORECASE)
            if rid_match:
                processes[current_pid]['router_id'] = rid_match.group(1)
                continue

            # Parse "network <ip> <wildcard> area <area_id>"
            net_match = re.match(
                r'network\s+([\d.]+)\s+([\d.]+)\s+area\s+([\d]+)',
                line, re.IGNORECASE,
            )
            if net_match:
                processes[current_pid]['networks'].append({
                    'network': net_match.group(1),
                    'wildcard': net_match.group(2),
                    'area': net_match.group(3),
                })
                continue

            # Parse "redistribute <protocol> [metric <val>] [route-map <name>]"
            redist_match = re.match(
                r'redistribute\s+(static|connected|bgp)'
                r'(?:\s+metric\s+(\d+))?'
                r'(?:\s+route-map\s+(\S+))?',
                line, re.IGNORECASE,
            )
            if redist_match:
                entry = {
                    'protocol': redist_match.group(1).lower(),
                }
                if redist_match.group(2):
                    entry['metric'] = int(redist_match.group(2))
                if redist_match.group(3):
                    entry['route_map'] = redist_match.group(3)
                processes[current_pid]['redistribute'].append(entry)
                continue

            # Parse "default-information originate [always] [metric <val>] [metric-type <val>]"
            default_match = re.match(r'default-information\s+originate', line, re.IGNORECASE)
            if default_match:
                processes[current_pid]['default_info_originate'] = True
                if re.search(r'\balways\b', line, re.IGNORECASE):
                    processes[current_pid]['default_info_originate_always'] = True
                metric_m = re.search(r'metric\s+(\d+)', line, re.IGNORECASE)
                if metric_m:
                    processes[current_pid]['default_info_originate_metric'] = int(metric_m.group(1))
                mtype_m = re.search(r'metric-type\s+(\d+)', line, re.IGNORECASE)
                if mtype_m:
                    processes[current_pid]['default_info_originate_metric_type'] = int(mtype_m.group(1))
                continue

            # Parse "passive-interface [default | vlan-interface <id>]"
            passive_match = re.match(
                r'passive-interface\s+(default|vlan-interface\s+\d+)',
                line, re.IGNORECASE,
            )
            if passive_match:
                processes[current_pid]['passive_interfaces'].append(
                    passive_match.group(1).strip().lower()
                )
                continue

    return processes


def parse_ospf_database(output: str) -> dict[str, int]:
    """Parse 'show ip ospf database' output.

    Args:
        output: Output from 'show ip ospf database'

    Returns:
        dict: OSPF LSDB summary
    """
    result: dict[str, int] = {
        'router_lsa_count': 0,
        'network_lsa_count': 0,
        'summary_lsa_count': 0,
        'asbr_summary_lsa_count': 0,
        'external_lsa_count': 0,
    }

    for line in output.splitlines():
        line = line.strip().lower()
        if 'router link states' in line:
            count_m = re.search(r'Link States\s*\((\d+)\)', line, re.IGNORECASE)
            if count_m:
                result['router_lsa_count'] = int(count_m.group(1))
        elif 'net link states' in line:
            count_m = re.search(r'Link States\s*\((\d+)\)', line, re.IGNORECASE)
            if count_m:
                result['network_lsa_count'] = int(count_m.group(1))
        elif 'summary net link states' in line:
            count_m = re.search(r'States\s*\((\d+)\)', line, re.IGNORECASE)
            if count_m:
                result['summary_lsa_count'] = int(count_m.group(1))
        elif 'summary asb link states' in line:
            count_m = re.search(r'States\s*\((\d+)\)', line, re.IGNORECASE)
            if count_m:
                result['asbr_summary_lsa_count'] = int(count_m.group(1))
        elif 'type-5 external link states' in line:
            count_m = re.search(r'States\s*\((\d+)\)', line, re.IGNORECASE)
            if count_m:
                result['external_lsa_count'] = int(count_m.group(1))

    return result
