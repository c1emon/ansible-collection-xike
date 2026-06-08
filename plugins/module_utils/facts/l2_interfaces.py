# -*- coding: utf-8 -*-

"""L2 Interfaces facts for Xike OS."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands


class L2InterfacesFacts(object):
    """Gather L2 interface facts from Xike switches."""

    def __init__(self, module):
        self.module = module
        self.facts = {}
        self._get_facts()

    def _get_facts(self):
        """Parse L2 interface information."""
        try:
            stdout = run_commands(self.module, ['show running-config'], check_rc=True) or []
            output = to_text(stdout[0] if stdout else '', errors='surrogate_or_strict')
            self.facts = parse_switchport_config(output)
        except Exception as exc:
            self.module.fail_json(msg='failed to gather L2 interface facts: {0}'.format(to_text(exc)))

    def get_facts(self):
        """Return gathered facts."""
        return self.facts


def parse_switchport_config(config_text):
    """Parse switchport configuration from running-config output.

    Args:
        config_text: Output from 'show running-config' or similar

    Returns:
        dict: Parsed interface configurations keyed by interface name
    """
    interfaces = {}
    current_interface = None

    for line in config_text.splitlines():
        line = line.strip()
        if line.startswith('interface '):
            current_interface = line.split(' ', 1)[1]
            interfaces[current_interface] = {
                'mode': None,
                'access_vlan': None,
                'trunk_allowed_vlan': None,
                'hybrid_untagged_vlan': None,
                'hybrid_tagged_vlan': None,
                'pvid': None,
            }
        elif current_interface and line.startswith('switchport link-type'):
            mode = line.split()[-1]
            interfaces[current_interface]['mode'] = mode
        elif current_interface and line.startswith('switchport pvid'):
            vlan_id = int(line.split()[-1])
            interfaces[current_interface]['pvid'] = vlan_id
            if interfaces[current_interface]['mode'] == 'access':
                interfaces[current_interface]['access_vlan'] = vlan_id
        elif current_interface and line.startswith('switchport trunk allowed vlan'):
            vlans = line.split('vlan ')[-1]
            interfaces[current_interface]['trunk_allowed_vlan'] = vlans
        elif current_interface and line.startswith('switchport hybrid untagged vlan'):
            vlans = line.split('vlan ')[-1]
            interfaces[current_interface]['hybrid_untagged_vlan'] = vlans
        elif current_interface and line.startswith('switchport hybrid tagged vlan'):
            vlans = line.split('vlan ')[-1]
            interfaces[current_interface]['hybrid_tagged_vlan'] = vlans

    return interfaces


def parse_interface_switchport(output):
    """Parse 'show interface switchport' output for a single interface.

    Args:
        output: Output from 'show interface <name> switchport'

    Returns:
        dict: Interface switchport configuration
    """
    result = {
        'mode': None,
        'access_vlan': None,
        'trunk_allowed_vlan': None,
        'hybrid_untagged_vlan': None,
        'hybrid_tagged_vlan': None,
        'pvid': None,
    }

    for line in output.splitlines():
        line = line.strip()
        if 'Link Type' in line or 'link-type' in line.lower():
            # Format: "Link Type: access" or "link-type access"
            if ':' in line:
                result['mode'] = line.split(':')[-1].strip().lower()
            else:
                parts = line.split()
                if len(parts) >= 3:
                    result['mode'] = parts[-1].lower()
        elif 'PVID' in line or 'pvid' in line.lower():
            if ':' in line:
                try:
                    result['pvid'] = int(line.split(':')[-1].strip())
                except ValueError:
                    pass
            else:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() == 'pvid' and i + 1 < len(parts):
                        try:
                            result['pvid'] = int(parts[i + 1])
                        except ValueError:
                            pass
        elif 'Trunk Allowed VLAN' in line or 'trunk allowed vlan' in line.lower():
            if 'vlan' in line.lower():
                vlans = line.split('vlan')[-1].strip()
                result['trunk_allowed_vlan'] = vlans
        elif 'Hybrid Untagged VLAN' in line or 'hybrid untagged vlan' in line.lower():
            if 'vlan' in line.lower():
                vlans = line.split('vlan')[-1].strip()
                result['hybrid_untagged_vlan'] = vlans
        elif 'Hybrid Tagged VLAN' in line or 'hybrid tagged vlan' in line.lower():
            if 'vlan' in line.lower():
                vlans = line.split('vlan')[-1].strip()
                result['hybrid_tagged_vlan'] = vlans

    return result
