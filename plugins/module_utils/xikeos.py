"""Common utilities for Xike OS modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

# Command mappings:兮克命令 vs Cisco IOS 命令
COMMAND_MAP = {
    'show_version': 'show version',
    'show_vlan_brief': 'show vlan brief',
    'show_interface': 'show interface',
    'show_interface_brief': 'show interface brief',
    'show_ip_route': 'show ip route',
    'show_ip_ospf_neighbor': 'show ip ospf neighbor',
    'show_mac_address_table': 'show mac-address-table',
    'show_stp': 'show stp interface brief',
    'show_running_config': 'show running-config',
    'configure_terminal': 'configure terminal',
    'write_memory': 'write memory',
}

# VLAN mode commands (兮克在 VLAN 模式下操作端口，思科在接口模式下)
VLAN_MODE_COMMANDS = {
    'add_port': 'switchport ethernet {port}',
    'remove_port': 'no switchport ethernet {port}',
}

# Interface mode commands
INTERFACE_COMMANDS = {
    'set_pvid': 'switchport pvid {vlan_id}',
    'set_link_type': 'switchport link-type {mode}',
    'set_trunk_allowed': 'switchport trunk allowed vlan {vlans}',
    'set_hybrid_untagged': 'switchport hybrid untagged vlan {vlans}',
    'set_hybrid_tagged': 'switchport hybrid tagged vlan {vlans}',
}

# Port speed options
SPEED_OPTIONS = ['10', '100', '1000', '10000', 'auto']

# Duplex options
DUPLEX_OPTIONS = ['auto', 'full', 'half']


def map_command(key):
    """Map a logical command key to Xike CLI command."""
    return COMMAND_MAP.get(key, key)
