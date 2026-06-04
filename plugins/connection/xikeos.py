from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
connection: xikeos
short_description: Xike switch SSH connection plugin
version_added: "0.1.0"
description:
  - SSH connection plugin for Xike (兮克) switches.
  - Uses netmiko raisecom device_type as backend.
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
  connection: xike.xikeos.xikeos
  gather_facts: no
  tasks:
    - name: Get version info
      xike.xikeos.xikeos_command:
        commands:
          - show version
"""

RETURN = """
  _device_type:
    description: Netmiko device type used for the connection
    returned: always
    type: str
    sample: raisecom
"""

from ansible_collections.ansible.netcommon.plugins.connection.network_cli import Connection as NetworkCliConnection


class Connection(NetworkCliConnection):
    """Xike switch SSH connection using netmiko raisecom backend."""

    transport = 'network_cli'
    # The device_type for netmiko - maps to raisecom ROAP CLI style
    DEFAULT_NETWORK_OS = 'xike.xikeos'

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
