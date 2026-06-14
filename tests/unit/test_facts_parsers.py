"""Unit tests for Xike OS facts parsers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import types
from unittest.mock import Mock

import pytest

# Import parsers directly (no device connection needed)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.vlans import (
    SHOW_VLAN_TEMPLATE,
    parse_vlan,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.textfsm_parser import (
    parse_textfsm_template,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.ttp_parser import (
    _load_ttp_template,
    parse_ttp_template,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.interfaces import (
    parse_interface_brief,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.ospfv2 import (
    Ospfv2Facts,
    parse_ospf_neighbors,
    parse_ospf_summary,
    parse_running_config,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.stp import (
    parse_stp_brief,
    parse_vlan_ranges,
)


# ---------------------------------------------------------------------------
# VLAN parser tests
# ---------------------------------------------------------------------------

class TestVlanParser:
    """Tests for parse_vlan."""

    SAMPLE_OUTPUT = """\
VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
1    default      Static     ENET      Ethernet1/0/1       Ethernet1/0/2(T)
                                       Ethernet1/0/3(T)    Ethernet1/0/4(T)
10   dev          Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
                                       Ethernet1/0/5(T)
21   isp          Static     ENET      Ethernet1/0/2(T)    Ethernet1/0/3(T)
"""

    def test_parse_vlan_returns_list(self):
        result = parse_vlan(self.SAMPLE_OUTPUT)
        assert isinstance(result, list)

    def test_vlan_parser_count(self):
        result = parse_vlan(self.SAMPLE_OUTPUT)
        assert len(result) == 3

    def test_vlan_parser_first_vlan(self):
        result = parse_vlan(self.SAMPLE_OUTPUT)
        vlan = result[0]
        assert vlan["vlan_id"] == 1
        assert vlan["name"] == "default"
        assert vlan["type"] == "Static"
        assert vlan["media"] == "ENET"
        assert vlan["state"] == "active"
        assert vlan["status"] == "active"
        assert vlan["ports"] == [
            {"name": "Ethernet1/0/1", "tagged": False},
            {"name": "Ethernet1/0/2", "tagged": True},
            {"name": "Ethernet1/0/3", "tagged": True},
            {"name": "Ethernet1/0/4", "tagged": True},
        ]

    def test_vlan_parser_second_vlan(self):
        result = parse_vlan(self.SAMPLE_OUTPUT)
        vlan = result[1]
        assert vlan["vlan_id"] == 10
        assert vlan["name"] == "dev"
        assert vlan["status"] == "active"
        assert vlan["ports"] == [
            {"name": "Ethernet1/0/3", "tagged": True},
            {"name": "Ethernet1/0/4", "tagged": True},
            {"name": "Ethernet1/0/5", "tagged": True},
        ]

    def test_vlan_parser_third_vlan(self):
        result = parse_vlan(self.SAMPLE_OUTPUT)
        vlan = result[2]
        assert vlan["vlan_id"] == 21
        assert vlan["name"] == "isp"
        assert vlan["ports"] == [
            {"name": "Ethernet1/0/2", "tagged": True},
            {"name": "Ethernet1/0/3", "tagged": True},
        ]

    def test_vlan_parser_empty_output(self):
        result = parse_vlan("")
        assert result == []

    def test_vlan_parser_no_ports(self):
        output = """\
VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
500  EMPTY        Static     ENET
"""
        result = parse_vlan(output)
        assert len(result) == 1
        assert result[0]["vlan_id"] == 500
        assert result[0]["name"] == "EMPTY"
        assert result[0]["state"] == "active"
        assert result[0]["status"] == "active"
        assert result[0]["type"] == "Static"
        assert result[0]["media"] == "ENET"
        assert result[0]["ports"] == []

    def test_vlan_parser_uses_bundled_textfsm_template(self):
        rows = parse_textfsm_template(self.SAMPLE_OUTPUT, SHOW_VLAN_TEMPLATE)
        assert rows == [
            {
                "vlan_id": "1",
                "name": "default",
                "type": "Static",
                "media": "ENET",
                "ports": ["Ethernet1/0/1", "Ethernet1/0/2(T)", "Ethernet1/0/3(T)", "Ethernet1/0/4(T)"],
            },
            {
                "vlan_id": "10",
                "name": "dev",
                "type": "Static",
                "media": "ENET",
                "ports": ["Ethernet1/0/3(T)", "Ethernet1/0/4(T)", "Ethernet1/0/5(T)"],
            },
            {
                "vlan_id": "21",
                "name": "isp",
                "type": "Static",
                "media": "ENET",
                "ports": ["Ethernet1/0/2(T)", "Ethernet1/0/3(T)"],
            },
        ]

    def test_vlan_parser_supports_multiple_continuation_lines(self):
        output = """\
VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
600  guest        Static     ENET      Ethernet1/0/1
                                       Ethernet1/0/2(T)
                                       Ethernet1/0/3(T)
"""
        result = parse_vlan(output)
        assert result == [
            {
                "vlan_id": 600,
                "name": "guest",
                "type": "Static",
                "media": "ENET",
                "state": "active",
                "status": "active",
                "ports": [
                    {"name": "Ethernet1/0/1", "tagged": False},
                    {"name": "Ethernet1/0/2", "tagged": True},
                    {"name": "Ethernet1/0/3", "tagged": True},
                ],
            }
        ]

    def test_parse_show_vlan_real_switch_output(self):
        output = """\
Switch#show vlan
VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
1    default      Static     ENET      Ethernet1/0/1       Ethernet1/0/2(T)
                                       Ethernet1/0/3(T)    Ethernet1/0/4(T)
                                       Ethernet1/0/5       Ethernet1/0/6
                                       Ethernet1/0/7
10   dev          Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
                                       Ethernet1/0/5(T)    Ethernet1/0/6(T)
                                       Ethernet1/0/7(T)
21   isp          Static     ENET      Ethernet1/0/2(T)    Ethernet1/0/3(T)
                                       Ethernet1/0/4(T)
33   storage      Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/9
                                       Ethernet1/0/10      Ethernet1/0/11
                                       Ethernet1/0/12
40   hole         Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
50   prod         Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
                                       Ethernet1/0/5(T)    Ethernet1/0/6(T)
                                       Ethernet1/0/7(T)    Ethernet1/0/8
99   lan          Static     ENET      Ethernet1/0/2(T)    Ethernet1/0/3(T)
                                       Ethernet1/0/4(T)
