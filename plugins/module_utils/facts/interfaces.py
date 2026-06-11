"""Facts parser for Xike OS 'show interface brief' output."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
from typing import Any, TYPE_CHECKING

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule

InterfaceFacts = dict[str, Any]


class InterfacesFacts(object):
    """Gather base interface facts from Xike OS devices."""

    def __init__(self, module: "AnsibleModule") -> None:
        self.module = module
        self.facts: dict[str, InterfaceFacts] = {}
        self._get_facts()

    def _get_facts(self) -> None:
        """Collect interface brief data and index it by interface name."""
        try:
            stdout = run_commands(self.module, ['show interface brief'], check_rc=True) or []
            output = to_text(stdout[0] if stdout else '', errors='surrogate_or_strict')
            self.facts = {iface['name']: iface for iface in parse_interface_brief(output)}
        except Exception as exc:
            self.module.fail_json(msg='failed to gather interface facts: {0}'.format(to_text(exc)))

    def get_facts(self) -> dict[str, InterfaceFacts]:
        """Return the parsed interface facts."""
        return self.facts


def parse_interface_brief(output: str) -> list[InterfaceFacts]:
    """
    Parse 'show interface brief' output into a list of interface dicts.

    Expected output format:
        Port    Desc   Link shutdn Speed         Pri PVID Mode TagVlan    UtVlan
        --------------------------------------------------------------------------------
        e0/0/1  test   up   enable  1000(FD)      0  1    TRK  100        -
        e0/0/2  -      up   enable  auto(FD)     0  1    ACC  -          -
        e0/0/3  -      down disable -            0  1    ACC  -          -

    Returns:
        list of dict, each with keys: name, description, link, shutdown,
        speed, duplex, priority, pvid, mode, tag_vlan, untag_vlan
    """
    interfaces: list[InterfaceFacts] = []

    if not output:
        return interfaces

    lines = output.strip().splitlines()

    # Skip header lines (first 2 lines: header + separator)
    data_lines = []
    header_seen = False
    for line in lines:
        stripped = line.strip()
        # Skip empty lines and separator lines (all dashes)
        if not stripped or re.match(r'^[-=]+$', stripped):
            # This is the separator; next non-empty non-separator line is data
            header_seen = True
            continue
        if header_seen or (not re.match(r'^Port\b', stripped, re.IGNORECASE)):
            data_lines.append(stripped)

    # Regex pattern matching the column layout:
    # Port  Desc  Link  shutdn  Speed  Pri  PVID  Mode  TagVlan  UtVlan
    # Adjust widths based on the sample output
    pattern = re.compile(
        r'^(\S+)'           # Port (e0/0/1)
        r'\s+(\S+|-)'       # Desc
        r'\s+(\S+)'         # Link (up/down)
        r'\s+(\S+)'         # shutdn (enable/disable)
        r'\s+(\S+|-)'       # Speed (1000(FD), auto(FD), -)
        r'\s+(\S+)'         # Pri
        r'\s+(\S+)'         # PVID
        r'\s+(\S+)'         # Mode (TRK/ACC)
        r'\s+(\S+|-)'       # TagVlan
        r'\s+(\S+|-)'       # UtVlan
    )

    for line in data_lines:
        m = pattern.match(line)
        if not m:
            continue

        port = m.group(1)
        desc_raw = m.group(2)
        link = m.group(3)
        shutdn_raw = m.group(4)
        speed_raw = m.group(5)
        pri = m.group(6)
        pvid = m.group(7)
        mode = m.group(8)
        tag_vlan = m.group(9)
        utag_vlan = m.group(10)

        # Normalize port name: e0/0/1 -> ethernet 0/0/1
        name = port
        if port.startswith('e') and '/' in port:
            name = 'ethernet ' + port[1:]

        # Description: '-' means none
        description = None if desc_raw == '-' else desc_raw

        # Admin state
        shutdown = shutdn_raw.lower() == 'disable'

        # Parse speed and duplex from e.g. "1000(FD)" or "auto(FD)" or "-"
        speed = None
        duplex = None
        if speed_raw and speed_raw != '-':
            # Extract speed and duplex from "1000(FD)" format
            sm = re.match(r'(\w+)\((\w+)\)', speed_raw)
            if sm:
                speed = sm.group(1)
                duplex = sm.group(2).lower()  # FD -> full, HD -> half
            else:
                speed = speed_raw

        # VLANs: '-' means none
        tag_vlan_val = None if tag_vlan == '-' else tag_vlan
        utag_vlan_val = None if utag_vlan == '-' else utag_vlan

        iface = {
            'name': name,
            'description': description,
            'link': link,
            'shutdown': shutdown,
            'speed': speed,
            'duplex': duplex,
            'priority': pri,
            'pvid': pvid,
            'mode': mode,
            'tag_vlan': tag_vlan_val,
            'untag_vlan': utag_vlan_val,
        }
        interfaces.append(iface)

    return interfaces
