# -*- coding: utf-8 -*-

"""LAG Interfaces facts for Xike OS (eth-trunk)."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Optional, TYPE_CHECKING

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule

LagState = dict[str, Any]


class LagInterfacesFacts(object):
    """Gather LAG (eth-trunk) interface facts from Xike switches."""

    def __init__(self, module: "AnsibleModule") -> None:
        self.module = module
        self.facts: dict[str, LagState] = {}
        self._get_facts()

    def _get_facts(self) -> None:
        """Parse LAG interface information.

        Executes show running-config through the network connection and parses
        eth-trunk interface blocks.
        """
        try:
            stdout = run_commands(self.module, ['show running-config'], check_rc=True) or []
            output = to_text(stdout[0] if stdout else '', errors='surrogate_or_strict')
            self.facts = parse_lag_config(output)
        except Exception as exc:
            self.module.fail_json(msg='failed to gather LAG interface facts: {0}'.format(to_text(exc)))

    def get_facts(self) -> dict[str, LagState]:
        """Return gathered facts."""
        return self.facts


def parse_lag_config(config_text: str) -> dict[str, LagState]:
    """Parse LAG/eth-trunk configuration from running-config output.

    Looks for blocks like:

        interface eth-trunk 1
         link-aggregation mode dynamic
         link-aggregation members ethernet 0/0/1
         link-aggregation members ethernet 0/0/2
         lacp mode active

    Args:
        config_text: Output from 'show running-config' or similar

    Returns:
        dict: Parsed eth-trunk configurations keyed by trunk name
              (e.g. 'eth-trunk 1')
    """
    trunks: dict[str, LagState] = {}
    current_trunk: Optional[str] = None

    for line in config_text.splitlines():
        line = line.strip()

        if line.startswith('interface eth-trunk'):
            trunk_id = line.split(' ', 2)[-1]
            current_trunk = 'eth-trunk {0}'.format(trunk_id)
            trunks[current_trunk] = {
                'name': current_trunk,
                'mode': None,
                'members': [],
                'lacp_mode': None,
            }
        elif current_trunk and line.startswith('link-aggregation mode'):
            mode = line.split()[-1]
            trunks[current_trunk]['mode'] = mode
        elif current_trunk and line.startswith('link-aggregation members ethernet'):
            port = line.split('ethernet')[-1].strip()
            trunks[current_trunk]['members'].append(port)
        elif current_trunk and line.startswith('lacp mode'):
            lacp = line.split()[-1]
            trunks[current_trunk]['lacp_mode'] = lacp

    return trunks


def parse_lacp_local(output: str) -> LagState:
    """Parse 'show lacp local' output for a single eth-trunk.

    Args:
        output: Output from 'show lacp local'

    Returns:
        dict: LAG configuration with keys: mode, members, lacp_mode
    """
    result: LagState = {
        'mode': None,
        'members': [],
        'lacp_mode': None,
    }

    for line in output.splitlines():
        line = line.strip()
        if 'Link Aggregation Mode' in line or 'link-aggregation mode' in line.lower():
            if ':' in line:
                result['mode'] = line.split(':')[-1].strip().lower()
            else:
                parts = line.split()
                if len(parts) >= 3:
                    result['mode'] = parts[-1].lower()
        elif 'Member' in line or 'members' in line.lower():
            if 'ethernet' in line.lower():
                port = line.split('ethernet')[-1].strip()
                if port:
                    result['members'].append(port)
        elif 'LACP Mode' in line or 'lacp mode' in line.lower():
            if ':' in line:
                result['lacp_mode'] = line.split(':')[-1].strip().lower()
            else:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() == 'mode' and i + 1 < len(parts):
                        result['lacp_mode'] = parts[i + 1].lower()
                        break

    return result