"""
        result = parse_vlan(output)

        assert [vlan["vlan_id"] for vlan in result] == [1, 10, 21, 33, 40, 50, 99]
        assert [len(vlan["ports"]) for vlan in result] == [7, 5, 3, 5, 2, 6, 3]
        assert result[0]["ports"] == [
            {"name": "Ethernet1/0/1", "tagged": False},
            {"name": "Ethernet1/0/2", "tagged": True},
            {"name": "Ethernet1/0/3", "tagged": True},
            {"name": "Ethernet1/0/4", "tagged": True},
            {"name": "Ethernet1/0/5", "tagged": False},
            {"name": "Ethernet1/0/6", "tagged": False},
            {"name": "Ethernet1/0/7", "tagged": False},
        ]
        assert result[3]["name"] == "storage"
        assert result[3]["ports"] == [
            {"name": "Ethernet1/0/3", "tagged": True},
            {"name": "Ethernet1/0/9", "tagged": False},
            {"name": "Ethernet1/0/10", "tagged": False},
            {"name": "Ethernet1/0/11", "tagged": False},
            {"name": "Ethernet1/0/12", "tagged": False},
        ]
        assert result[5]["ports"][-1] == {"name": "Ethernet1/0/8", "tagged": False}

    def test_textfsm_helper_missing_template_error_is_actionable(self):
        with pytest.raises(FileNotFoundError, match="Bundled TextFSM template 'missing.textfsm' was not injected and was not found"):
            parse_textfsm_template(self.SAMPLE_OUTPUT, "missing.textfsm")

    def test_textfsm_helper_uses_injected_template_when_local_file_is_unavailable(self):
        expected_template = "value VLAN_ID (\\d+)\nvalue NAME (\\S+)\n\nstart\n  ^${VLAN_ID} ${NAME} -> Record"
        expected_output = self.SAMPLE_OUTPUT

        class FakeTextFSM:
            def __init__(self, template_file):
                self.template = template_file.read()
                self.header = ["VLAN_ID", "NAME"]

            def ParseText(self, output):
                assert output == expected_output
                assert self.template == expected_template
                return [["10", "dev"]]

        fake_textfsm = types.SimpleNamespace(TextFSM=FakeTextFSM)

        with pytest.MonkeyPatch.context() as mp:
            mp.setitem(sys.modules, "textfsm", fake_textfsm)
            mp.setattr("ansible_collections.c1emon.xikeos.plugins.module_utils.facts.textfsm_parser.os.path.isfile", lambda *_: False)
            result = parse_textfsm_template(
                self.SAMPLE_OUTPUT,
                "show_vlan.textfsm",
                templates={
                    "show_vlan.textfsm": expected_template,
                },
            )

        assert result == [{"vlan_id": "10", "name": "dev"}]

    def test_ttp_helper_uses_injected_template_and_missing_template_is_actionable(self):
        assert _load_ttp_template("show_vlan.ttp", templates={"show_vlan.ttp": "template contents"}) == "template contents"

        with pytest.raises(FileNotFoundError, match="Bundled TTP template 'missing.ttp' was not injected and was not found"):
            with pytest.MonkeyPatch.context() as mp:
                mp.setattr("ansible_collections.c1emon.xikeos.plugins.module_utils.facts.ttp_parser.os.path.isfile", lambda *_: False)
                _load_ttp_template("missing.ttp")

    def test_ttp_parser_accepts_injected_template_without_local_file(self):
        class FakeTTP:
            def __init__(self, data, template):
                self.data = data
                self.template = template
                self._result = [[{"vlans": [{"vlan_id": 10, "name": "dev"}]}]]

            def parse(self, one=True):
                assert one is True
                assert self.template == "template contents"

            def result(self):
                return self._result

        fake_ttp_module = types.SimpleNamespace(ttp=FakeTTP)

        with pytest.MonkeyPatch.context() as mp:
            mp.setitem(sys.modules, "ttp", fake_ttp_module)
            result = parse_ttp_template(
                "show vlan output",
                "show_vlan.ttp",
                result_key="vlans",
                templates={"show_vlan.ttp": "template contents"},
            )

        assert result == [{"vlan_id": 10, "name": "dev"}]

    def test_parse_show_vlan_multiline_real_output(self):
        output = """\
VLAN Name         Type       Media     Ports
---- ------------ ---------- --------- ----------------------------------------
1    default      Static     ENET      Ethernet1/0/1       Ethernet1/0/2(T)
                                       Ethernet1/0/3(T)    Ethernet1/0/4(T)
10   dev          Static     ENET      Ethernet1/0/3(T)    Ethernet1/0/4(T)
                                       Ethernet1/0/5(T)
