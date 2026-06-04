# -*- coding: utf-8 -*-

"""ACL facts for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re


class AclsFacts(object):
    """Gather ACL facts from Xike OS devices."""

    def __init__(self, module):
        self.module = module
        self.facts = {'acls': [], 'acl_bindings': []}
        self._get_facts()

    def _get_facts(self):
        """Parse ACL information.

        Executes 'show access-list config' and 'show access-list runtime'
        on the device to gather ACL configurations and bindings.
        """
        try:
            # Get ACL configuration
            rc, out, err = self.module.run_command('show access-list config')
            if rc == 0:
                self.facts['acls'] = parse_access_list_config(out)

            # Get ACL bindings (runtime)
            rc2, out2, err2 = self.module.run_command('show access-list runtime')
            if rc2 == 0:
                self.facts['acl_bindings'] = parse_access_list_runtime(out2)
        except Exception:
            pass


def parse_access_list_config(output):
    """
    Parse 'show access-list config' output.

    Expected output format:
    -------------------------------------------------------
    ACL ID: 1 (Standard IP ACL)
    -------------------------------------------------------
    10 permit 192.168.1.0 0.0.0.255
    20 deny any

    -------------------------------------------------------
    ACL ID: 1001 (MAC ACL)
    -------------------------------------------------------
    10 permit 0011.2233.4455 0000.0000.0000
    20 deny any

    -------------------------------------------------------
    ACL ID: 2001 (Mixed ACL)
    -------------------------------------------------------
    10 permit ip 192.168.1.0 0.0.0.255 any
    20 deny tcp any any eq 80

    Or alternate format:
    access-list 1 permit 192.168.1.0 0.0.0.255
    access-list 1 deny any
    access-list 1001 permit 0011.2233.4455 0000.0000.0000
    access-list 2001 permit ip 192.168.1.0 0.0.0.255 any
    """
    acls = []
    if not output:
        return acls

    lines = output.strip().split('\n')

    # Try to detect format
    if any('ACL ID:' in line for line in lines):
        acls = _parse_block_format(lines)
    elif any(line.strip().startswith('access-list ') for line in lines):
        acls = _parse_inline_format(lines)
    else:
        acls = _parse_generic_format(lines)

    return acls


def _parse_block_format(lines):
    """Parse block-style ACL config output."""
    acls = []
    current_acl = None
    current_rules = []

    for line in lines:
        stripped = line.strip()

        # Match ACL ID header: "ACL ID: 1 (Standard IP ACL)"
        match = re.match(r'ACL ID:\s*(\d+)(?:\s*\((.+)\))?', stripped)
        if match:
            # Save previous ACL
            if current_acl is not None:
                current_acl['rules'] = current_rules
                acls.append(current_acl)

            acl_id = int(match.group(1))
            acl_desc = match.group(2) or ''

            # Determine ACL type from description
            acl_type = _determine_acl_type(acl_id, acl_desc)

            current_acl = {
                'acl_id': acl_id,
                'acl_type': acl_type,
                'remark': '',
                'rules': [],
            }
            current_rules = []
            continue

        # Skip separator/header lines
        if stripped.startswith('---') or stripped.startswith('==='):
            continue
        if not stripped:
            continue
        if stripped.lower().startswith('remark'):
            if current_acl:
                current_acl['remark'] = stripped.split(None, 1)[1] if len(stripped.split(None, 1)) > 1 else ''
            continue

        # Parse rule line
        if current_acl is not None:
            rule = _parse_rule_line(stripped, current_acl['acl_type'])
            if rule:
                current_rules.append(rule)

    # Don't forget the last ACL
    if current_acl is not None:
        current_acl['rules'] = current_rules
        acls.append(current_acl)

    return acls


def _parse_inline_format(lines):
    """Parse inline 'access-list <id> ...' format."""
    acl_map = {}

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('!'):
            continue

        # Match: access-list <id> [permit|deny] <protocol> <src> <dst>
        match = re.match(r'access-list\s+(\d+)\s+(permit|deny)\s+(.*)', stripped)
        if match:
            acl_id = int(match.group(1))
            action = match.group(2)
            rest = match.group(3)

            if acl_id not in acl_map:
                acl_type = _determine_acl_type(acl_id, '')
                acl_map[acl_id] = {
                    'acl_id': acl_id,
                    'acl_type': acl_type,
                    'remark': '',
                    'rules': [],
                }

            # Parse the rest based on ACL type
            rule = _parse_rule_rest(action, rest, acl_map[acl_id]['acl_type'])
            if rule:
                acl_map[acl_id]['rules'].append(rule)

    # Convert to sorted list
    return [acl_map[aid] for aid in sorted(acl_map.keys())]


def _parse_generic_format(lines):
    """Parse generic format where rules are listed without clear ACL ID headers."""
    acls = []
    current_acl = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Try to find ACL ID in various formats
        # Format: "1 permit 192.168.1.0 0.0.0.255"
        # Format: "10 permit ip any any"
        match = re.match(r'^(\d+)\s+(permit|deny)\s+(.*)', stripped)
        if match:
            acl_id = int(match.group(1))
            action = match.group(2)
            rest = match.group(3)

            # Determine ACL type from ID range
            acl_type = _determine_acl_type(acl_id, '')

            if current_acl is None or current_acl['acl_id'] != acl_id:
                if current_acl is not None:
                    acls.append(current_acl)

                current_acl = {
                    'acl_id': acl_id,
                    'acl_type': acl_type,
                    'remark': '',
                    'rules': [],
                }

            rule = _parse_rule_rest(action, rest, acl_type)
            if rule:
                current_acl['rules'].append(rule)

    if current_acl is not None:
        acls.append(current_acl)

    return acls


def _determine_acl_type(acl_id, description=''):
    """Determine ACL type from ID range and/or description.

    Xike ACL numbering:
    - Standard ACL: 1-999
    - MAC ACL: 1000-1999
    - Mixed ACL: 2000-2999
    """
    desc_lower = description.lower()
    if 'standard' in desc_lower or 'ip acl' in desc_lower:
        return 'standard'
    if 'mac' in desc_lower:
        return 'mac'
    if 'mixed' in desc_lower:
        return 'mixed'

    if 1 <= acl_id <= 999:
        return 'standard'
    elif 1000 <= acl_id <= 1999:
        return 'mac'
    elif 2000 <= acl_id <= 2999:
        return 'mixed'

    return 'standard'


def _parse_rule_line(line, acl_type):
    """Parse a rule line within a block format."""
    # Match: <seq> <action> <rest>
    match = re.match(r'^(\d+)?\s*(permit|deny)\s+(.*)', line, re.IGNORECASE)
    if not match:
        return None

    action = match.group(2).lower()
    rest = match.group(3)

    return _parse_rule_rest(action, rest, acl_type)


def _parse_rule_rest(action, rest, acl_type):
    """Parse the remaining part of a rule after action keyword."""
    parts = rest.split()

    if not parts:
        return None

    rule = {
        'action': action,
        'protocol': '',
        'source': '',
        'destination': '',
        'remark': '',
    }

    if acl_type == 'standard':
        # Standard ACL: permit/deny <source> [wildcard]
        # e.g., "permit 192.168.1.0 0.0.0.255"
        # e.g., "permit any"
        rule['protocol'] = 'ip'
        source = parts[0]
        if len(parts) > 1 and _looks_like_wildcard(parts[1]):
            source = source + ' ' + parts[1]
        rule['source'] = source
        rule['destination'] = 'any'

    elif acl_type == 'mac':
        # MAC ACL: permit/deny <src_mac> <dst_mac>
        # e.g., "permit 0011.2233.4455 0000.0000.0000"
        rule['protocol'] = 'mac'
        if len(parts) >= 2:
            rule['source'] = parts[0]
            rule['destination'] = parts[1]
        elif len(parts) == 1:
            rule['source'] = parts[0]
            rule['destination'] = 'any'

    elif acl_type == 'mixed':
        # Mixed ACL: permit/deny <protocol> <src> <dst> [options]
        # e.g., "permit ip 192.168.1.0 0.0.0.255 any"
        # e.g., "deny tcp any any eq 80"
        if len(parts) >= 1 and parts[0].lower() in ('ip', 'tcp', 'udp', 'icmp', 'gre', 'ospf'):
            rule['protocol'] = parts[0]
            if len(parts) >= 3:
                rule['source'] = parts[1]
                rule['destination'] = parts[2]
            elif len(parts) == 2:
                rule['source'] = parts[1]
                rule['destination'] = 'any'
        else:
            # Treat first part as source
            rule['protocol'] = 'ip'
            if len(parts) >= 2:
                rule['source'] = parts[0]
                rule['destination'] = parts[1]
            elif len(parts) == 1:
                rule['source'] = parts[0]
                rule['destination'] = 'any'

    return rule


def _looks_like_wildcard(token):
    """Check if a token looks like a wildcard mask."""
    if token == '0.0.0.0':
        return True
    parts = token.split('.')
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        return True
    return False


def parse_access_list_runtime(output):
    """
    Parse 'show access-list runtime' output for ACL bindings.

    Expected output format:
    Interface: Vlan10
      Direction: inbound
        IP ACL: 100
        MAC ACL: 1001

    Interface: Vlan20
      Direction: outbound
        IP ACL: 200
        MAC ACL: 2002
    """
    bindings = []
    if not output:
        return bindings

    current_iface = None
    current_direction = None

    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        # Match interface line
        match = re.match(r'Interface:\s*(\S+)', stripped, re.IGNORECASE)
        if match:
            current_iface = match.group(1)
            current_direction = None
            continue

        # Match direction line
        match = re.match(r'Direction:\s*(\S+)', stripped, re.IGNORECASE)
        if match:
            current_direction = match.group(1).lower()
            continue

        # Match ACL binding
        match = re.match(r'(?:IP|MAC|IPv6)\s+ACL:\s*(\d+)', stripped, re.IGNORECASE)
        if match and current_iface:
            acl_id = int(match.group(1))
            # Determine if IP or MAC from the line prefix
            is_mac = 'mac' in stripped.lower()
            bindings.append({
                'interface': current_iface,
                'direction': current_direction or 'inbound',
                'acl_id': acl_id,
                'acl_type': 'mac' if is_mac else 'ip',
            })

    return bindings


def parse_running_config(config_text):
    """Parse ACL configuration from running-config output.

    Looks for lines like:
        access-list 1 permit 192.168.1.0 0.0.0.255
        access-list 1 deny any
        access-list 1001 permit 0011.2233.4455 0000.0000.0000
        access-list 2001 permit ip 192.168.1.0 0.0.0.255 any

    Also looks for access-group bindings:
        access-group ip-acl 100 in
        access-group mac-acl 1001 out

    Args:
        config_text: Output from 'show running-config'

    Returns:
        dict: {'acls': [...], 'acl_bindings': [...]}
    """
    acl_map = {}
    bindings = []

    for line in config_text.splitlines():
        line = line.strip()

        # Parse access-list rules
        match = re.match(r'access-list\s+(\d+)\s+(permit|deny)\s+(.*)', line)
        if match:
            acl_id = int(match.group(1))
            action = match.group(2)
            rest = match.group(3)

            if acl_id not in acl_map:
                acl_type = _determine_acl_type(acl_id, '')
                acl_map[acl_id] = {
                    'acl_id': acl_id,
                    'acl_type': acl_type,
                    'remark': '',
                    'rules': [],
                }

            rule = _parse_rule_rest(action, rest, acl_map[acl_id]['acl_type'])
            if rule:
                acl_map[acl_id]['rules'].append(rule)
            continue

        # Parse access-group bindings
        # Format: access-group [ip-acl|mac-acl] <id> [in|out]
        match = re.match(
            r'access-group\s+(ip-acl|mac-acl|ipv6-acl)\s+(\d+)\s*(in|out)?',
            line, re.IGNORECASE
        )
        if match:
            acl_type_str = match.group(1).lower()
            acl_id = int(match.group(2))
            direction = match.group(3) or 'inbound'

            bindings.append({
                'interface': '',
                'direction': direction,
                'acl_id': acl_id,
                'acl_type': 'mac' if 'mac' in acl_type_str else 'ip',
            })

    acls = [acl_map[aid] for aid in sorted(acl_map.keys())]

    return {'acls': acls, 'acl_bindings': bindings}
