"""Shared helpers for resource-module lifecycle tests."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import Mock


class ExitJson(Exception):
    """Raised when a mocked AnsibleModule exits successfully."""


def fake_module(params, check_mode=False):
    module = Mock()
    module.params = params
    module.check_mode = check_mode
    module.exit_json.side_effect = ExitJson
    module.fail_json.side_effect = AssertionError("fail_json should not be called")
    return module


def successful_command_module(params=None, check_mode=False, outputs=None):
    module = fake_module(params or {}, check_mode=check_mode)
    module._socket_path = "/tmp/xikeos-test-socket"
    module._xikeos_command_outputs = outputs or []
    return module


def network_connection(run_outputs=None, edit_response=None):
    connection = Mock()
    connection.run_commands.return_value = run_outputs if run_outputs is not None else []
    connection.edit_config.return_value = edit_response if edit_response is not None else {"response": ["ok"]}
    return connection