21   isp          Static     ENET      Ethernet1/0/2(T)    Ethernet1/0/3(T)
"""
        result = parse_vlan(output)

        assert result == [
            {
                "vlan_id": 1,
                "name": "default",
                "type": "Static",
                "media": "ENET",
                "state": "active",
                "status": "active",
                "ports": [
                    {"name": "Ethernet1/0/1", "tagged": False},
                    {"name": "Ethernet1/0/2", "tagged": True},
                    {"name": "Ethernet1/0/3", "tagged": True},
                    {"name": "Ethernet1/0/4", "tagged": True},
                ],
            },
            {
                "vlan_id": 10,
                "name": "dev",
                "type": "Static",
                "media": "ENET",
                "state": "active",
                "status": "active",
                "ports": [
                    {"name": "Ethernet1/0/3", "tagged": True},
                    {"name": "Ethernet1/0/4", "tagged": True},
                    {"name": "Ethernet1/0/5", "tagged": True},
                ],
            },
            {
                "vlan_id": 21,
                "name": "isp",
                "type": "Static",
                "media": "ENET",
                "state": "active",
                "status": "active",
                "ports": [
                    {"name": "Ethernet1/0/2", "tagged": True},
                    {"name": "Ethernet1/0/3", "tagged": True},
                ],
            },
        ]


# ---------------------------------------------------------------------------
# Interface brief parser tests
# ---------------------------------------------------------------------------

class TestInterfaceBriefParser:
    """Tests for parse_interface_brief."""

    SAMPLE_OUTPUT = """\
Port    Desc   Link shutdn Speed         Pri PVID Mode TagVlan    UtVlan
--------------------------------------------------------------------------------
e0/0/1  test   up   enable  1000(FD)      0  1    TRK  100        -
e0/0/2  -      up   enable  auto(FD)     0  1    ACC  -          -
e0/0/3  down   down disable auto(FD)     0  1    ACC  -          -
"""

    def test_interface_brief_returns_list(self):
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        assert isinstance(result, list)

    def test_interface_brief_count(self):
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        assert len(result) == 3

    def test_interface_brief_first_port(self):
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        iface = result[0]
        assert iface["name"] == "ethernet 0/0/1"
        assert iface["description"] == "test"
        assert iface["link"] == "up"
        assert iface["shutdown"] is False
        assert iface["speed"] == "1000"
        assert iface["duplex"] == "fd"
        assert iface["mode"] == "TRK"
        assert iface["tag_vlan"] == "100"
        assert iface["untag_vlan"] is None

    def test_interface_brief_second_port(self):
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        iface = result[1]
        assert iface["name"] == "ethernet 0/0/2"
        assert iface["description"] is None
        assert iface["link"] == "up"
        assert iface["shutdown"] is False
        assert iface["speed"] == "auto"
        assert iface["duplex"] == "fd"
        assert iface["mode"] == "ACC"

    def test_interface_brief_third_port_down(self):
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        iface = result[2]
        assert iface["name"] == "ethernet 0/0/3"
        assert iface["description"] == "down"
        assert iface["link"] == "down"
        assert iface["shutdown"] is True
        assert iface["speed"] == "auto"
        assert iface["mode"] == "ACC"

    def test_interface_brief_empty_output(self):
        result = parse_interface_brief("")
        assert result == []

    def test_interface_brief_none_output(self):
        result = parse_interface_brief(None)
        assert result == []

    def test_interface_brief_port_normalization(self):
        """Verify e0/0/1 -> ethernet 0/0/1 normalization."""
        result = parse_interface_brief(self.SAMPLE_OUTPUT)
        for iface in result:
            assert iface["name"].startswith("ethernet ")


# ---------------------------------------------------------------------------
# OSPF neighbor parser tests
# ---------------------------------------------------------------------------

class TestOspfNeighborParser:
    """Tests for parse_ospf_neighbors."""

    SAMPLE_OUTPUT = """\
