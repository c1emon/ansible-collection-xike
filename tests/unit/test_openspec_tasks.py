"""Unit tests for the OpenSpec task coverage."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from unittest.mock import Mock, call, patch

import pytest

from ansible_collections.xike.xikeos.plugins.cliconf import xikeos as cliconf_module
from ansible_collections.xike.xikeos.plugins.cliconf.xikeos import Cliconf
from ansible_collections.xike.xikeos.plugins.modules import (
    xikeos_command as command_module,
    xikeos_config as config_module,
    xikeos_vlans as vlans_module,
)
from ansible_collections.xike.xikeos.plugins.terminal.xikeos import TerminalModule


class ExitJson(Exception):
    pass


def _fake_module(params, check_mode=False):
    module = Mock()
    module.params = params
    module.check_mode = check_mode
    module.exit_json.side_effect = ExitJson
    module.fail_json.side_effect = AssertionError("fail_json should not be called")
    return module


def test_terminal_regexes_and_open_shell_calls():
    assert TerminalModule.terminal_stdout_re[0].search(b"\nrouter(config-if)#")
    assert TerminalModule.terminal_stderr_re[1].search(b"Invalid input detected")
    assert TerminalModule.terminal_config_prompt.fullmatch("router(config-if)#")

    term = TerminalModule.__new__(TerminalModule)
    term._exec_cli_command = Mock()

    term.on_open_shell()

    assert term._exec_cli_command.call_args_list == [
        call(b"terminal length 0"),
        call(b"terminal width 512"),
    ]


def test_cliconf_get_config_edit_config_and_capabilities():
    plugin = Cliconf.__new__(Cliconf)
    plugin.send_command = Mock(side_effect=["running-config", "term", "vlan", "name", "end"])

    assert plugin.get_config(source="startup", flags=["all", "brief"]) == "running-config"
    plugin.send_command.assert_called_with("show startup-config all brief")

    plugin.send_command.reset_mock(side_effect=True)
    plugin.send_command.side_effect = ["term", "vlan", "name", "end"]
    result = plugin.edit_config(candidate=[{"command": "vlan 100"}, "! ignored", "end", "name DATA"])
    assert result == {"request": ["vlan 100", "name DATA"], "response": ["vlan", "name"]}
    assert plugin.send_command.call_args_list == [
        call("configure terminal"),
        call("vlan 100"),
        call("name DATA"),
        call("end"),
    ]

    with patch.object(
        cliconf_module.CliconfBase,
        "get_capabilities",
        return_value={"rpc": [], "device_operations": {}, "format": [], "network_api": ""},
    ):
        capabilities = json.loads(plugin.get_capabilities())

    assert capabilities["rpc"] == ["get_config", "edit_config", "run_commands"]
    assert capabilities["network_api"] == "cliconf"
    assert capabilities["format"] == ["text"]
    assert capabilities["device_operations"]["supports_commit"] is False

    with patch.object(
        cliconf_module.CliconfBase,
        "get_capabilities",
        return_value=json.dumps({"rpc": [], "device_operations": {}, "format": [], "network_api": ""}),
    ):
        capabilities = json.loads(plugin.get_capabilities())

    assert capabilities["rpc"] == ["get_config", "edit_config", "run_commands"]


def test_xikeos_command_stdout_and_lines():
    module = _fake_module({"commands": ["show version", "show vlan brief"]})
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(
        command_module, "run_commands", return_value=[b"line1\nline2", "single"]
    ):
        with pytest.raises(ExitJson):
            command_module.main()

    result = module.exit_json.call_args.kwargs
    assert result["commands"] == ["show version", "show vlan brief"]
    assert result["stdout"] == ["line1\nline2", "single"]
    assert result["stdout_lines"] == [["line1", "line2"], ["single"]]
    assert result["changed"] is False


def test_xikeos_config_check_mode_and_save_flow():
    check_module = _fake_module({"lines": ["vlan 10"], "save": True}, check_mode=True)
    with patch.object(config_module, "AnsibleModule", return_value=check_module), patch.object(
        config_module, "load_config"
    ) as load_mock, patch.object(config_module, "run_commands") as run_mock:
        with pytest.raises(ExitJson):
            config_module.main()

    assert check_module.exit_json.call_args.kwargs == {
        "changed": True,
        "commands": ["vlan 10"],
        "saved": False,
    }
    load_mock.assert_not_called()
    run_mock.assert_not_called()

    module = _fake_module({"lines": ["vlan 10"], "save": True})
    with patch.object(config_module, "AnsibleModule", return_value=module), patch.object(
        config_module, "load_config", return_value={"response": ["ok"]}
    ) as load_mock, patch.object(config_module, "run_commands") as run_mock:
        with pytest.raises(ExitJson):
            config_module.main()

    assert module.exit_json.call_args.kwargs == {
        "changed": True,
        "commands": ["vlan 10", config_module.SAVE_COMMAND],
        "saved": True,
        "response": ["ok"],
    }
    load_mock.assert_called_once_with(module, ["vlan 10"])
    run_mock.assert_called_once_with(module, [config_module.SAVE_COMMAND], check_rc=True)


def test_xikeos_vlans_normalize_and_lifecycle():
    assert vlans_module._normalize_vlan({"vlan_id": "100", "status": "suspend", "ports": ["e0/0/1"]}) == {
        "vlan_id": 100,
        "name": "",
        "state": "suspend",
        "ports": ["e0/0/1"],
    }

    unchanged = _fake_module({"config": [{"vlan_id": 100, "name": "DATA", "state": "active"}], "state": "merged"})
    current = [{"vlan_id": 100, "name": "DATA", "state": "active"}]
    with patch.object(vlans_module, "AnsibleModule", return_value=unchanged), patch.object(
        vlans_module, "gather_vlans", return_value=current
    ) as gather_mock, patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert unchanged.exit_json.call_args.kwargs == {
        "changed": False,
        "commands": [],
        "before": current,
        "after": current,
    }
    gather_mock.assert_called_once_with(unchanged)
    load_mock.assert_not_called()

    changed = _fake_module({"config": [{"vlan_id": 100, "name": "VOICE", "state": "active"}], "state": "merged"})
    with patch.object(vlans_module, "AnsibleModule", return_value=changed), patch.object(
        vlans_module, "gather_vlans", return_value=current
    ), patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert changed.exit_json.call_args.kwargs["changed"] is True
    assert changed.exit_json.call_args.kwargs["commands"] == ["vlan 100", "description VOICE", "exit"]
    assert changed.exit_json.call_args.kwargs["after"] == [{"vlan_id": 100, "name": "VOICE", "state": "active"}]
    load_mock.assert_called_once_with(changed, ["vlan 100", "description VOICE", "exit"])

    deleted = _fake_module({"config": [{"vlan_id": 100}], "state": "deleted"})
    before_deleted = [{"vlan_id": 100, "name": "DATA", "state": "active"}, {"vlan_id": 200, "name": "VOICE", "state": "active"}]
    with patch.object(vlans_module, "AnsibleModule", return_value=deleted), patch.object(
        vlans_module, "gather_vlans", return_value=before_deleted
    ), patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert deleted.exit_json.call_args.kwargs["commands"] == ["no vlan 100"]
    assert deleted.exit_json.call_args.kwargs["after"] == [{"vlan_id": 200, "name": "VOICE", "state": "active"}]
    load_mock.assert_called_once_with(deleted, ["no vlan 100"])

    check_mode = _fake_module({"config": [{"vlan_id": 300, "name": "NEW"}], "state": "merged"}, check_mode=True)
    with patch.object(vlans_module, "AnsibleModule", return_value=check_mode), patch.object(
        vlans_module, "gather_vlans", return_value=[]
    ), patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert check_mode.exit_json.call_args.kwargs["changed"] is True
    assert check_mode.exit_json.call_args.kwargs["commands"] == ["vlan 300", "description NEW", "exit"]
    load_mock.assert_not_called()
