# c1emon.xikeos Module Reference

Complete reference for all 17 modules in the `c1emon.xikeos` collection.

Resource-module state behavior is explicit:

- Lifecycle-complete modules (`xikeos_vlans`, `xikeos_static_routes`, `xikeos_acls`, `xikeos_interfaces`, `xikeos_l2_interfaces`, `xikeos_l3_interfaces`, `xikeos_lag_interfaces`) gather current state, compute diffs, honor check mode, apply changes through the Xike OS network configuration path, and report `before`/`after`.
- `xikeos_vlans` also supports non-mutating `state=gathered`.
- Specialty modules (`xikeos_stp`, `xikeos_erps`, `xikeos_eaps`, `xikeos_qinq`, `xikeos_mirror`, `xikeos_port_isolate`, `xikeos_flex_monitor_link`, `xikeos_ospfv2`) currently support explicit non-mutating `state=rendered`; their mutating states fail fast until facts/diff/apply support is implemented.

## Table of Contents

- [Interface Modules](#interface-modules)
  - [xikeos_interfaces](#xikeos_interfaces)
  - [xikeos_l2_interfaces](#xikeos_l2_interfaces)
  - [xikeos_l3_interfaces](#xikeos_l3_interfaces)
  - [xikeos_lag_interfaces](#xikeos_lag_interfaces)
- [VLAN Modules](#vlan-modules)
  - [xikeos_vlans](#xikeos_vlans)
- [Routing Modules](#routing-modules)
  - [xikeos_ospfv2](#xikeos_ospfv2)
  - [xikeos_static_routes](#xikeos_static_routes)
- [Security Modules](#security-modules)
  - [xikeos_acls](#xikeos_acls)
  - [xikeos_stp](#xikeos_stp)
- [Xike-Specific Modules](#xike-specific-modules)
  - [xikeos_mirror](#xikeos_mirror)
  - [xikeos_port_isolate](#xikeos_port_isolate)
  - [xikeos_erps](#xikeos_erps)
  - [xikeos_eaps](#xikeos_eaps)
  - [xikeos_qinq](#xikeos_qinq)
  - [xikeos_flex_monitor_link](#xikeos_flex_monitor_link)
- [Fallback Modules](#fallback-modules)
  - [xikeos_config](#xikeos_config)
  - [xikeos_command](#xikeos_command)

---

## Interface Modules

### xikeos_interfaces

Configure Ethernet interfaces on Xike switches.

**Purpose**: Manage physical interface properties including speed, duplex, description, MTU, and admin state.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of interface configurations |
| `config[].name` | str | - | Yes | - | Interface name (e.g., `ethernet 0/0/1`) |
| `config[].description` | str | - | No | - | Interface description string |
| `config[].speed` | str | - | No | `10`, `100`, `1000`, `10000`, `auto` | Interface speed |
| `config[].duplex` | str | - | No | `auto`, `full`, `half` | Interface duplex mode |
| `config[].enabled` | bool | `true` | No | - | Admin state (`false` = shutdown) |
| `config[].mtu` | int | - | No | - | MTU size |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Add or update interface configuration
- `replaced`: Replace entire interface configuration

**CLI Commands Generated**:
```
interface ethernet 0/0/1
description Uplink to core
speed 1000
duplex full
mtu 1500
no shutdown
```

**Example**:
```yaml
- name: Configure interface
  c1emon.xikeos.xikeos_interfaces:
    config:
      - name: ethernet 0/0/1
        description: Uplink to core
        speed: 1000
        duplex: full
        enabled: true
        mtu: 1500
    state: merged
```

---

### xikeos_l2_interfaces

Manage Layer 2 interface configurations including access, trunk, and hybrid modes.

**Purpose**: Configure VLAN-related L2 settings on Ethernet interfaces. Supports the Xike-specific **hybrid port mode**.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of interface configurations |
| `config[].name` | str | - | Yes | - | Interface name (e.g., `ethernet 0/0/1`) |
| `config[].mode` | str | - | No | `access`, `trunk`, `hybrid` | Interface link-type mode |
| `config[].access_vlan` | int | - | No | - | VLAN ID for access port |
| `config[].trunk_allowed_vlan` | str | - | No | - | VLANs allowed on trunk (e.g., `10,20,30` or `all`) |
| `config[].hybrid_untagged_vlan` | str | - | No | - | VLANs sent untagged on hybrid port |
| `config[].hybrid_tagged_vlan` | str | - | No | - | VLANs sent tagged on hybrid port |
| `config[].pvid` | int | - | No | - | Port VLAN ID (PVID) |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Add or update L2 interface configuration
- `replaced`: Replace entire L2 interface configuration

**CLI Commands Generated**:

Access mode:
```
interface ethernet 0/0/1
switchport link-type access
switchport pvid 100
```

Trunk mode:
```
interface ethernet 0/0/2
switchport link-type trunk
switchport trunk allowed vlan 10,20,30
```

Hybrid mode (Xike-specific):
```
interface ethernet 0/0/3
switchport link-type hybrid
switchport pvid 100
switchport hybrid untagged vlan 10,20
switchport hybrid tagged vlan 30,40
```

**Example**:
```yaml
# Access port
- name: Configure access port
  c1emon.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: access
        access_vlan: 100
    state: merged

# Hybrid port (Xike-specific)
- name: Configure hybrid port
  c1emon.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/3
        mode: hybrid
        pvid: 100
        hybrid_untagged_vlan: "10,20"
        hybrid_tagged_vlan: "30,40"
    state: merged
```

---

### xikeos_l3_interfaces

Manage Layer 3 VLAN interface IP addresses.

**Purpose**: Configure IPv4 and IPv6 addresses on VLAN interfaces.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of VLAN interface configurations |
| `config[].name` | str | - | Yes | - | VLAN interface name (e.g., `vlan-interface 100`) |
| `config[].ipv4` | list | - | No | - | List of IPv4 addresses |
| `config[].ipv4[].address` | str | - | Yes | - | IPv4 address (e.g., `192.168.1.1`) |
| `config[].ipv4[].subnet_mask` | str | - | Yes | - | Subnet mask (e.g., `255.255.255.0`) |
| `config[].ipv6` | list | - | No | - | List of IPv6 addresses |
| `config[].ipv6[].address` | str | - | Yes | - | IPv6 address with prefix (e.g., `2001:db8::1/64`) |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Add or update IP addresses
- `replaced`: Replace entire IP configuration

**CLI Commands Generated**:
```
interface vlan-interface 100
ip address 192.168.100.1 255.255.255.0
ipv6 address 2001:db8::1/64
```

**Example**:
```yaml
- name: Configure VLAN interface IP
  c1emon.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 100
        ipv4:
          - address: 192.168.100.1
            subnet_mask: 255.255.255.0
        ipv6:
          - address: "2001:db8::1/64"
    state: merged
```

---

### xikeos_lag_interfaces

Manage LAG (eth-trunk) interface configurations.

**Purpose**: Create and manage Link Aggregation Groups using eth-trunk bundles with static or dynamic (LACP) aggregation.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of eth-trunk configurations |
| `config[].name` | str | - | Yes | - | Eth-trunk name (e.g., `eth-trunk 1`) |
| `config[].mode` | str | - | No | `static`, `dynamic` | Link aggregation mode |
| `config[].members` | list | - | No | - | Member ethernet port IDs (e.g., `["0/0/1", "0/0/2"]`) |
| `config[].lacp_mode` | str | - | No | `active`, `passive` | LACP mode (only for dynamic) |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Add or update LAG configuration
- `replaced`: Replace entire LAG configuration

**CLI Commands Generated**:
```
interface eth-trunk 1
link-aggregation mode static
link-aggregation members ethernet 0/0/1
link-aggregation members ethernet 0/0/2
lacp mode active
```

**Example**:
```yaml
# Static LAG
- name: Create static eth-trunk
  c1emon.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 1
        mode: static
        members:
          - "0/0/1"
          - "0/0/2"
    state: merged

# Dynamic LAG with LACP
- name: Create LACP LAG
  c1emon.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 2
        mode: dynamic
        lacp_mode: active
        members:
          - "0/0/3"
          - "0/0/4"
    state: merged
```

---

## VLAN Modules

### xikeos_vlans

Manage VLANs on Xike OS switches.

**Purpose**: Create, modify, and delete VLANs on Xike switches.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of VLAN configurations |
| `config[].vlan_id` | int | - | Yes | - | VLAN ID (1-4094) |
| `config[].name` | str | `""` | No | - | VLAN name/description |
| `config[].state` | str | `active` | No | `active`, `suspend` | VLAN state |
| `state` | str | `merged` | No | `merged`, `replaced`, `deleted` | Desired state |

**States**:
- `merged`: Create or update VLANs
- `replaced`: Replace VLAN configuration
- `deleted`: Delete VLANs

**CLI Commands Generated**:
```
vlan 100
description DATA
exit
```

**Example**:
```yaml
# Create VLANs
- name: Create VLANs
  c1emon.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
        state: active
      - vlan_id: 200
        name: VOICE
        state: active
    state: merged

# Delete VLANs
- name: Remove VLANs
  c1emon.xikeos.xikeos_vlans:
    config:
      - vlan_id: 200
      - vlan_id: 300
    state: deleted
```

---

## Routing Modules

### xikeos_ospfv2

Manage OSPFv2 routing protocol on Xike switches.

**Purpose**: Configure OSPFv2 routing including networks, redistribution, passive interfaces, and default-information originate.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | No | - | OSPFv2 configuration |
| `config.process_id` | int | - | Yes | - | OSPF process ID |
| `config.router_id` | str | - | No | - | OSPF router ID (e.g., `1.1.1.1`) |
| `config.networks` | list | - | No | - | Network statements |
| `config.networks[].network` | str | - | Yes | - | Network IP address |
| `config.networks[].wildcard` | str | - | Yes | - | Wildcard mask |
| `config.networks[].area` | str | - | Yes | - | OSPF area ID |
| `config.redistribute` | list | - | No | - | Redistribution entries |
| `config.redistribute[].protocol` | str | - | Yes | `static`, `connected`, `bgp` | Protocol to redistribute |
| `config.redistribute[].metric` | int | - | No | - | Metric for redistributed routes |
| `config.redistribute[].route_map` | str | - | No | - | Route-map name |
| `config.default_info_originate` | bool | `false` | No | - | Enable default-information originate |
| `config.default_info_originate_always` | bool | `false` | No | - | Always advertise default route |
| `config.default_info_originate_metric` | int | - | No | - | Metric for default route |
| `config.default_info_originate_metric_type` | int | - | No | `1`, `2` | Metric type (1=E1, 2=E2) |
| `config.passive_interfaces` | list | - | No | - | Interfaces to make passive |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Add or update OSPF configuration
- `replaced`: Replace entire OSPF configuration

**CLI Commands Generated**:
```
router ospf 1
ospf router-id 1.1.1.1
network 10.0.0.0 0.0.255.255 area 0
network 192.168.1.0 0.0.0.255 area 1
redistribute static metric 10
default-information originate always metric 100 metric-type 2
passive-interface vlan-interface 10
```

**Example**:
```yaml
- name: Configure OSPF
  c1emon.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - network: 10.0.0.0
          wildcard: 0.0.255.255
          area: "0"
        - network: 192.168.1.0
          wildcard: 0.0.0.255
          area: "1"
      redistribute:
        - protocol: static
          metric: 10
      default_info_originate: true
      default_info_originate_always: true
      passive_interfaces:
        - vlan-interface 10
    state: merged
```

---

### xikeos_static_routes

Manage static routes on Xike OS devices.

**Purpose**: Configure IPv4 and IPv6 static routes.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of static route configurations |
| `config[].destination` | str | - | Yes | - | Network destination address |
| `config[].mask` | str | - | Yes | - | Subnet mask or prefix length |
| `config[].next_hop` | str | - | Yes | - | Next hop IP address |
| `config[].distance` | int | `1` | No | - | Administrative distance (1-255) |
| `config[].route_type` | str | `ipv4` | No | `ipv4`, `ipv6` | Type of static route |
| `state` | str | `merged` | No | `merged`, `replaced`, `deleted` | Desired state |

**States**:
- `merged`: Add or update static routes
- `replaced`: Replace all static routes
- `deleted`: Delete static routes

**CLI Commands Generated**:
```
ip route 192.168.100.0 255.255.255.0 10.0.0.2
ip route 0.0.0.0 0.0.0.0 10.0.0.1
ipv6 route 2001:db8::/32 2001:db8::1
```

**Example**:
```yaml
# IPv4 static route
- name: Configure static route
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 192.168.100.0
        mask: 255.255.255.0
        next_hop: 10.0.0.2
        distance: 1
        route_type: ipv4
    state: merged

# IPv6 static route
- name: Configure IPv6 route
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: "2001:db8::"
        mask: "48"
        next_hop: "2001:db8::1"
        route_type: ipv6
    state: merged
```

---

## Security Modules

### xikeos_acls

Manage Access Control Lists on Xike OS devices.

**Purpose**: Configure Standard, MAC, and Mixed/Extended ACLs with Xike-specific numbering.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | list | - | No | - | List of ACL configurations |
| `config[].acl_id` | int | - | Yes | - | ACL identifier number |
| `config[].acl_type` | str | - | Yes | `standard`, `mac`, `mixed` | Type of ACL |
| `config[].remark` | str | `""` | No | - | ACL description |
| `config[].rules` | list | - | No | - | List of ACL rules |
| `config[].rules[].sequence` | int | - | No | - | Sequence number (1-65535) |
| `config[].rules[].action` | str | - | Yes | `permit`, `deny` | Action to take |
| `config[].rules[].protocol` | str | `ip` | No | - | Protocol to match |
| `config[].rules[].source` | str | - | Yes | - | Source address |
| `config[].rules[].destination` | str | `any` | No | - | Destination address |
| `state` | str | `merged` | No | `merged`, `replaced`, `deleted` | Desired state |

**ACL Number Ranges**:
- Standard ACL: 1-999
- MAC ACL: 1000-1999
- Mixed/Extended ACL: 2000-2999

**States**:
- `merged`: Create or update ACLs
- `replaced`: Replace ACL configuration
- `deleted`: Delete ACLs

**CLI Commands Generated**:

Standard ACL:
```
access-list 100 permit 192.168.0.0 0.0.255.255
access-list 100 deny any
```

MAC ACL:
```
access-list 1001 permit 0011.2233.4455 0000.0000.0000
```

Mixed/Extended ACL:
```
access-list 2001 permit tcp 192.168.1.0 0.0.0.255 any
access-list 2001 deny tcp any any
```

**Example**:
```yaml
# Standard ACL
- name: Create standard IP ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
        remark: Permit internal networks
        rules:
          - sequence: 10
            action: permit
            source: 192.168.0.0 0.0.255.255
          - sequence: 20
            action: deny
            source: any
    state: merged

# Mixed/Extended ACL
- name: Create mixed ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 2001
        acl_type: mixed
        remark: Web traffic filter
        rules:
          - sequence: 10
            action: permit
            protocol: tcp
            source: 192.168.1.0 0.0.0.255
            destination: any
    state: merged
```

---

### xikeos_stp

Manage Spanning Tree Protocol settings on Xike OS devices.

**Purpose**: Configure STP modes (STP, RSTP, MSTP, PVST), bridge priority, timers, and MSTP/PVST instances.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | No | - | STP configuration |
| `config.stp_mode` | str | - | No | `stp`, `rstp`, `mstp`, `pvst`, `rapid-pvst` | STP protocol mode |
| `config.priority` | int | - | No | - | Bridge priority (0-61440, step 4096) |
| `config.hello_time` | int | - | No | - | Hello BPDU interval (1-10 sec) |
| `config.forward_time` | int | - | No | - | Forward delay (4-30 sec) |
| `config.max_age` | int | - | No | - | Max BPDU age (6-40 sec) |
| `config.pathcost_standard` | str | - | No | `dot1d-1998`, `dot1t` | Path cost standard |
| `config.bpdu_guard` | bool | - | No | - | Enable BPDU guard globally |
| `config.bpdu_filter` | bool | - | No | - | Enable BPDU filter globally |
| `config.mstp` | dict | - | No | - | MSTP-specific configuration |
| `config.mstp.region_name` | str | - | No | - | MSTP region name |
| `config.mstp.revision` | int | - | No | - | MSTP revision level (0-65535) |
| `config.mstp.instances` | list | - | No | - | MSTP instance configurations |
| `config.pvst` | dict | - | No | - | PVST-specific configuration |
| `config.pvst.instances` | list | - | No | - | PVST instance configurations |
| `state` | str | `merged` | No | `merged`, `replaced` | Desired state |

**States**:
- `merged`: Create or update STP settings
- `replaced`: Replace entire STP configuration

**CLI Commands Generated**:
```
stp
stp mode mstp
stp priority 4096
stp hello-time 2
stp forward-time 15
mstp region-name MY_REGION
mstp revision-level 1
mstp instance 1 priority 8192
mstp instance 1 vlan 10-20
```

**Example**:
```yaml
# Configure MSTP
- name: Set STP mode to MSTP
  c1emon.xikeos.xikeos_stp:
    config:
      stp_mode: mstp
      priority: 4096
      hello_time: 2
      forward_time: 15
      mstp:
        region_name: MY_REGION
        revision: 1
        instances:
          - instance_id: 1
            priority: 8192
            vlans: [10, 20, 30]
    state: merged
```

---

## Xike-Specific Modules

### xikeos_mirror

Manage port mirroring on Xike OS switches.

**Purpose**: Configure mirror groups with source interfaces and destination interfaces for traffic monitoring.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | Yes (when present) | - | Mirror group configuration |
| `config.group_id` | int | - | Yes | - | Mirror group ID |
| `config.source_interfaces` | list | - | No | - | Source interfaces to mirror |
| `config.source_interfaces[].name` | str | - | Yes | - | Interface name (e.g., `ethernet 0/0/1` or `cpu`) |
| `config.source_interfaces[].direction` | str | `both` | No | `ingress`, `egress`, `both` | Traffic direction |
| `config.destination_interface` | str | - | No | - | Destination interface |
| `state` | str | `present` | No | `present`, `absent` | Desired state |

**States**:
- `present`: Create or update mirror group
- `absent`: Remove mirror group or source interfaces

**CLI Commands Generated**:
```
mirror group 1 source-interface ethernet 0/0/1 both
mirror group 1 source-interface ethernet 0/0/2 ingress
mirror group 1 destination-interface ethernet 0/0/10
```

**Example**:
```yaml
# Create mirror group
- name: Create mirror group
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: ethernet 0/0/1
          direction: both
        - name: ethernet 0/0/2
          direction: ingress
      destination_interface: ethernet 0/0/10
    state: present

# Add CPU source
- name: Add CPU mirror source
  c1emon.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: cpu
          direction: both
    state: present
```

---

### xikeos_port_isolate

Manage port isolation groups on Xike OS switches.

**Purpose**: Configure port isolation groups to prevent inter-port communication within a group while allowing communication with ports outside the group.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | Yes (when present) | - | Port isolation group configuration |
| `config.group_id` | int | - | Yes | - | Port isolation group ID |
| `config.members` | list | - | No | - | Member interfaces |
| `state` | str | `present` | No | `present`, `absent` | Desired state |

**States**:
- `present`: Create or update port isolation group
- `absent`: Remove port isolation group or members

**CLI Commands Generated**:
```
interface port-isolate group 1
switchport ethernet 0/0/1
switchport ethernet 0/0/2
switchport ethernet 0/0/3
exit
```

**Example**:
```yaml
# Create isolation group
- name: Create port isolation group
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/1
        - ethernet 0/0/2
        - ethernet 0/0/3
    state: present

# Add all ports
- name: Add all ports to isolation
  c1emon.xikeos.xikeos_port_isolate:
    config:
      group_id: 2
      members:
        - all
    state: present
```

---

### xikeos_erps

Manage ERPS (G.8032) ring protection on Xike OS devices.

**Purpose**: Configure Ethernet Ring Protection Switching (ERPS) instances for carrier-grade Ethernet ring topologies.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `instance_id` | int | - | Yes | - | ERPS instance identifier |
| `control_vlan` | int | - | No | - | Control VLAN ID |
| `port0` | str | - | No | - | Port0 configuration (e.g., `ethernet 1 owner`) |
| `port1` | str | - | No | - | Port1 configuration (e.g., `ethernet 2 neighbour`) |
| `work_mode` | str | - | No | `non-revertive`, `revertive` | ERPS work mode |
| `protected_instances` | str | - | No | - | MSTP instances protected (e.g., `1,2,5-10`) |
| `ring_enable` | bool | `true` | No | - | Enable/disable the ERPS ring |
| `guard_timer` | int | - | No | - | Guard timer (0-3000 centiseconds) |
| `mel` | int | - | No | - | Management Entity Level (0-7) |
| `wtr_timer` | int | - | No | - | Wait-to-Restore timer (1-120 minutes) |
| `state` | str | `present` | No | `present`, `absent` | Desired state |

**States**:
- `present`: Create or update ERPS instance
- `absent`: Remove ERPS instance

**CLI Commands Generated**:
```
erps
erps instance 1
control-vlan 100
port0 ethernet 1 owner
port1 ethernet 2 neighbour
work-mode revertive
protected-instance 1,2,3
guard-timer 500
wtr-timer 5
mel 5
ring enable
```

**Example**:
```yaml
# Configure ERPS instance
- name: Configure ERPS
  c1emon.xikeos.xikeos_erps:
    instance_id: 1
    control_vlan: 100
    port0: "ethernet 1 owner"
    port1: "ethernet 2 neighbour"
    work_mode: revertive
    protected_instances: "1,2,3"
    ring_enable: true
    guard_timer: 500
    wtr_timer: 5
    mel: 5
    state: present
```

---

### xikeos_eaps

Manage EAPS (Ethernet Automatic Protection Switching) on Xike OS devices.

**Purpose**: Configure EAPS domains for Ethernet ring protection with support for multiple work modes.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `domain_id` | int | - | Yes | - | EAPS domain identifier |
| `control_vlan` | int | - | No | - | Control VLAN ID |
| `rings` | list | - | No | - | Ring configurations |
| `rings[].ring_id` | int | - | Yes | - | Ring identifier |
| `rings[].role` | str | - | No | `master`, `transit` | Node role in the ring |
| `rings[].enabled` | bool | `true` | No | - | Enable/disable this ring |
| `work_mode` | str | - | No | `eips-subring`, `rrpp`, `standard` | EAPS work mode |
| `state` | str | `present` | No | `present`, `absent` | Desired state |

**States**:
- `present`: Create or update EAPS domain
- `absent`: Remove EAPS domain

**CLI Commands Generated**:
```
eaps
eaps domain 1
control-vlan 100
work-mode standard
ring 1 enable
ring 1 role master
ring 2 enable
ring 2 role transit
```

**Example**:
```yaml
# Configure EAPS domain
- name: Configure EAPS
  c1emon.xikeos.xikeos_eaps:
    domain_id: 1
    control_vlan: 100
    work_mode: standard
    rings:
      - ring_id: 1
        role: master
        enabled: true
      - ring_id: 2
        role: transit
        enabled: true
    state: present
```

---

### xikeos_qinq

Manage QinQ (VLAN stacking) configuration on Xike OS devices.

**Purpose**: Configure 802.1ad QinQ VLAN stacking with support for VLAN insert, pass-through, and swap rules.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | No | - | QinQ configuration |
| `config.mode` | str | - | No | `customer`, `uplink` | QinQ mode |
| `config.inner_tpid` | str | - | No | - | Inner TPID value (e.g., `0x8100`) |
| `config.outer_tpid` | str | - | No | - | Outer TPID value (e.g., `0x88a8`) |
| `config.vlan_inserts` | list | - | No | - | VLAN insert rules |
| `config.vlan_inserts[].start_vlan` | int | - | Yes | - | Start VLAN ID |
| `config.vlan_inserts[].end_vlan` | int | - | Yes | - | End VLAN ID |
| `config.vlan_inserts[].service_vlan` | int | - | Yes | - | Service (outer) VLAN ID |
| `config.vlan_inserts[].priority` | int | - | No | - | Priority value |
| `config.vlan_pass_throughs` | list | - | No | - | VLAN pass-through rules |
| `config.vlan_swaps` | list | - | No | - | VLAN swap rules |
| `state` | str | `merged` | No | `merged`, `replaced`, `deleted` | Desired state |

**States**:
- `merged`: Create or update QinQ settings
- `replaced`: Replace entire QinQ configuration
- `deleted`: Remove QinQ configuration

**CLI Commands Generated**:
```
qinq mode customer
qinq inner-tpid 0x8100
qinq outer-tpid 0x88a8
vlan insert 100 200 500
vlan pass-through 10 20
vlan swap 100 199 900 priority 3
```

**Example**:
```yaml
# Configure QinQ
- name: Set QinQ mode
  c1emon.xikeos.xikeos_qinq:
    config:
      mode: customer
      inner_tpid: "0x8100"
      outer_tpid: "0x88a8"
      vlan_inserts:
        - start_vlan: 100
          end_vlan: 200
          service_vlan: 500
    state: merged
```

---

### xikeos_flex_monitor_link

Manage Flex-Link and Monitor-Link configurations on Xike OS devices.

**Purpose**: Configure Flex-Link for backup link redundancy without STP, and Monitor-Link for uplink monitoring with downlink failover.

**Parameters**:

| Parameter | Type | Default | Required | Choices | Description |
|-----------|------|---------|----------|---------|-------------|
| `config` | dict | - | No | - | Configuration to apply |
| `config.flex_links` | list | - | No | - | Flex-Link group configurations |
| `config.flex_links[].group_id` | int | - | Yes | - | Flex-Link group ID |
| `config.flex_links[].master_port` | dict | - | No | - | Master port specification |
| `config.flex_links[].master_port.type` | str | - | Yes | `eth`, `eth-trunk` | Port type |
| `config.flex_links[].master_port.id` | str | - | Yes | - | Port or trunk ID |
| `config.flex_links[].slave_port` | dict | - | No | - | Slave (backup) port specification |
| `config.flex_links[].preemption_mode` | str | - | No | `role`, `bandwidth` | Preemption mode |
| `config.monitor_links` | list | - | No | - | Monitor-Link group configurations |
| `config.monitor_links[].group_id` | int | - | Yes | - | Monitor-Link group ID |
| `config.monitor_links[].uplink_port` | dict | - | No | - | Uplink port specification |
| `config.monitor_links[].downlink_ports` | list | - | No | - | Downlink port specifications |
| `state` | str | `merged` | No | `merged`, `replaced`, `deleted` | Desired state |

**States**:
- `merged`: Create or update Flex-Link/Monitor-Link settings
- `replaced`: Replace existing configuration
- `deleted`: Delete Flex-Link/Monitor-Link configuration

**CLI Commands Generated**:
```
flex-link group 1
master-port eth 0/0/1
slave-port eth 0/0/2
preemption mode role
exit

monitor-link group 1
uplink-port eth 0/0/1
downlink-port eth 0/0/2
downlink-port eth 0/0/3
exit
```

**Example**:
```yaml
# Configure Flex-Link
- name: Configure Flex-Link group
  c1emon.xikeos.xikeos_flex_monitor_link:
    config:
      flex_links:
        - group_id: 1
          master_port:
            type: eth
            id: "0/0/1"
          slave_port:
            type: eth
            id: "0/0/2"
          preemption_mode: role
    state: merged

# Configure Monitor-Link
- name: Configure Monitor-Link
  c1emon.xikeos.xikeos_flex_monitor_link:
    config:
      monitor_links:
        - group_id: 1
          uplink_port:
            type: eth
            id: "0/0/1"
          downlink_ports:
            - type: eth
              id: "0/0/2"
            - type: eth
              id: "0/0/3"
    state: merged
```

---

## Fallback Modules

### xikeos_config

Push raw configuration lines to Xike switches.

**Purpose**: Execute arbitrary configuration commands when resource modules are not available or for one-off configurations.

**Parameters**:

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `lines` | list | - | No | List of configuration commands |
| `save` | bool | `false` | No | Save running-config to startup-config |
| `diff` | bool | `true` | No | Show diff before applying |
| `backup` | bool | `false` | No | Backup current config before changes |

**States**: None (imperative module)

**CLI Commands Generated**:
```
vlan 100
description DATA
interface ethernet 0/0/1
switchport pvid 100
write memory
```

**Example**:
```yaml
- name: Push raw config
  c1emon.xikeos.xikeos_config:
    lines:
      - vlan 100
      - name DATA
      - interface ethernet 0/0/1
      - switchport pvid 100
    save: true
```

---

### xikeos_command

Execute read-only show commands on Xike switches.

**Purpose**: Run show commands and return output for inspection or further processing.

**Parameters**:

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `commands` | list | - | Yes | List of commands to execute |

**States**: None (read-only module)

**Example**:
```yaml
- name: Show version
  c1emon.xikeos.xikeos_command:
    commands:
      - show version
      - show vlan
  register: result

- debug:
    var: result.stdout
```

---

## Summary Table

| Module | Category | States | Description |
|--------|----------|--------|-------------|
| `xikeos_interfaces` | Interface | merged, replaced | Ethernet interface properties |
| `xikeos_l2_interfaces` | Interface | merged, replaced | L2 config (access/trunk/hybrid) |
| `xikeos_l3_interfaces` | Interface | merged, replaced | VLAN interface IPs |
| `xikeos_lag_interfaces` | Interface | merged, replaced | LAG eth-trunk bundles |
| `xikeos_vlans` | VLAN | merged, replaced, deleted | VLAN management |
| `xikeos_ospfv2` | Routing | merged, replaced | OSPFv2 protocol |
| `xikeos_static_routes` | Routing | merged, replaced, deleted | Static routes |
| `xikeos_acls` | Security | merged, replaced, deleted | Access Control Lists |
| `xikeos_stp` | Security | merged, replaced | Spanning Tree Protocol |
| `xikeos_mirror` | Xike-specific | present, absent | Port mirroring |
| `xikeos_port_isolate` | Xike-specific | present, absent | Port isolation groups |
| `xikeos_erps` | Xike-specific | present, absent | ERPS G.8032 ring protection |
| `xikeos_eaps` | Xike-specific | present, absent | EAPS ring protection |
| `xikeos_qinq` | Xike-specific | merged, replaced, deleted | QinQ VLAN stacking |
| `xikeos_flex_monitor_link` | Xike-specific | merged, replaced, deleted | Flex-Link/Monitor-Link |
| `xikeos_config` | Fallback | - | Raw config push |
| `xikeos_command` | Fallback | - | Read-only commands |
