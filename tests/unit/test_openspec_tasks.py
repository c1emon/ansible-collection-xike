"""Unit tests for the OpenSpec task coverage."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import ast
import json
from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from ansible_collections.c1emon.xikeos.plugins.cliconf import xikeos as cliconf_module
from ansible_collections.c1emon.xikeos.plugins.cliconf.xikeos import Cliconf
from ansible_collections.c1emon.xikeos.plugins.action import xikeos_vlans as action_vlans_module
from ansible_collections.c1emon.xikeos.plugins.modules import (
    xikeos_command as command_module,
    xikeos_acls as acls_module,
    xikeos_config as config_module,
    xikeos_eaps as eaps_module,
    xikeos_erps as erps_module,
    xikeos_flex_monitor_link as flex_monitor_link_module,
    xikeos_facts as facts_module,
    xikeos_interfaces as interfaces_module,
    xikeos_l2_interfaces as l2_interfaces_module,
    xikeos_l3_interfaces as l3_interfaces_module,
    xikeos_lag_interfaces as lag_interfaces_module,
    xikeos_mirror as mirror_module,
    xikeos_ospf_v2 as ospf_v2_module,
    xikeos_port_isolate as port_isolate_module,
    xikeos_qinq as qinq_module,
    xikeos_static_routes as static_routes_module,
    xikeos_stp as stp_module,
    xikeos_vlans as vlans_module,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos import xikeos as network_utils
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos import errors as xikeos_errors
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos import safety as safety_utils
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts import ospfv2 as ospfv2_facts_module
from ansible_collections.c1emon.xikeos.plugins.terminal.xikeos import TerminalModule

from .lifecycle_helpers import ExitJson, fake_module


def _fake_module(params, check_mode=False):
    return fake_module(params, check_mode=check_mode)


RESOURCE_MODULES_DIR = Path(__file__).resolve().parents[2] / "plugins" / "modules"
RESOURCE_MODULE_NAMES = {
    "xikeos_acls.py",
    "xikeos_eaps.py",
    "xikeos_erps.py",
    "xikeos_flex_monitor_link.py",
    "xikeos_interfaces.py",
    "xikeos_l2_interfaces.py",
    "xikeos_l3_interfaces.py",
    "xikeos_lag_interfaces.py",
    "xikeos_mirror.py",
    "xikeos_ospf_v2.py",
    "xikeos_port_isolate.py",
    "xikeos_qinq.py",
    "xikeos_static_routes.py",
    "xikeos_stp.py",
    "xikeos_vlans.py",
}


def test_resource_modules_do_not_use_local_run_command_for_device_configuration():
    offenders = []
    for module_path in sorted(RESOURCE_MODULES_DIR.glob("xikeos_*.py")):
        if module_path.name not in RESOURCE_MODULE_NAMES:
            continue
        tree = ast.parse(module_path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "run_command":
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "module":
                    offenders.append("{0}:{1}".format(module_path.name, node.lineno))

    assert offenders == []


def test_terminal_regexes_and_open_shell_calls():
    assert TerminalModule.terminal_stdout_re[0].search(b"\nrouter(config-if)#")
    assert TerminalModule.terminal_stdout_re[0].search(b"\nrouter(config-router-af)#")
    assert TerminalModule.terminal_stderr_re[1].search(b"Invalid input detected")
    assert TerminalModule.terminal_config_prompt.fullmatch("router(config-if)#")
    assert TerminalModule.terminal_config_prompt.fullmatch("router(config-router-af)#")

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

    assert plugin.get_config(source="startup", flags=["all", "brief"], format="text") == "running-config"
    plugin.send_command.assert_called_with("show startup-config all brief")

    plugin.send_command.reset_mock(side_effect=True)
    plugin.send_command.side_effect = ["term", "vlan", "name", "end"]
    result = json.loads(plugin.edit_config(candidate=[{"command": "vlan 100"}, "! ignored", "end", "name DATA"]))
    assert result == {"diff": "", "request": ["vlan 100", "name DATA"], "response": ["vlan", "name"]}
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


@pytest.mark.parametrize(
    "version_line, expected_hostname",
    [("Hostname: core-switch", "core-switch"), ("System name: edge-switch", "edge-switch")],
)
def test_cliconf_get_device_info_parses_hostname_variants(version_line, expected_hostname):
    plugin = Cliconf.__new__(Cliconf)
    plugin.get = Mock(return_value="\n".join([version_line, "Software version: 1.2.3", "Model: X1000"]))

    info = plugin.get_device_info()

    assert info["network_os"] == "xikeos"
    assert info["network_os_version"] == "1.2.3"
    assert info["network_os_model"] == "X1000"
    assert info["network_os_hostname"] == expected_hostname


def test_network_load_config_uses_candidate_and_propagates_typeerror():
    module = Mock()
    connection = Mock()
    connection.edit_config.side_effect = [TypeError("candidate is required"), {"response": ["ok"]}]

    with patch.object(network_utils, "get_connection", return_value=connection):
        with pytest.raises(TypeError, match="candidate is required"):
            network_utils.load_config(module, ["vlan 10"])

    connection.edit_config.assert_called_once_with(candidate=["vlan 10"])


def test_network_helpers_raise_typed_errors_on_connection_failure():
    module = Mock()
    connection = Mock()
    connection.run_commands.side_effect = network_utils.ConnectionError("transport lost")
    connection.get_config.side_effect = network_utils.ConnectionError("config lost")
    connection.edit_config.side_effect = network_utils.ConnectionError("apply lost")

    with patch.object(network_utils, "get_connection", return_value=connection):
        with pytest.raises(xikeos_errors.XikeOSCommandError):
            network_utils.run_commands(module, ["show version"])

    with patch.object(network_utils, "get_connection", return_value=connection):
        with pytest.raises(xikeos_errors.XikeOSConnectionError):
            network_utils.get_config(module)

    with patch.object(network_utils, "get_connection", return_value=connection):
        with pytest.raises(xikeos_errors.XikeOSConfigError):
            network_utils.load_config(module, ["vlan 10"])


def test_xikeos_error_string_and_detail_fields():
    err = xikeos_errors.XikeOSConfigError("boom", commands=["vlan 10"], detail="details", context="config")

    assert str(err) == "boom"
    assert err.commands == ["vlan 10"]
    assert err.detail == "details"
    assert err.context == "config"


def test_network_load_config_decodes_json_string_response():
    module = Mock()
    connection = Mock()
    connection.edit_config.return_value = json.dumps({"response": ["ok"], "request": ["vlan 10"]})

    with patch.object(network_utils, "get_connection", return_value=connection):
        assert network_utils.load_config(module, ["vlan 10"]) == {"response": ["ok"], "request": ["vlan 10"]}


def test_network_get_config_uses_flags_and_returns_text():
    module = Mock()
    connection = Mock()
    connection.get_config.return_value = b"running-config"

    with patch.object(network_utils, "get_connection", return_value=connection):
        assert network_utils.get_config(module, flags=["all", "brief"]) == "running-config"

    connection.get_config.assert_called_once_with(source="running", flags=["all", "brief"], format=None)


def test_xikeos_command_stdout_and_lines():
    module = _fake_module({"commands": ["show version", "show vlan"]})
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(
        command_module, "run_commands", return_value=[b"line1\nline2", "single"]
    ):
        with pytest.raises(ExitJson):
            command_module.main()

    result = module.exit_json.call_args.kwargs
    assert result["commands"] == ["show version", "show vlan"]
    assert result["stdout"] == ["line1\nline2", "single"]
    assert result["stdout_lines"] == [["line1", "line2"], ["single"]]
    assert result["changed"] is False


def test_xikeos_command_blocks_mutating_commands_by_default():
    module = _fake_module({"commands": ["reload"], "wait_for": [], "match": "all", "retries": 1, "interval": 0})
    module.fail_json.side_effect = ExitJson
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(command_module, "run_commands") as run_mock:
        with pytest.raises(ExitJson):
            command_module.main()

    run_mock.assert_not_called()
    assert "blocked" in module.fail_json.call_args.kwargs["msg"]
    assert module.fail_json.call_args.kwargs["commands"] == ["reload"]


def test_xikeos_command_unsafe_override_warns_and_waits():
    module = _fake_module(
        {
            "commands": ["reload"],
            "unsafe_allow_mutating_commands": True,
            "wait_for": ["result[0] contains ready"],
            "match": "all",
            "retries": 2,
            "interval": 0,
        }
    )
    module.warn = Mock()
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(
        command_module, "run_commands", side_effect=[["not yet"], ["ready"]]
    ):
        with pytest.raises(ExitJson):
            command_module.main()

    module.warn.assert_called_once()
    assert module.exit_json.call_args.kwargs["changed"] is True
    assert module.exit_json.call_args.kwargs["stdout"] == ["ready"]


def test_xikeos_command_check_mode_skips_network_for_guarded_commands():
    module = _fake_module(
        {
            "commands": ["reload"],
            "unsafe_allow_mutating_commands": True,
            "wait_for": ["result[0] contains ready"],
            "match": "all",
            "retries": 2,
            "interval": 0,
        },
        check_mode=True,
    )
    module.warn = Mock()
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(
        command_module, "run_commands"
    ) as run_mock:
        with pytest.raises(ExitJson):
            command_module.main()

    module.warn.assert_called_once()
    run_mock.assert_not_called()
    assert module.exit_json.call_args.kwargs == {
        "changed": True,
        "commands": ["reload"],
        "stdout": [],
        "stdout_lines": [],
    }


def test_xikeos_command_check_mode_keeps_show_command_behavior():
    module = _fake_module({"commands": ["show version"]}, check_mode=True)
    with patch.object(command_module, "AnsibleModule", return_value=module), patch.object(
        command_module, "run_commands", return_value=[b"line1\nline2"]
    ) as run_mock:
        with pytest.raises(ExitJson):
            command_module.main()

    run_mock.assert_called_once_with(module, ["show version"], check_rc=True)
    assert module.exit_json.call_args.kwargs["changed"] is False
    assert module.exit_json.call_args.kwargs["stdout"] == ["line1\nline2"]
    assert module.exit_json.call_args.kwargs["stdout_lines"] == [["line1", "line2"]]


def test_redaction_preserves_context_and_hides_secret_values():
    output = "username admin password supersecret\nsnmp-server community public RO\ninterface ethernet 1/0/1"
    redacted = safety_utils.redact_text(output)
    assert "supersecret" not in redacted
    assert "public" not in redacted
    assert safety_utils.REDACTION_MARKER in redacted
    assert "interface ethernet 1/0/1" in redacted


def test_xikeos_facts_minimum_device_facts():
    module = _fake_module({"gather_subset": ["min"], "gather_network_resources": []})
    version_output = "Hostname: core-switch\nSoftware version: V300SP10240912\nModel: SKS8300\nSerial number: SN123"
    with patch.object(facts_module, "AnsibleModule", return_value=module), patch.object(
        facts_module, "run_commands", return_value=[version_output]
    ):
        with pytest.raises(ExitJson):
            facts_module.main()

    facts = module.exit_json.call_args.kwargs["ansible_facts"]
    assert facts["ansible_net_hostname"] == "core-switch"
    assert facts["ansible_net_model"] == "SKS8300"
    assert facts["ansible_net_version"] == "V300SP10240912"
    assert facts["ansible_net_serialnum"] == "SN123"
    assert facts["ansible_net_api"] == "cliconf"
    assert facts["ansible_net_gather_subset"] == ["min"]
    assert facts["ansible_net_gather_network_resources"] == []
    assert "ansible_network_resources" not in facts


def test_xikeos_facts_gathers_resource_facts_under_ansible_network_resources():
    module = _fake_module({"gather_subset": ["min"], "gather_network_resources": ["vlans", "interfaces"]})
    with patch.object(facts_module, "AnsibleModule", return_value=module), patch.object(
        facts_module, "run_commands", return_value=["Hostname: core"]
    ), patch.object(facts_module, "gather_vlans", return_value=[{"vlan_id": 10, "name": "DATA", "state": "active"}]), patch.object(
        facts_module, "gather_interfaces", return_value={"ethernet 1/0/1": {"description": "uplink", "enabled": True}}
    ):
        with pytest.raises(ExitJson):
            facts_module.main()

    facts = module.exit_json.call_args.kwargs["ansible_facts"]
    assert facts["ansible_net_gather_network_resources"] == ["vlans", "interfaces"]
    assert facts["ansible_network_resources"]["vlans"] == [{"vlan_id": 10, "name": "DATA", "state": "active"}]
    assert facts["ansible_network_resources"]["interfaces"] == [
        {"name": "ethernet 1/0/1", "description": "uplink", "enabled": True}
    ]


def test_xikeos_facts_reports_context_for_typed_gather_failures():
    module = _fake_module({"gather_subset": ["min"], "gather_network_resources": ["vlans"]})
    module.fail_json.side_effect = ExitJson

    with patch.object(facts_module, "AnsibleModule", return_value=module), patch.object(
        facts_module, "run_commands", side_effect=xikeos_errors.XikeOSCommandError("show version failed", commands=["show version"], detail="lost")
    ), patch.object(facts_module, "gather_vlans", side_effect=xikeos_errors.XikeOSFactsError("vlan gather failed", detail="bad", context="vlans")):
        with pytest.raises(ExitJson):
            facts_module.main()

    assert module.fail_json.call_args.kwargs["context"] in {"device", "vlans"}


def test_xikeos_facts_golden_sks8300_resource_shapes_are_config_compatible():
    module = _fake_module({"gather_subset": ["min"], "gather_network_resources": ["vlans", "l2_interfaces", "l3_interfaces"]})
    version_output = "Hostname: sks8300-a\nSoftware version: V300SP10240912\nModel: SKS8300"
    vlan_facts = [{"vlan_id": 10, "name": "servers", "state": "active"}]
    l2_facts = {"ethernet 1/0/1": {"mode": "access", "access_vlan": 10, "pvid": 10}}
    l3_facts = {"vlan-interface 10": {"ipv4": [{"address": "192.0.2.1", "subnet_mask": "255.255.255.0"}], "ipv6": []}}

    with patch.object(facts_module, "AnsibleModule", return_value=module), patch.object(
        facts_module, "run_commands", return_value=[version_output]
    ), patch.object(facts_module, "gather_vlans", return_value=vlan_facts), patch.object(
        facts_module, "gather_l2_interfaces", return_value=l2_facts
    ), patch.object(facts_module, "gather_l3_interfaces", return_value=l3_facts):
        with pytest.raises(ExitJson):
            facts_module.main()

    resources = module.exit_json.call_args.kwargs["ansible_facts"]["ansible_network_resources"]
    assert resources["vlans"] == [{"vlan_id": 10, "name": "servers", "state": "active"}]
    assert resources["l2_interfaces"] == [{"name": "ethernet 1/0/1", "mode": "access", "access_vlan": 10, "pvid": 10}]
    assert resources["l3_interfaces"] == [
        {"name": "vlan-interface 10", "ipv4": [{"address": "192.0.2.1", "subnet_mask": "255.255.255.0"}], "ipv6": []}
    ]


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


def test_xikeos_config_apply_failure_stops_before_save():
    module = _fake_module({"lines": ["vlan 10"], "save": True})
    module.fail_json.side_effect = ExitJson

    with patch.object(config_module, "AnsibleModule", return_value=module), patch.object(
        config_module, "load_config", side_effect=xikeos_errors.XikeOSConfigError("apply failed", commands=["vlan 10"], detail="down")
    ), patch.object(config_module, "run_commands") as run_mock:
        with pytest.raises(ExitJson):
            config_module.main()

    run_mock.assert_not_called()
    assert module.fail_json.call_args.kwargs["changed"] is True
    assert module.fail_json.call_args.kwargs["saved"] is False
    assert module.fail_json.call_args.kwargs["commands"] == ["vlan 10"]


def test_xikeos_config_save_failure_reports_applied_context():
    module = _fake_module({"lines": ["vlan 10"], "save": True})
    module.fail_json.side_effect = ExitJson

    with patch.object(config_module, "AnsibleModule", return_value=module), patch.object(
        config_module, "load_config", return_value={"response": ["ok"]}
    ), patch.object(config_module, "run_commands", side_effect=xikeos_errors.XikeOSCommandError("save failed", commands=[config_module.SAVE_COMMAND], detail="disk full")):
        with pytest.raises(ExitJson):
            config_module.main()

    assert module.fail_json.call_args.kwargs["changed"] is True
    assert module.fail_json.call_args.kwargs["saved"] is False
    assert module.fail_json.call_args.kwargs["commands"] == ["vlan 10", config_module.SAVE_COMMAND]


def test_xikeos_config_warns_or_rejects_unsupported_diff_and_backup():
    module = _fake_module({"lines": ["vlan 10"], "diff": True, "backup": True})
    module.warn = Mock()
    module.fail_json.side_effect = ExitJson

    with patch.object(config_module, "AnsibleModule", return_value=module), patch.object(
        config_module, "load_config", return_value={"response": ["ok"]}
    ) as load_mock:
        with pytest.raises(ExitJson):
            config_module.main()

    assert module.warn.called or module.fail_json.called
    load_mock.assert_not_called()


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

    omitted_name = _fake_module({"config": [{"vlan_id": 100, "state": "active"}], "state": "merged"})
    with patch.object(vlans_module, "AnsibleModule", return_value=omitted_name), patch.object(
        vlans_module, "gather_vlans", return_value=current
    ), patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert omitted_name.exit_json.call_args.kwargs == {
        "changed": False,
        "commands": [],
        "before": current,
        "after": current,
    }
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

    gathered = _fake_module({"config": None, "state": "gathered"})
    gathered_vlans = [{"vlan_id": 10, "name": "dev", "state": "active", "ports": [{"name": "Ethernet1/0/3", "tagged": True}]}]
    with patch.object(vlans_module, "AnsibleModule", return_value=gathered), patch.object(
        vlans_module, "gather_vlans", return_value=gathered_vlans
    ), patch.object(vlans_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            vlans_module.main()

    assert gathered.exit_json.call_args.kwargs == {"changed": False, "gathered": gathered_vlans}
    load_mock.assert_not_called()


def test_xikeos_vlans_gather_vlans_decodes_bytes_and_reports_failures():
    module = Mock()
    module.params = {}
    module.fail_json.side_effect = RuntimeError("gather failed")

    output = b"""VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
