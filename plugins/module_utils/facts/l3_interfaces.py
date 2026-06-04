# -*- coding: utf-8 -*-

"""L3 Interfaces facts for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class L3InterfacesFacts(object):
    """Gather L3 interface facts from Xike switches."""

    def __init__(self, module):
        self.module = module
        self.facts = {}
        self._get_facts()

    def _get_facts(self):
        """Parse L3 interface information.

        Executes 'show interface vlan-interface' commands on the device
        and parses IP address information.
        """
        self.facts = {}

        try:
            # Try to get VLAN interface list
            rc, out, err = self.module.run_command('show interface vlan-interface')
            if rc != 0:
                return

            # Parse interface names from output
            interfaces = self._parse_interface_list(out)
            for iface_name in interfaces:
                rc2, iface_out, err2 = self.module.run_command(
                    'show interface vlan-interface {0}'.format(iface_name)
                )
                if rc2 == 0:
                    parsed = parse_interface_ip(iface_out)
                    if parsed.get('ipv4') or parsed.get('ipv6'):
                        self.facts[iface_name] = parsed
        except Exception:
            pass

    def _parse_interface_list(self, output):
        """Parse interface names from 'show interface vlan-interface' output."""
        interfaces = []
        for line in output.splitlines():
            line = line.strip()
            # Look for lines like "Vlan-interface1" or "vlan-interface 1"
            lower = line.lower()
            if 'vlan-interface' in lower:
                parts = lower.split('vlan-interface')
                if len(parts) > 1:
                    name_part = parts[-1].strip()
                    # Extract the ID
                    for token in name_part.split():
                        if token.isdigit():
                            interfaces.append('vlan-interface {0}'.format(token))
                            break
        return interfaces


def parse_running_config(config_text):
    """Parse L3 interface configuration from running-config output.

    Args:
        config_text: Output from 'show running-config'

    Returns:
        dict: Parsed interface configurations keyed by interface name
    """
    interfaces = {}
    current_interface = None

    for line in config_text.splitlines():
        line = line.strip()
        if line.startswith('interface vlan-interface'):
            current_interface = line.split(' ', 2)[2] if len(line.split(' ')) > 2 else line.split(' ', 1)[1]
            interfaces[current_interface] = {
                'ipv4': [],
                'ipv6': [],
            }
        elif current_interface and line.startswith('ip address '):
            # Format: ip address 192.168.1.1 255.255.255.0
            parts = line.split()
            if len(parts) >= 4:
                addr = parts[2]
                mask = parts[3]
                interfaces[current_interface]['ipv4'].append({
                    'address': addr,
                    'subnet_mask': mask,
                })
        elif current_interface and line.startswith('ipv6 address '):
            # Format: ipv6 address 2001:db8::1/64
            addr_part = line.split('ipv6 address ', 1)[1].strip()
            if '/' in addr_part:
                addr, prefix = addr_part.rsplit('/', 1)
                interfaces[current_interface]['ipv6'].append({
                    'address': addr,
                    'subnet': int(prefix),
                })
            else:
                interfaces[current_interface]['ipv6'].append({
                    'address': addr_part,
                })

    return interfaces


def parse_interface_ip(output):
    """Parse 'show interface vlan-interface <id>' output for IP addresses.

    Args:
        output: Output from 'show interface vlan-interface <id>'

    Returns:
        dict: Interface IP configuration with 'ipv4' and 'ipv6' lists
    """
    result = {
        'ipv4': [],
        'ipv6': [],
    }

    for line in output.splitlines():
        line = line.strip()
        # IPv4: "IP Address: 192.168.1.1" or "ip address 192.168.1.1 255.255.255.0"
        lower = line.lower()
        if 'ip address' in lower and 'ipv6' not in lower:
            if ':' in line:
                # Format: "IP Address: 192.168.1.1   Subnet Mask: 255.255.255.0"
                addr_part = line.split(':')[-1].strip()
                result['ipv4'].append({'address': addr_part, 'subnet_mask': ''})
            else:
                parts = line.split()
                if len(parts) >= 4:
                    addr = parts[2]
                    mask = parts[3]
                    result['ipv4'].append({'address': addr, 'subnet_mask': mask})
        elif 'ipv6 address' in lower:
            if ':' in line and '/' in line:
                # Format: "IPv6 Address: 2001:db8::1/64"
                addr_part = line.split(':', 2)[-1].strip() if line.lower().startswith('ipv6') else line.split(':')[-1].strip()
                if '/' in addr_part:
                    addr, prefix = addr_part.rsplit('/', 1)
                    result['ipv6'].append({'address': addr, 'subnet': int(prefix)})
            else:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() == 'address' and i + 1 < len(parts):
                        addr = parts[i + 1]
                        if '/' in addr:
                            a, p = addr.rsplit('/', 1)
                            result['ipv6'].append({'address': a, 'subnet': int(p)})
                        else:
                            result['ipv6'].append({'address': addr})

    return result
