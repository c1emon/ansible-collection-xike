from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

DOCUMENTATION = """
connection: xikeos
short_description: Legacy Xike network_cli compatibility connection plugin
version_added: "0.1.0"
description:
  - Compatibility wrapper around ansible.netcommon.network_cli for Xike (兮克) switches.
  - The supported architecture uses ansible_connection=ansible.netcommon.network_cli and ansible_network_os=c1emon.xikeos.xikeos.
options:
  host:
    description: Target device hostname or IP
    type: str
    required: true
  port:
    description: SSH port
    type: int
    default: 22
  username:
    description: SSH username
    type: str
    required: true
  password:
    description: SSH password
    type: str
    required: true
"""

EXAMPLES = """
- name: Connect to Xike switch
  hosts: xike_switches
  connection: c1emon.xikeos.xikeos
  gather_facts: no
  tasks:
    - name: Get version info
      c1emon.xikeos.xikeos_command:
        commands:
          - show version
"""

RETURN = """
  network_os:
    description: Xike OS network platform selected by network_cli.
    returned: always
    type: str
    sample: c1emon.xikeos.xikeos
"""

from ansible_collections.ansible.netcommon.plugins.connection.network_cli import Connection as NetworkCliConnection


class Connection(NetworkCliConnection):
    """Legacy network_cli compatibility wrapper for Xike OS."""

    transport = 'network_cli'
    # Prefer ansible_network_os=c1emon.xikeos.xikeos with ansible.netcommon.network_cli.
    DEFAULT_NETWORK_OS = 'c1emon.xikeos.xikeos'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the compatibility wrapper."""
        super(Connection, self).__init__(*args, **kwargs)
