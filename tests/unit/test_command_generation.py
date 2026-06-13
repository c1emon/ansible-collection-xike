"""Unit tests for Xike OS command generation functions."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

# Import command generation functions directly (no device connection needed)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_vlans import (
    get_commands as vlan_get_commands,
    vlan_id_range,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_interfaces import (
    build_interface_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_l2_interfaces import (
    build_commands as l2_build_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_l3_interfaces import (
    build_commands as l3_build_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_lag_interfaces import (
    build_trunk_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_ospf_v2 import (
    build_commands as ospf_build_commands,
    build_delete_commands as ospf_build_delete_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_mirror import (
    get_commands as mirror_get_commands,
)
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_qinq import (
    get_commands as qinq_get_commands,
)


# ---------------------------------------------------------------------------
# VLAN create / delete tests
# ---------------------------------------------------------------------------

class TestVlanCommands:
    """Tests for VLAN command generation."""

    def test_vlan_create_single(self):
        config = [{"vlan_id": 100, "name": "DATA", "state": "active"}]
        cmds = vlan_get_commands(config, "merged")
        assert "vlan 100" in cmds
        assert "description DATA" in cmds
        assert "exit" in cmds

    def test_vlan_create_multiple(self):
        config = [
            {"vlan_id": 100, "name": "DATA"},
            {"vlan_id": 200, "name": "VOICE"},
        ]
        cmds = vlan_get_commands(config, "merged")
        assert cmds.count("vlan 100") == 1
        assert cmds.count("vlan 200") == 1
        assert "description DATA" in cmds
        assert "description VOICE" in cmds

    def test_vlan_create_no_name(self):
        config = [{"vlan_id": 500}]
        cmds = vlan_get_commands(config, "merged")
        assert "vlan 500" in cmds
        assert "exit" in cmds
        # No description command when name is empty
        assert not any("description" in c for c in cmds)

    def test_vlan_delete_single(self):
        config = [{"vlan_id": 100}]
        cmds = vlan_get_commands(config, "deleted")
        assert cmds == ["no vlan 100"]

    def test_vlan_delete_multiple(self):
        config = [{"vlan_id": 100}, {"vlan_id": 200}]
        cmds = vlan_get_commands(config, "deleted")
        assert "no vlan 100" in cmds
        assert "no vlan 200" in cmds

    def test_vlan_id_range_consecutive(self):
        assert vlan_id_range([1, 2, 3, 4, 5]) == "1-5"

    def test_vlan_id_range_non_consecutive(self):
        assert vlan_id_range([1, 3, 5]) == "1,3,5"

    def test_vlan_id_range_mixed(self):
        assert vlan_id_range([1, 2, 3, 10, 11, 20]) == "1-3,10-11,20"

    def test_vlan_id_range_empty(self):
        assert vlan_id_range([]) == ""


# ---------------------------------------------------------------------------
# Interface config tests
# ---------------------------------------------------------------------------

class TestInterfaceCommands:
    """Tests for interface command generation."""

    def test_interface_description(self):
        cfg = {"name": "ethernet 0/0/1", "description": "Uplink to core"}
        cmds = build_interface_commands(cfg)
        assert "interface ethernet 0/0/1" in cmds
        assert "description Uplink to core" in cmds

    def test_interface_speed(self):
        cfg = {"name": "ethernet 0/0/1", "speed": "1000"}
        cmds = build_interface_commands(cfg)
        assert "speed 1000" in cmds

    def test_interface_duplex(self):
        cfg = {"name": "ethernet 0/0/1", "duplex": "full"}
        cmds = build_interface_commands(cfg)
        assert "duplex full" in cmds

    def test_interface_shutdown(self):
        cfg = {"name": "ethernet 0/0/1", "enabled": False}
        cmds = build_interface_commands(cfg)
        assert "shutdown" in cmds

    def test_interface_no_shutdown(self):
        cfg = {"name": "ethernet 0/0/1", "enabled": True}
        cmds = build_interface_commands(cfg)
        assert "no shutdown" in cmds

    def test_interface_mtu(self):
        cfg = {"name": "ethernet 0/0/1", "mtu": 1500}
        cmds = build_interface_commands(cfg)
        assert "mtu 1500" in cmds

    def test_interface_no_description(self):
        cfg = {"name": "ethernet 0/0/1", "description": ""}
        cmds = build_interface_commands(cfg)
        assert "no description" in cmds

    def test_interface_all_options(self):
        cfg = {
            "name": "ethernet 0/0/2",
            "description": "Server link",
            "speed": "10000",
            "duplex": "full",
            "enabled": True,
            "mtu": 9000,
        }
        cmds = build_interface_commands(cfg)
        assert cmds == [
            "interface ethernet 0/0/2",
            "description Server link",
            "speed 10000",
            "duplex full",
            "mtu 9000",
            "no shutdown",
        ]


# ---------------------------------------------------------------------------
# L2 hybrid port tests
# ---------------------------------------------------------------------------

class TestL2HybridCommands:
    """Tests for L2 interface (hybrid port) command generation."""

    def test_hybrid_port_commands(self):
        config = {
            "name": "ethernet 0/0/1",
            "mode": "hybrid",
            "pvid": 100,
            "hybrid_untagged_vlan": "10,20",
            "hybrid_tagged_vlan": "30,40",
        }
        cmds = l2_build_commands(config, "merged", {})
        assert "interface ethernet 0/0/1" in cmds
        assert "switchport link-type hybrid" in cmds
        assert "switchport pvid 100" in cmds
        assert "switchport hybrid untagged vlan 10,20" in cmds
        assert "switchport hybrid tagged vlan 30,40" in cmds

    def test_access_port_commands(self):
        config = {
            "name": "ethernet 0/0/2",
            "mode": "access",
            "access_vlan": 100,
        }
        cmds = l2_build_commands(config, "merged", {})
        assert "interface ethernet 0/0/2" in cmds
        assert "switchport link-type access" in cmds
        assert "switchport pvid 100" in cmds

    def test_trunk_port_commands(self):
        config = {
            "name": "ethernet 0/0/3",
            "mode": "trunk",
            "trunk_allowed_vlan": "10,20,30",
        }
        cmds = l2_build_commands(config, "merged", {})
        assert "interface ethernet 0/0/3" in cmds
        assert "switchport link-type trunk" in cmds
        assert "switchport trunk allowed vlan 10,20,30" in cmds

    def test_no_change_returns_empty(self):
        config = {
            "name": "ethernet 0/0/1",
            "mode": "access",
            "access_vlan": 100,
        }
        existing = {
            "ethernet 0/0/1": {
                "mode": "access",
                "access_vlan": 100,
            }
        }
        cmds = l2_build_commands(config, "merged", existing)
        assert cmds == []

    def test_hybrid_untagged_only(self):
        config = {
            "name": "ethernet 0/0/1",
            "mode": "hybrid",
            "hybrid_untagged_vlan": "50",
        }
        cmds = l2_build_commands(config, "merged", {})
        assert "switchport hybrid untagged vlan 50" in cmds
        assert not any("hybrid tagged vlan" in c for c in cmds)


# ---------------------------------------------------------------------------
# L3 IP address tests
# ---------------------------------------------------------------------------

class TestL3InterfaceCommands:
    """Tests for L3 interface (IP address) command generation."""

    def test_ipv4_address_add(self):
        config = {
            "name": "vlan-interface 100",
            "ipv4": [{"address": "192.168.100.1", "subnet_mask": "255.255.255.0"}],
        }
        cmds = l3_build_commands(config, {})
        assert "interface vlan-interface 100" in cmds
        assert "ip address 192.168.100.1 255.255.255.0" in cmds

    def test_ipv4_address_replace(self):
        config = {
            "name": "vlan-interface 100",
            "ipv4": [{"address": "192.168.100.2", "subnet_mask": "255.255.255.0"}],
        }
        existing = {
            "vlan-interface 100": {
                "ipv4": [{"address": "192.168.100.1", "subnet_mask": "255.255.255.0"}],
            }
        }
        cmds = l3_build_commands(config, existing)
        assert "no ip address 192.168.100.1 255.255.255.0" in cmds
        assert "ip address 192.168.100.2 255.255.255.0" in cmds

    def test_ipv4_address_no_change(self):
        config = {
            "name": "vlan-interface 100",
            "ipv4": [{"address": "192.168.100.1", "subnet_mask": "255.255.255.0"}],
        }
        existing = {
            "vlan-interface 100": {
                "ipv4": [{"address": "192.168.100.1", "subnet_mask": "255.255.255.0"}],
            }
        }
        cmds = l3_build_commands(config, existing)
        assert cmds == []

    def test_ipv6_address_add(self):
        config = {
            "name": "vlan-interface 1",
            "ipv6": [{"address": "2001:db8::1/64"}],
        }
        cmds = l3_build_commands(config, {})
        assert "interface vlan-interface 1" in cmds
        assert "ipv6 address 2001:db8::1/64" in cmds

    def test_ipv4_and_ipv6_together(self):
        config = {
            "name": "vlan-interface 10",
            "ipv4": [{"address": "10.0.0.1", "subnet_mask": "255.255.255.0"}],
            "ipv6": [{"address": "2001:db8::1/64"}],
        }
        cmds = l3_build_commands(config, {})
        assert "ip address 10.0.0.1 255.255.255.0" in cmds
        assert "ipv6 address 2001:db8::1/64" in cmds


# ---------------------------------------------------------------------------
# LAG eth-trunk tests
# ---------------------------------------------------------------------------

class TestLagTrunkCommands:
    """Tests for eth-trunk command generation."""

    def test_static_trunk_create(self):
        config = {
            "name": "eth-trunk 1",
            "mode": "static",
            "members": ["0/0/1", "0/0/2"],
        }
        cmds = build_trunk_commands(config, {})
        assert "interface eth-trunk 1" in cmds
        assert "link-aggregation mode static" in cmds
        assert "link-aggregation members ethernet 0/0/1" in cmds
        assert "link-aggregation members ethernet 0/0/2" in cmds

    def test_dynamic_trunk_with_lacp(self):
        config = {
            "name": "eth-trunk 2",
            "mode": "dynamic",
            "lacp_mode": "active",
            "members": ["0/0/3"],
        }
        cmds = build_trunk_commands(config, {})
        assert "interface eth-trunk 2" in cmds
        assert "link-aggregation mode dynamic" in cmds
        assert "lacp mode active" in cmds
        assert "link-aggregation members ethernet 0/0/3" in cmds

    def test_trunk_add_members(self):
        config = {
            "name": "eth-trunk 1",
            "members": ["0/0/1", "0/0/2", "0/0/3"],
        }
        existing = {
            "eth-trunk 1": {
                "mode": "static",
                "members": ["0/0/1", "0/0/2"],
            }
        }
        cmds = build_trunk_commands(config, existing)
        assert "link-aggregation members ethernet 0/0/3" in cmds
        # 0/0/1 and 0/0/2 are already members
        assert not any("0/0/1" in c and "members" in c for c in cmds if "no" not in c)

    def test_trunk_remove_members(self):
        config = {
            "name": "eth-trunk 1",
            "members": ["0/0/1"],
        }
        existing = {
            "eth-trunk 1": {
                "mode": "static",
                "members": ["0/0/1", "0/0/2"],
            }
        }
        cmds = build_trunk_commands(config, existing)
        assert "no link-aggregation members ethernet 0/0/2" in cmds

    def test_trunk_no_change(self):
        config = {
            "name": "eth-trunk 1",
            "mode": "static",
            "members": ["0/0/1"],
        }
        existing = {
            "eth-trunk 1": {
                "mode": "static",
                "members": ["0/0/1"],
            }
        }
        cmds = build_trunk_commands(config, existing)
        assert cmds == []


# ---------------------------------------------------------------------------
# OSPF network command tests
# ---------------------------------------------------------------------------

class TestOspfCommands:
    """Tests for OSPF command generation."""

    def test_ospf_basic(self):
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "networks": [
                {"network": "10.0.0.0", "wildcard": "0.0.255.255", "area": "0"},
            ],
        }
        cmds = ospf_build_commands(config, {"processes": {}})
        assert "router ospf 1" in cmds
        assert "ospf router-id 1.1.1.1" in cmds
        assert "network 10.0.0.0 0.0.255.255 area 0" in cmds

    def test_ospf_multiple_networks(self):
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "networks": [
                {"network": "10.0.0.0", "wildcard": "0.0.255.255", "area": "0"},
                {"network": "192.168.1.0", "wildcard": "0.0.0.255", "area": "1"},
            ],
        }
        cmds = ospf_build_commands(config, {"processes": {}})
        assert "network 10.0.0.0 0.0.255.255 area 0" in cmds
        assert "network 192.168.1.0 0.0.0.255 area 1" in cmds

    def test_ospf_redistribute(self):
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "redistribute": [
                {"protocol": "static", "metric": 10},
                {"protocol": "connected", "route_map": "CONN"},
            ],
        }
        cmds = ospf_build_commands(config, {"processes": {}})
        assert "redistribute static metric 10" in cmds
        assert "redistribute connected route-map CONN" in cmds

    def test_ospf_default_information(self):
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "default_info_originate": True,
            "default_info_originate_always": True,
            "default_info_originate_metric": 100,
            "default_info_originate_metric_type": 2,
        }
        cmds = ospf_build_commands(config, {"processes": {}})
        assert "router ospf 1" in cmds
        assert any("default-information originate always metric 100 metric-type 2" in c for c in cmds)

    def test_ospf_passive_interfaces(self):
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "passive_interfaces": ["vlan-interface 10", "vlan-interface 20"],
        }
        cmds = ospf_build_commands(config, {"processes": {}})
        assert "passive-interface vlan-interface 10" in cmds
        assert "passive-interface vlan-interface 20" in cmds

    def test_ospf_delete_commands(self):
        existing = {
            "processes": {
                1: {
                    "process_id": 1,
                    "router_id": "1.1.1.1",
                    "networks": [
                        {"network": "10.0.0.0", "wildcard": "0.0.255.255", "area": "0"},
                    ],
                    "redistribute": [{"protocol": "static", "metric": 10}],
                    "passive_interfaces": ["vlan-interface 10"],
                    "default_info_originate": True,
                }
            }
        }
        config = {"process_id": 1}
        cmds = ospf_build_delete_commands(config, existing)
        assert "router ospf 1" in cmds
        assert "no network 10.0.0.0 0.0.255.255 area 0" in cmds
        assert "no redistribute static" in cmds
        assert "no passive-interface vlan-interface 10" in cmds
        assert "no default-information originate" in cmds
        assert "no ospf router-id" in cmds
        assert "exit" in cmds

    def test_ospf_no_changes_returns_empty(self):
        existing = {
            "processes": {
                1: {
                    "process_id": 1,
                    "router_id": "1.1.1.1",
                    "networks": [
                        {"network": "10.0.0.0", "wildcard": "0.0.255.255", "area": "0"},
                    ],
                    "redistribute": [],
                    "passive_interfaces": [],
                    "default_info_originate": False,
                }
            }
        }
        config = {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "networks": [
                {"network": "10.0.0.0", "wildcard": "0.0.255.255", "area": "0"},
            ],
        }
        cmds = ospf_build_commands(config, existing)
        assert cmds == []


# ---------------------------------------------------------------------------
# Mirror group command tests
# ---------------------------------------------------------------------------

class TestMirrorCommands:
    """Tests for mirror group command generation."""

    def test_mirror_present_with_sources_and_dest(self):
        config = {
            "group_id": 1,
            "source_interfaces": [
                {"name": "ethernet 0/0/1", "direction": "both"},
                {"name": "ethernet 0/0/2", "direction": "ingress"},
            ],
            "destination_interface": "ethernet 0/0/10",
        }
        cmds = mirror_get_commands(config, "present")
        assert "mirror group 1 source-interface ethernet 0/0/1 both" in cmds
        assert "mirror group 1 source-interface ethernet 0/0/2 ingress" in cmds
        assert "mirror group 1 destination-interface ethernet 0/0/10" in cmds

    def test_mirror_present_cpu_source(self):
        config = {
            "group_id": 1,
            "source_interfaces": [{"name": "cpu", "direction": "both"}],
            "destination_interface": "ethernet 0/0/10",
        }
        cmds = mirror_get_commands(config, "present")
        assert "mirror group 1 source-interface cpu both" in cmds

    def test_mirror_absent_specific_source(self):
        config = {
            "group_id": 1,
            "source_interfaces": [{"name": "ethernet 0/0/2"}],
        }
        cmds = mirror_get_commands(config, "absent")
        assert "no mirror group 1 source-interface ethernet 0/0/2" in cmds

    def test_mirror_absent_destination(self):
        config = {
            "group_id": 1,
            "destination_interface": "ethernet 0/0/10",
        }
        cmds = mirror_get_commands(config, "absent")
        assert "no mirror group 1 destination-interface ethernet 0/0/10" in cmds

    def test_mirror_absent_cpu_source(self):
        config = {
            "group_id": 1,
            "source_interfaces": [{"name": "cpu"}],
        }
        cmds = mirror_get_commands(config, "absent")
        assert "no mirror group 1 source-interface cpu" in cmds

    def test_mirror_no_group_id_returns_empty(self):
        config = {
            "source_interfaces": [{"name": "ethernet 0/0/1"}],
        }
        cmds = mirror_get_commands(config, "present")
        assert cmds == []


# ---------------------------------------------------------------------------
# QinQ command tests
# ---------------------------------------------------------------------------

class TestQinqCommands:
    """Tests for QinQ command generation."""

    def test_optional_rule_lists_accept_none(self):
        config = {
            "mode": "customer",
            "outer_tpid": "0x8100",
            "vlan_inserts": None,
            "vlan_pass_throughs": [
                {
                    "start_vlan": 100,
                    "end_vlan": 100,
                }
            ],
            "vlan_swaps": None,
        }

        cmds = qinq_get_commands(config, "merged")

        assert cmds == [
            "qinq mode customer",
            "qinq outer-tpid 0x8100",
            "vlan pass-through 100 100",
        ]