10   DATA         Static     ENET      Ethernet1/0/1       Ethernet1/0/2(T)
"""
    with patch.object(vlans_module, "run_commands", return_value=[output]):
        assert vlans_module.gather_vlans(module) == [
            {
                "vlan_id": 10,
                "name": "DATA",
                "state": "active",
                "ports": [
                    {"name": "Ethernet1/0/1", "tagged": False},
                    {"name": "Ethernet1/0/2", "tagged": True},
                ],
                "type": "Static",
                "media": "ENET",
            }
        ]

    failing = Mock()
    failing.fail_json.side_effect = RuntimeError("gather failed")
    with patch.object(vlans_module, "run_commands", side_effect=Exception("connection lost")):
        with pytest.raises(RuntimeError, match="gather failed"):
            vlans_module.gather_vlans(failing)

    assert "show vlan" in failing.fail_json.call_args.kwargs["msg"]
    assert "connection lost" in failing.fail_json.call_args.kwargs["msg"]


def test_xikeos_vlans_fails_explicitly_for_unsupported_mutating_edge_cases():
    suspended = _fake_module({"config": [{"vlan_id": 100, "state": "suspend"}], "state": "merged"})
    suspended.fail_json.side_effect = ExitJson
    with patch.object(vlans_module, "AnsibleModule", return_value=suspended), pytest.raises(ExitJson):
        vlans_module.main()

    assert "suspend" in suspended.fail_json.call_args.kwargs["msg"]

    default_delete = _fake_module({"config": [{"vlan_id": 1}], "state": "deleted"})
    default_delete.fail_json.side_effect = ExitJson
    with patch.object(vlans_module, "AnsibleModule", return_value=default_delete), pytest.raises(ExitJson):
        vlans_module.main()

    assert "VLAN 1" in default_delete.fail_json.call_args.kwargs["msg"]


def test_static_routes_lifecycle_uses_network_apply_and_check_mode_computes_diff():
    existing = [{"destination": "192.168.1.0", "mask": "255.255.255.0", "next_hop": "10.0.0.1", "distance": 1, "route_type": "ipv4"}]
    desired = [{"destination": "192.168.2.0", "mask": "255.255.255.0", "next_hop": "10.0.0.1", "distance": 1, "route_type": "ipv4"}]

    check_module = _fake_module({"config": desired, "state": "merged"}, check_mode=True)
    with patch.object(static_routes_module, "AnsibleModule", return_value=check_module), patch.object(
        static_routes_module, "StaticRoutesFacts"
    ) as facts_mock, patch.object(static_routes_module, "load_config") as load_mock:
        facts_mock.return_value.facts = {"static_routes": existing}
        with pytest.raises(ExitJson):
            static_routes_module.main()

    assert check_module.exit_json.call_args.kwargs["changed"] is True
    assert check_module.exit_json.call_args.kwargs["commands"] == ["ip route 192.168.2.0 255.255.255.0 10.0.0.1"]
    load_mock.assert_not_called()

    module = _fake_module({"config": desired, "state": "merged"})
    with patch.object(static_routes_module, "AnsibleModule", return_value=module), patch.object(
        static_routes_module, "StaticRoutesFacts"
    ) as facts_mock, patch.object(static_routes_module, "load_config") as load_mock:
        facts_mock.side_effect = [Mock(facts={"static_routes": existing}), Mock(facts={"static_routes": desired})]
        with pytest.raises(ExitJson):
            static_routes_module.main()

    assert module.exit_json.call_args.kwargs["after"] == desired
    load_mock.assert_called_once_with(module, ["ip route 192.168.2.0 255.255.255.0 10.0.0.1"])


def test_static_routes_infers_ipv6_route_type_when_omitted():
    route = {"destination": "2001:db8::", "mask": "32", "next_hop": "2001:db8::1"}

    assert static_routes_module.normalize_route(route)["route_type"] == "ipv6"
    assert static_routes_module.route_key(route) == ("2001:db8::", "32", "ipv6")
    assert static_routes_module.build_static_route_commands([route], []) == ["ipv6 route 2001:db8::/32 2001:db8::1"]


def test_static_routes_infers_ipv4_route_type_when_omitted():
    route = {"destination": "192.0.2.0", "mask": "24", "next_hop": "192.0.2.1"}

    assert static_routes_module.normalize_route(route)["route_type"] == "ipv4"
    assert static_routes_module.route_key(route) == ("192.0.2.0", "255.255.255.0", "ipv4")
    assert static_routes_module.build_static_route_commands([route], []) == ["ip route 192.0.2.0 255.255.255.0 192.0.2.1"]


def test_static_routes_rendered_does_not_gather_or_apply():
    route = {"destination": "192.0.2.0", "mask": "24", "next_hop": "192.0.2.1"}
    module = _fake_module({"config": [route], "state": "rendered"})
    with patch.object(static_routes_module, "AnsibleModule", return_value=module), patch.object(
        static_routes_module, "StaticRoutesFacts"
    ) as facts_mock, patch.object(static_routes_module, "load_config") as load_mock:
        with pytest.raises(ExitJson):
            static_routes_module.main()

    assert module.exit_json.call_args.kwargs["changed"] is False
    assert module.exit_json.call_args.kwargs["rendered"] == ["ip route 192.0.2.0 255.255.255.0 192.0.2.1"]
    facts_mock.assert_not_called()
    load_mock.assert_not_called()


def test_static_routes_gathered_returns_gathered_key():
    existing = [{"destination": "192.0.2.0", "mask": "255.255.255.0", "next_hop": "192.0.2.1", "distance": 1, "route_type": "ipv4"}]
    module = _fake_module({"config": [], "state": "gathered"})
    with patch.object(static_routes_module, "AnsibleModule", return_value=module), patch.object(
        static_routes_module, "StaticRoutesFacts"
    ) as facts_mock:
        facts_mock.return_value.facts = {"static_routes": existing}
        with pytest.raises(ExitJson):
            static_routes_module.main()

    assert module.exit_json.call_args.kwargs == {"changed": False, "gathered": existing}


def test_static_routes_facts_failure_is_explicit():
    module = _fake_module({"config": [], "state": "merged"})
    module.fail_json.side_effect = ExitJson
    with patch.object(static_routes_module, "AnsibleModule", return_value=module), patch.object(
        static_routes_module, "StaticRoutesFacts", side_effect=Exception("route gather failed")
    ), pytest.raises(ExitJson):
        static_routes_module.main()

    assert module.fail_json.call_args.kwargs["msg"] == "failed to gather static route facts"
    assert module.fail_json.call_args.kwargs["error"] == "route gather failed"


def test_acls_lifecycle_uses_network_apply_and_check_mode_computes_diff():
    existing = [{"acl_id": 100, "acl_type": "standard", "rules": [{"action": "permit", "source": "10.0.0.0 0.255.255.255", "destination": "any"}]}]
    desired = [{"acl_id": 100, "acl_type": "standard", "rules": [{"action": "deny", "source": "any", "destination": "any"}]}]

    check_module = _fake_module({"config": desired, "state": "merged"}, check_mode=True)
    with patch.object(acls_module, "AnsibleModule", return_value=check_module), patch.object(
        acls_module, "AclsFacts"
    ) as facts_mock, patch.object(acls_module, "load_config") as load_mock:
        facts_mock.return_value.facts = {"acls": existing}
        with pytest.raises(ExitJson):
            acls_module.main()

    assert check_module.exit_json.call_args.kwargs["changed"] is True
    assert check_module.exit_json.call_args.kwargs["commands"] == ["access-list 100 deny any"]
    load_mock.assert_not_called()

    module = _fake_module({"config": desired, "state": "merged"})
    with patch.object(acls_module, "AnsibleModule", return_value=module), patch.object(
        acls_module, "AclsFacts"
    ) as facts_mock, patch.object(acls_module, "load_config") as load_mock:
        facts_mock.side_effect = [Mock(facts={"acls": existing}), Mock(facts={"acls": desired})]
        with pytest.raises(ExitJson):
            acls_module.main()

    assert module.exit_json.call_args.kwargs["after"] == desired
    load_mock.assert_called_once_with(module, ["access-list 100 deny any"])


def test_acls_facts_failure_is_explicit():
    module = _fake_module({"config": [], "state": "merged"})
    module.fail_json.side_effect = ExitJson
    with patch.object(acls_module, "AnsibleModule", return_value=module), patch.object(
        acls_module, "AclsFacts", side_effect=Exception("ACL gather failed")
    ), pytest.raises(ExitJson):
        acls_module.main()

    assert module.fail_json.call_args.kwargs["msg"] == "failed to gather ACL facts"
    assert module.fail_json.call_args.kwargs["error"] == "ACL gather failed"


@pytest.mark.parametrize(
    "module_under_test,facts_attr,facts_class,params,before,after,expected_commands",
    [
        (
            interfaces_module,
            "InterfacesFacts",
            None,
            {"config": [{"name": "ethernet 0/0/1", "description": "new", "enabled": True}], "state": "merged"},
            {"ethernet 0/0/1": {"name": "ethernet 0/0/1", "description": "old", "enabled": True}},
            {"ethernet 0/0/1": {"name": "ethernet 0/0/1", "description": "new", "enabled": True}},
            ["interface ethernet 0/0/1", "description new"],
        ),
        (
            l2_interfaces_module,
            "L2InterfacesFacts",
            None,
            {"config": [{"name": "ethernet 0/0/1", "mode": "access", "access_vlan": 100}], "state": "merged"},
            {"ethernet 0/0/1": {"mode": "access", "access_vlan": 10}},
            {"ethernet 0/0/1": {"mode": "access", "access_vlan": 100}},
            ["interface ethernet 0/0/1", "switchport pvid 100"],
        ),
        (
            l3_interfaces_module,
            "L3InterfacesFacts",
            None,
            {"config": [{"name": "vlan-interface 100", "ipv4": [{"address": "10.0.0.2", "subnet_mask": "255.255.255.0"}]}], "state": "merged"},
            {"vlan-interface 100": {"ipv4": [{"address": "10.0.0.1", "subnet_mask": "255.255.255.0"}], "ipv6": []}},
            {"vlan-interface 100": {"ipv4": [{"address": "10.0.0.1", "subnet_mask": "255.255.255.0"}, {"address": "10.0.0.2", "subnet_mask": "255.255.255.0"}], "ipv6": []}},
            ["interface vlan-interface 100", "ip address 10.0.0.2 255.255.255.0"],
        ),
        (
            lag_interfaces_module,
            "LagInterfacesFacts",
            None,
            {"config": [{"name": "eth-trunk 1", "mode": "static", "members": ["0/0/1"]}], "state": "merged"},
            {"eth-trunk 1": {"name": "eth-trunk 1", "mode": "static", "members": []}},
            {"eth-trunk 1": {"name": "eth-trunk 1", "mode": "static", "members": ["0/0/1"]}},
            ["interface eth-trunk 1", "link-aggregation members ethernet 0/0/1"],
        ),
    ],
)
def test_interface_family_lifecycle(module_under_test, facts_attr, facts_class, params, before, after, expected_commands):
    facts_class = facts_class or getattr(module_under_test, facts_attr)

    unchanged = _fake_module(params)
    with patch.object(module_under_test, "AnsibleModule", return_value=unchanged), patch.object(
        module_under_test, facts_attr
    ) as facts_mock, patch.object(module_under_test, "load_config") as load_mock:
        facts_mock.return_value.get_facts.return_value = after
        with pytest.raises(ExitJson):
            module_under_test.main()

    assert unchanged.exit_json.call_args.kwargs["changed"] is False
    assert unchanged.exit_json.call_args.kwargs["commands"] == []
    load_mock.assert_not_called()

    check_module = _fake_module(params, check_mode=True)
    with patch.object(module_under_test, "AnsibleModule", return_value=check_module), patch.object(
        module_under_test, facts_attr
    ) as facts_mock, patch.object(module_under_test, "load_config") as load_mock:
        facts_mock.return_value.get_facts.return_value = before
        with pytest.raises(ExitJson):
            module_under_test.main()

    assert check_module.exit_json.call_args.kwargs["changed"] is True
    assert check_module.exit_json.call_args.kwargs["commands"] == expected_commands
    load_mock.assert_not_called()

    changed = _fake_module(params)
    with patch.object(module_under_test, "AnsibleModule", return_value=changed), patch.object(
        module_under_test, facts_attr
    ) as facts_mock, patch.object(module_under_test, "load_config") as load_mock:
        facts_mock.return_value.get_facts.side_effect = [before, after]
        with pytest.raises(ExitJson):
            module_under_test.main()

    assert changed.exit_json.call_args.kwargs["changed"] is True
    assert changed.exit_json.call_args.kwargs["after"] == after
    load_mock.assert_called_once_with(changed, expected_commands)

    failing = _fake_module(params)
    failing.fail_json.side_effect = ExitJson
    with patch.object(module_under_test, "AnsibleModule", return_value=failing), patch.object(
        module_under_test, facts_attr, side_effect=Exception("facts failed")
    ), pytest.raises(ExitJson):
        module_under_test.main()

    assert failing.fail_json.call_args.kwargs["msg"].startswith("failed to gather")
    assert failing.fail_json.call_args.kwargs["error"] == "facts failed"


def test_xikeos_ospf_v2_gathers_normalized_before_and_after_facts():
    module = _fake_module({})
    summary_output = """\
