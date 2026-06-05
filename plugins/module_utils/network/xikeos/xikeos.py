from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.connection import Connection, ConnectionError


def get_connection(module):
    if hasattr(module, "_xikeos_connection"):
        return module._xikeos_connection
    module._xikeos_connection = Connection(module._socket_path)
    return module._xikeos_connection


def get_capabilities(module):
    if hasattr(module, "_xikeos_capabilities"):
        return module._xikeos_capabilities
    try:
        capabilities = Connection(module._socket_path).get_capabilities()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
        raise
    module._xikeos_capabilities = json.loads(capabilities)
    return module._xikeos_capabilities


def run_commands(module, commands, check_rc=True):
    connection = get_connection(module)
    try:
        return connection.run_commands(commands=commands, check_rc=check_rc)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc), commands=commands)


def get_config(module, flags=None):
    connection = get_connection(module)
    try:
        return to_text(connection.get_config(flags=flags), errors="surrogate_or_strict")
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def load_config(module, commands):
    connection = get_connection(module)
    try:
        return connection.edit_config(candidate=commands)
    except TypeError:
        return connection.edit_config(commands)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc), commands=commands)