Neighbor ID     Pri  State           Dead Time   Address         Interface
2.2.2.2           1  FULL/BDR        00:00:35    10.0.0.2        vlan-interface 10
3.3.3.3           1  FULL/DR         00:00:30    10.0.1.2        vlan-interface 20
"""

    def test_ospf_neighbor_returns_list(self):
        result = parse_ospf_neighbors(self.SAMPLE_OUTPUT)
        assert isinstance(result, list)

    def test_ospf_neighbor_count(self):
        result = parse_ospf_neighbors(self.SAMPLE_OUTPUT)
        assert len(result) == 2

    def test_ospf_neighbor_first(self):
        result = parse_ospf_neighbors(self.SAMPLE_OUTPUT)
        n = result[0]
        assert n["neighbor_id"] == "2.2.2.2"
        assert n["priority"] == 1
        assert n["state"] == "FULL/BDR"
        assert n["dead_time"] == "00:00:35"
        assert n["address"] == "10.0.0.2"
        assert n["interface"] == "vlan-interface 10"

    def test_ospf_neighbor_second(self):
        result = parse_ospf_neighbors(self.SAMPLE_OUTPUT)
        n = result[1]
        assert n["neighbor_id"] == "3.3.3.3"
        assert n["state"] == "FULL/DR"
        assert n["interface"] == "vlan-interface 20"

    def test_ospf_neighbor_empty_output(self):
        result = parse_ospf_neighbors("")
        assert result == []

    def test_ospf_neighbor_no_separator(self):
        output = """\
Neighbor ID     Pri  State           Dead Time   Address         Interface
5.5.5.5           1  FULL/BDR        00:00:32    10.0.2.2        vlan-interface 30
"""
        result = parse_ospf_neighbors(output)
        assert len(result) == 1
        assert result[0]["neighbor_id"] == "5.5.5.5"


# ---------------------------------------------------------------------------
# STP brief parser tests
# ---------------------------------------------------------------------------

class TestStpBriefParser:
    """Tests for parse_stp_brief."""

    SAMPLE_OUTPUT = """\
STP status: ENABLED
STP mode: RSTP
Bridge ID: 0000.001a.2b3c.4d5e
Bridge Priority: 32768
Hello Time: 2 sec
Forward Delay: 15 sec
Max Age: 20 sec
Pathcost Standard: dot1d-1998
BPDU Guard: Disabled
BPDU Filter: Disabled
"""

    def test_stp_brief_returns_dict(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert isinstance(result, dict)

    def test_stp_mode(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["stp_mode"] == "rstp"

    def test_stp_priority(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["priority"] == 32768

    def test_stp_hello_time(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["hello_time"] == 2

    def test_stp_forward_delay(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["forward_time"] == 15

    def test_stp_max_age(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["max_age"] == 20

    def test_stp_pathcost_standard(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["pathcost_standard"] == "dot1d-1998"

    def test_stp_bpdu_guard_disabled(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["bpdu_guard"] is False

    def test_stp_bpdu_filter_disabled(self):
        result = parse_stp_brief(self.SAMPLE_OUTPUT)
        assert result["bpdu_filter"] is False

    def test_stp_brief_with_enabled_bpdu_guard(self):
        output = """\
STP mode: RSTP
BPDU Guard: Enabled
BPDU Filter: Enabled
"""
        result = parse_stp_brief(output)
        assert result["bpdu_guard"] is True
        assert result["bpdu_filter"] is True

    def test_stp_brief_empty_output(self):
        result = parse_stp_brief("")
        assert result == {}

    def test_parse_vlan_ranges_single(self):
        result = parse_vlan_ranges("100")
        assert result == [100]

    def test_parse_vlan_ranges_range(self):
        result = parse_vlan_ranges("1-5")
        assert result == [1, 2, 3, 4, 5]

    def test_parse_vlan_ranges_mixed(self):
        result = parse_vlan_ranges("1-3,5,7-9")
        assert result == [1, 2, 3, 5, 7, 8, 9]

    def test_parse_vlan_ranges_sorted_unique(self):
        result = parse_vlan_ranges("5,1-3,5")
        assert result == [1, 2, 3, 5]


# ---------------------------------------------------------------------------
# OSPF summary parser tests
# ---------------------------------------------------------------------------

class TestOspfSummaryParser:
    """Tests for parse_ospf_summary."""

    def test_ospf_summary_single_process(self):
        output = """\
Routing Process "ospf 1" with ID 1.1.1.1
 Supports only single TOS(TOS0) routes
 Start time: 00:00:05.123