Routing Process \"ospf 1\" with ID 1.1.1.1
 Area BACKBONE(0)
"""
    neighbor_output = """\
Neighbor ID     Pri  State           Dead Time   Address         Interface
2.2.2.2           1  FULL/DR         00:00:30    10.0.1.2        vlan-interface 20
"""

    with patch.object(ospf_v2_module, "AnsibleModule", return_value=module), patch.object(
        ospfv2_facts_module, "run_commands", return_value=[summary_output, neighbor_output]
    ):
        with pytest.raises(ExitJson):
            ospf_v2_module.main()

    result = module.exit_json.call_args.kwargs
    assert result["before"] == {
        "processes": {
            1: {
                "process_id": 1,
                "router_id": "1.1.1.1",
                "areas": [{"area_id": "0"}],
                "networks": [],
                "passive_interfaces": [],
            }
        },
        "neighbors": [
            {
                "neighbor_id": "2.2.2.2",
                "priority": 1,
                "state": "FULL/DR",
                "dead_time": "00:00:30",
                "address": "10.0.1.2",
                "interface": "vlan-interface 20",
            }
        ],
    }
    assert result["after"] == result["before"]


def test_xikeos_ospf_v2_surfaces_contextual_fact_gather_failures():
    module = _fake_module({})
    module.fail_json.side_effect = ExitJson

    with patch.object(ospf_v2_module, "AnsibleModule", return_value=module), patch.object(
        ospfv2_facts_module,
        "run_commands",
        side_effect=xikeos_errors.XikeOSCommandError("command execution failed", commands=["show ip ospf"], detail="lost"),
    ):
        with pytest.raises(ExitJson):
            ospf_v2_module.main()

    assert module.fail_json.call_args.kwargs["context"] == "ospf_v2"
    assert module.fail_json.call_args.kwargs["error"] == "command execution failed"


@pytest.mark.parametrize(
    "module_under_test,rendered_params,mutating_params",
    [
        (stp_module, {"config": {"stp_mode": "rstp"}, "state": "rendered"}, {"config": {"stp_mode": "rstp"}, "state": "merged"}),
        (erps_module, {"instance_id": 1, "state": "rendered"}, {"instance_id": 1, "state": "present"}),
        (eaps_module, {"domain_id": 1, "state": "rendered"}, {"domain_id": 1, "state": "present"}),
        (qinq_module, {"config": {"mode": "customer"}, "state": "rendered"}, {"config": {"mode": "customer"}, "state": "merged"}),
        (
            mirror_module,
            {"config": {"group_id": 1, "source_interfaces": [{"name": "cpu", "direction": "both"}]}, "state": "rendered"},
            {"config": {"group_id": 1, "source_interfaces": [{"name": "cpu", "direction": "both"}]}, "state": "present"},
        ),
        (
            port_isolate_module,
            {"config": {"group_id": 1, "members": ["all"]}, "state": "rendered"},
            {"config": {"group_id": 1, "members": ["all"]}, "state": "present"},
        ),
        (
            flex_monitor_link_module,
            {"config": {"flex_links": [{"group_id": 1, "master_port": {"type": "eth", "id": "0/0/1"}}]}, "state": "rendered"},
            {"config": {"flex_links": [{"group_id": 1, "master_port": {"type": "eth", "id": "0/0/1"}}]}, "state": "merged"},
        ),
        (
            ospf_v2_module,
            {"config": {"process_id": 1, "router_id": "1.1.1.1"}, "state": "rendered"},
            {"config": {"process_id": 1, "router_id": "1.1.1.1"}, "state": "merged"},
        ),
    ],
)
def test_specialty_modules_are_rendered_only_or_fail_fast(module_under_test, rendered_params, mutating_params):
    rendered = _fake_module(rendered_params)
    with patch.object(module_under_test, "AnsibleModule", return_value=rendered):
        with pytest.raises(ExitJson):
            module_under_test.main()

    assert rendered.exit_json.call_args.kwargs["changed"] is False
    assert rendered.exit_json.call_args.kwargs["commands"]
    assert rendered.exit_json.call_args.kwargs["rendered"] == rendered.exit_json.call_args.kwargs["commands"]

    mutating = _fake_module(mutating_params)
    mutating.fail_json.side_effect = ExitJson
    with patch.object(module_under_test, "AnsibleModule", return_value=mutating):
        with pytest.raises(ExitJson):
            module_under_test.main()

    assert "state=rendered only" in mutating.fail_json.call_args.kwargs["msg"]
    mutating.exit_json.assert_not_called()


def test_xikeos_vlans_action_injects_bundled_textfsm_template_before_delegating():
    action = action_vlans_module.ActionModule.__new__(action_vlans_module.ActionModule)
    action._task = Mock(args={"_textfsm_templates": {"existing.textfsm": "existing"}})

    with patch.object(
        action_vlans_module.ActionModule,
        "_load_textfsm_template",
        return_value="bundled-template",
    ) as load_mock, patch.object(
        action_vlans_module.NormalActionModule,
        "run",
        return_value={"ok": True},
    ) as parent_run:
        assert action.run(tmp="tmp", task_vars={"foo": "bar"}) == {"ok": True}

    load_mock.assert_called_once_with(action_vlans_module.SHOW_VLAN_TEMPLATE)
    assert action._task.args["_textfsm_templates"] == {
        "existing.textfsm": "existing",
        action_vlans_module.SHOW_VLAN_TEMPLATE: "bundled-template",
    }
    parent_run.assert_called_once_with(tmp="tmp", task_vars={"foo": "bar"})
