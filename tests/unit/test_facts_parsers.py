"""Unit tests for Xike OS facts parsers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

# Import parsers directly (no device connection needed)
from ansible_collections.xike.xikeos.plugins.module_utils.facts.vlans import (
    VLAN_BRIEF_TEMPLATE,
    parse_vlan_brief,
    parse_vlan_line,
)
from ansible_collections.xike.xikeos.plugins.module_utils.facts.ttp_parser import (
    parse_ttp_template,
)
from ansible_collections.xike.xikeos.plugins.module_utils.facts.interfaces import (
    parse_interface_brief,
)
from ansible_collections.xike.xikeos.plugins.module_utils.facts.ospfv2 import (
    parse_ospf_neighbors,
    parse_ospf_summary,
    parse_running_config,
)
from ansible_collections.xike.xikeos.plugins.module_utils.facts.stp import (
    parse_stp_brief,
    parse_vlan_ranges,
)


# ---------------------------------------------------------------------------
# VLAN brief parser tests
# ---------------------------------------------------------------------------

class TestVlanBriefParser:
    """Tests for parse_vlan_brief."""

    SAMPLE_OUTPUT = """\
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    e0/0/1, e0/0/2, e0/0/3
100  DATA                             active    e0/0/10
200  VOICE                            active    e0/0/20
"""

    def test_parse_vlan_brief_returns_list(self):
        result = parse_vlan_brief(self.SAMPLE_OUTPUT)
        assert isinstance(result, list)

    def test_vlan_brief_parser_count(self):
        result = parse_vlan_brief(self.SAMPLE_OUTPUT)
        assert len(result) == 3

    def test_vlan_brief_parser_first_vlan(self):
        result = parse_vlan_brief(self.SAMPLE_OUTPUT)
        vlan = result[0]
        assert vlan["vlan_id"] == 1
        assert vlan["name"] == "default"
        assert vlan["state"] == "active"
        assert vlan["status"] == "active"
        assert vlan["ports"] == ["e0/0/1", "e0/0/2", "e0/0/3"]

    def test_vlan_brief_parser_second_vlan(self):
        result = parse_vlan_brief(self.SAMPLE_OUTPUT)
        vlan = result[1]
        assert vlan["vlan_id"] == 100
        assert vlan["name"] == "DATA"
        assert vlan["status"] == "active"
        assert vlan["ports"] == ["e0/0/10"]

    def test_vlan_brief_parser_third_vlan(self):
        result = parse_vlan_brief(self.SAMPLE_OUTPUT)
        vlan = result[2]
        assert vlan["vlan_id"] == 200
        assert vlan["name"] == "VOICE"
        assert vlan["ports"] == ["e0/0/20"]

    def test_vlan_brief_parser_empty_output(self):
        result = parse_vlan_brief("")
        assert result == []

    def test_vlan_brief_parser_no_ports(self):
        output = """\
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
500  EMPTY                            active
"""
        result = parse_vlan_brief(output)
        assert len(result) == 1
        assert result[0]["vlan_id"] == 500
        assert result[0]["name"] == "EMPTY"
        assert result[0]["state"] == "active"
        assert result[0]["status"] == "active"
        assert result[0]["ports"] == []

    def test_vlan_brief_parser_uses_bundled_ttp_template(self):
        rows = parse_ttp_template(self.SAMPLE_OUTPUT, VLAN_BRIEF_TEMPLATE, result_key="vlans")
        assert rows == [
            {"row": "1    default                          active    e0/0/1, e0/0/2, e0/0/3"},
            {"row": "100  DATA                             active    e0/0/10"},
            {"row": "200  VOICE                            active    e0/0/20"},
        ]

    def test_vlan_brief_parser_preserves_names_with_spaces(self):
        output = """\
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
600  Guest VLAN                       suspend
"""
        result = parse_vlan_brief(output)
        assert result == [
            {
                "vlan_id": 600,
                "name": "Guest VLAN",
                "state": "suspend",
                "status": "suspend",
                "ports": [],
            }
        ]

    def test_ttp_helper_missing_template_error_is_actionable(self):
        with pytest.raises(FileNotFoundError, match="Bundled TTP template 'missing.ttp' was not found"):
            parse_ttp_template(self.SAMPLE_OUTPUT, "missing.ttp")

    def test_parse_vlan_line_single(self):
        line = "100  DATA   active   e0/0/10"
        result = parse_vlan_line(line)
        assert result is not None
        assert result["vlan_id"] == 100
        assert result["name"] == "DATA"


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