"""
        result = parse_ospf_summary(output)
        assert 1 in result
        assert result[1]["process_id"] == 1
        assert result[1]["router_id"] == "1.1.1.1"

    def test_ospf_summary_areas(self):
        output = """\
Routing Process "ospf 1" with ID 1.1.1.1
    Area BACKBONE(0)
    Area 1
"""
        result = parse_ospf_summary(output)
        assert len(result[1]["areas"]) == 2

    def test_ospf_summary_empty(self):
        result = parse_ospf_summary("")
        assert result == {}


# ---------------------------------------------------------------------------
# OSPF facts gathering tests
# ---------------------------------------------------------------------------

class TestOspfFactsGathering:
    """Tests for Ospfv2Facts."""

    def test_ospfv2_facts_use_run_commands_instead_of_module_run_command(self):
        module = types.SimpleNamespace(run_command=Mock())
        summary_output = 'Routing Process "ospf 1" with ID 1.1.1.1\n Area BACKBONE(0)\n'
        neighbor_output = (
            'Neighbor ID     Pri  State           Dead Time   Address         Interface\n'
            '2.2.2.2           1  FULL/DR         00:00:30    10.0.1.2        vlan-interface 20\n'
        )

        run_mock = Mock(return_value=[summary_output, neighbor_output])
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "ansible_collections.c1emon.xikeos.plugins.module_utils.facts.ospfv2.run_commands",
                run_mock,
            )
            facts = Ospfv2Facts(module).facts

        run_mock.assert_called_once_with(module, ["show ip ospf", "show ip ospf neighbor"], check_rc=True)
        module.run_command.assert_not_called()
        assert facts["processes"][1]["router_id"] == "1.1.1.1"
        assert facts["processes"][1]["areas"] == [{"area_id": "0"}]
        assert facts["neighbors"][0]["neighbor_id"] == "2.2.2.2"

    def test_ospfv2_facts_surface_gather_failures(self):
        module = types.SimpleNamespace(run_command=Mock())

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "ansible_collections.c1emon.xikeos.plugins.module_utils.facts.ospfv2.run_commands",
                Mock(side_effect=RuntimeError("boom")),
            )
            with pytest.raises(RuntimeError, match="boom"):
                Ospfv2Facts(module)


# ---------------------------------------------------------------------------
# OSPF running-config parser tests
# ---------------------------------------------------------------------------

class TestOspfRunningConfigParser:
    """Tests for parse_running_config."""

    def test_parse_router_ospf(self):
        config = """\
router ospf 1
 ospf router-id 1.1.1.1
 network 10.0.0.0 0.0.255.255 area 0
"""
        result = parse_running_config(config)
        assert 1 in result
        assert result[1]["router_id"] == "1.1.1.1"
        assert len(result[1]["networks"]) == 1
        assert result[1]["networks"][0]["network"] == "10.0.0.0"
        assert result[1]["networks"][0]["wildcard"] == "0.0.255.255"
        assert result[1]["networks"][0]["area"] == "0"

    def test_parse_redistribute(self):
        config = """\
router ospf 1
 redistribute static metric 10
 redistribute connected route-map CONN
"""
        result = parse_running_config(config)
        assert len(result[1]["redistribute"]) == 2

    def test_parse_passive_interface(self):
        config = """\
router ospf 1
 passive-interface vlan-interface 10
 passive-interface default
"""
        result = parse_running_config(config)
        assert len(result[1]["passive_interfaces"]) == 2
        assert "vlan-interface 10" in result[1]["passive_interfaces"]
        assert "default" in result[1]["passive_interfaces"]

    def test_parse_default_information(self):
        config = """\
router ospf 1
 default-information originate always metric 100 metric-type 2
"""
        result = parse_running_config(config)
        assert result[1]["default_info_originate"] is True
        assert result[1]["default_info_originate_always"] is True
        assert result[1]["default_info_originate_metric"] == 100
        assert result[1]["default_info_originate_metric_type"] == 2
