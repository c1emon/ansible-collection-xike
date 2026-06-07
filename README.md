# xike.xikeos Ansible Collection

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/andy/xike-xikeos)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Ansible](https://img.shields.io/badge/Ansible-%3E%3D2.15-red.svg)](https://www.ansible.com/)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg)](https://www.python.org/)

Ansible Collection for managing **Xike (兮克) switches** with Cisco IOS-like CLI.

## Overview

The `xike.xikeos` collection provides Ansible modules for automating **Xike (兮克) Ethernet switches**. Xike switches use a Cisco IOS-like command-line interface, making this collection familiar to anyone with IOS experience while supporting Xike-specific features.

### Who is this for?

- **Network engineers** managing Xike switch infrastructure who want consistent, repeatable automation
- **DevOps/Platform teams** building CI/CD pipelines for network configuration
- **Anyone** migrating from or coexisting with Cisco IOS environments

### Key Features

- **17 module files** covering L2, L3, routing, security, and Xike-specific features
- **Hybrid port mode** — a Xike-specific feature for flexible VLAN tagging
- **ERPS/EAPS** ring protection for carrier-grade Ethernet
- **QinQ tunneling** for service provider deployments
- **Reference execution path** for `xikeos_command`, `xikeos_config`, and `xikeos_vlans` through `network_cli`/cliconf
- **Reference idempotent VLAN module** with current-state gathering, check mode, and `before`/`after` results
- Other resource modules currently provide command-generation/planned-command behavior and are candidates for follow-up execution-path refactors.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Playbook                            │
│   tasks:                                                        │
│     - xike.xikeos.xikeos_vlans:                                  │
│         config: ...                                             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   xike.xikeos Modules                           │
│                                                                 │
│  xikeos_vlans          xikeos_stp           xikeos_erps         │
│  xikeos_interfaces     xikeos_mirror        xikeos_eaps         │
│  xikeos_l2_interfaces  xikeos_port_isolate  xikeos_qinq         │
│  xikeos_l3_interfaces  xikeos_acls          xikeos_flex_monitor │
│  xikeos_lag_interfaces xikeos_static_routes xikeos_config       │
│  xikeos_ospfv2         xikeos_command                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Module Utils (rm_templates / facts)                │
│  facts/vlans.py    facts/ospfv2.py    facts/eaps.py             │
│  facts/interfaces.py  facts/stp.py    facts/erps.py             │
│  facts/l2_interfaces.py  ...         facts/qinq.py              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│        ansible.netcommon.network_cli + terminal/cliconf          │
│        ansible_network_os: xike.xikeos.xikeos                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Xike Switch                               │
│                  (IOS-like CLI via SSH)                         │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **Ansible** | >= 2.15 | Core automation engine |
| **ansible.netcommon** | >= 5.0 | Standard `network_cli`, terminal, and cliconf plugins |
| **ttp** | >= 0.9.5 | Runtime parser for bundled facts templates |
| **TextFSM** | >= 1.1.3 | Runtime parser for complex table facts templates |
| **Netmiko** | optional | Reference only for Raisecom-like CLI behavior |
| **Python** | >= 3.10 | Runtime dependency |

### Dependencies

```bash
# Install Python dependencies
ansible-galaxy collection install ansible.netcommon
pip install "ttp>=0.9.5" "textfsm>=1.1.3"
```

Ansible collection installation does not automatically install Python package
dependencies. Install `ttp` and `textfsm` in the Python environment used by the
Ansible control node before gathering VLAN facts or using `xikeos_vlans`
current-state diffing.

VLAN gathering loads the bundled `show_vlan.textfsm` template on the control
node through the `xikeos_vlans` action plugin and passes the template to the
module as an internal argument. The module can still use local template files
for direct development tests, but live AnsiballZ execution does not require
template data files inside the module payload. If a required parser template is
neither injected nor available locally, the parser fails explicitly with the
missing template name and expected path.

## Installation

### From Ansible Galaxy (once published)

```bash
ansible-galaxy collection install xike.xikeos
```

### From Source

```bash
git clone https://github.com/andy/xike-xikeos.git
cd xike-xikeos
ansible-galaxy collection build
ansible-galaxy collection install xike-xikeos-0.1.0.tar.gz
```

### From Local Development Directory

```bash
# Install directly from local clone
ansible-galaxy collection install /path/to/xike-xikeos/

# Or symlink for development
ln -s /path/to/xike-xikeos ~/.ansible/collections/ansible_collections/xike/xikeos
```

### Development Setup

```bash
git clone https://github.com/andy/xike-xikeos.git
cd xike-xikeos

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install project and development dependencies
uv sync --group dev

# Run tests
uv run pytest -q tests/unit
```

## Quick Start

### 1. Create an Inventory

```yaml
# inventory.yml
all:
  children:
    xike_switches:
      hosts:
        core-sw01:
          ansible_host: 192.168.1.100
          ansible_user: admin
          ansible_password: "{{ vault_switch_password }}"
          ansible_network_os: xike.xikeos.xikeos
          ansible_connection: ansible.netcommon.network_cli
```

### 2. Create VLANs

```yaml
# create_vlans.yml
---
- name: Configure Xike Switch VLANs
  hosts: xike_switches
  gather_facts: no
  tasks:
    - name: Create VLANs
      xike.xikeos.xikeos_vlans:
        config:
          - vlan_id: 100
            name: DATA
            state: active
          - vlan_id: 200
            name: VOICE
            state: active
        state: merged
```

### 3. Run It

```bash
ansible-playbook -i inventory.yml create_vlans.yml
```

## Inventory Setup

```yaml
# inventory.yml — Full example with all required variables
all:
  children:
    xike_switches:
      hosts:
        core-sw01:
          ansible_host: 192.168.1.100        # Management IP
          ansible_port: 22                     # SSH port (default: 22)
          ansible_user: admin                  # Login username
          ansible_password: secret             # Login password (use vault!)
          ansible_network_os: xike.xikeos.xikeos  # Collection platform FQCN
          ansible_connection: ansible.netcommon.network_cli
          ansible_become: yes                  # Enable privilege escalation
          ansible_become_method: enable        # Enable mode method
          ansible_become_password: secret      # Enable password

        access-sw01:
          ansible_host: 192.168.1.101
          ansible_user: admin
          ansible_password: "{{ vault_access_sw_password }}"
          ansible_network_os: xike.xikeos.xikeos
          ansible_connection: ansible.netcommon.network_cli

    # Group variables (apply to all switches in group)
    xike_switches:
      vars:
        ansible_network_os: xike.xikeos.xikeos
        ansible_connection: ansible.netcommon.network_cli
        ansible_user: admin
        ansible_become: yes
        ansible_become_method: enable
```

## Manual Coverage (三层配置手册对照清单)

> 本 Collection 基于兮克三层配置手册（97 章）开发。以下清单标注每章的实现状态。

### ✅ 模块覆盖（19 章）

> 状态说明：`xikeos_command`、`xikeos_config`、`xikeos_vlans` 已接入 `network_cli`/cliconf 执行路径；其余资源模块目前主要生成/报告计划命令，尚未全部完成真机执行路径重构。

| 手册章节 | 功能 | 对应模块 | 备注 |
|---------|------|---------|------|
| 1. 端口配置 | interface, speed, duplex, shutdown, description | `xikeos_interfaces` | ✅ |
| 2. 端口统计 | show statistics, show utilization | `xikeos_command` | ⚠️ 用 show 命令 |
| 5. 802.1Q VLAN | vlan, switchport, pvid, trunk, hybrid | `xikeos_vlans` + `xikeos_l2_interfaces` | ✅ 含 hybrid |
| 19. ACL | access-list 1-2999, access-group | `xikeos_acls` | ✅ 含 MAC ACL |
| 40. 链路聚合 | eth-trunk, link-aggregation, lacp | `xikeos_lag_interfaces` | ✅ |
| 41. Flex-link | flex-link group, master/slave port | `xikeos_flex_monitor_link` | ✅ |
| 42. Monitor-link | monitor-link group, uplink/downlink | `xikeos_flex_monitor_link` | ✅ |
| 43. STP/RSTP | stp mode, priority, bpdu-guard | `xikeos_stp` | ✅ |
| 44. MSTP | mstp region, instance, vlan mapping | `xikeos_stp` | ✅ |
| 45. PVST | pvst instance, vlan | `xikeos_stp` | ✅ |
| 47. EAPS | eaps domain, ring, work-mode | `xikeos_eaps` | ✅ |
| 48. ERPS | erps instance, control-vlan, port0/port1 | `xikeos_erps` | ✅ |
| 80. 管理接口 | internal-interface | `xikeos_l3_interfaces` | ⚠️ 部分 |
| 81. VLAN 接口 | interface vlan-interface, ip address | `xikeos_l3_interfaces` | ✅ |
| 82. Supervlan | supervlan-interface | `xikeos_l3_interfaces` | ⚠️ 部分 |
| 83. Loopback | loopback-interface | `xikeos_l3_interfaces` | ⚠️ 部分 |
| 86. 静态路由 | ip route, ipv6 route | `xikeos_static_routes` | ✅ |
| 88. OSPF | router ospf, network, redistribute | `xikeos_ospfv2` | ✅ |
| 端口镜像 | mirror group, source/destination | `xikeos_mirror` | ✅ |
| 端口隔离 | port-isolate group | `xikeos_port_isolate` | ✅ |
| QinQ | qinq mode, vlan insert/swap | `xikeos_qinq` | ✅ |
| MAC 地址表 | mac-address-table | `xikeos_config` 兜底 | ⚠️ 用原始命令 |

### ❌ 未实现（~28 章）

| 手册章节 | 功能 | 复杂度 | 说明 |
|---------|------|--------|------|
| 3. MTU 配置 | mtu | 低 | 可在 `xikeos_interfaces` 中扩展 |
| 4. Loopback 检测 | loopback internal/external | 低 | 环回测试 |
| 6. Mac-vlan | mac-vlan mac-address | 低 | 基于 MAC 的 VLAN |
| 7. Ip-subnet-vlan | ip-subnet-vlan | 低 | 基于子网的 VLAN |
| 8. Protocol-vlan | protocol-vlan profile | 中 | 基于协议的 VLAN |
| 9. Vlan-trunking | vlan-trunking mode | 低 | VLAN 自动透传 |
| 10. Vlan-swap | vlan swap | 低 | VLAN 转换 |
| 13. 流量控制 | flow-control | 低 | |
| 14. 带宽控制 | bandwidth ingress | 低 | |
| 15. Dlf-Control | unknown-discard | 低 | |
| 16. Local-Switch | local-switch | 低 | |
| 18. Sflow | sflow agent/collector | 中 | |
| 20. QACL | traffic insert-vlan/mirror/priority | 高 | 流分类动作 |
| 21. 队列调度 | queue-scheduler | 高 | QoS |
| 22. 双速三色 | two-rate-policer | 高 | 限速 |
| 24. 风暴抑制 | storm-control | 低 | |
| 25. 端口安全 | port-security | 中 | |
| 26. IP Source Guard | ip-source-guard | 中 | |
| 27. ARP 防欺骗 | arp anti-spoofing | 中 | |
| 28. DHCP 防攻击 | dhcp anti-attack | 中 | |
| 35. PPPoE Plus | pppoeplus | 高 | |
| 36-38. AAA | RADIUS/TACACS+/802.1X | 高 | |
| 49-53. DHCP | Snooping/Server/Client/Relay/v6 | 高 | |
| 55-57. 组播 | IGMP/MLD snooping, multicast | 高 | |
| 65. SNMP | snmp-server | 中 | |
| 72. 日志 | logging | 低 | |
| 87. RIP | router rip | 低 | |
| 89. VRRP | vrrp vrid | 中 | |
| 90. 策略路由 | route-map, prefix-list | 中 | |
| 95-97. PIM/CFM | 组播路由/OAM | 高 | |

### 📊 模块覆盖率统计

```
手册总章节数:    97
模块覆盖:        22 章（含兜底模块覆盖的 2 章）
未实现:          ~28 章
用 xikeos_config 兜底: ~10 章（可用原始命令配置）
覆盖率（专用模块）: ~23%
覆盖率（含兜底）:   ~33%
```

**核心网络功能（VLAN/接口/路由/STP/安全）已有模块或命令模板覆盖**；其中 VLAN 是当前参考幂等执行模块，其他资源模块仍需后续接入统一执行路径。缺失的主要是辅助功能（DHCP/组播/AAA/QoS/监控）。

## Usage Examples

### VLAN Management

```yaml
# Create VLANs
- name: Create VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
        state: active
      - vlan_id: 200
        name: VOICE
        state: active
    state: merged

# Replace all VLAN configuration
- name: Replace VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: SALES
    state: replaced

# Delete VLANs
- name: Remove VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 200
      - vlan_id: 300
    state: deleted
```

### Interface Configuration

> 当前 `xikeos_interfaces` 示例展示参数和计划命令生成；该模块尚未接入统一 cliconf 执行路径。

```yaml
# Configure interface properties
- name: Set interface parameters
  xike.xikeos.xikeos_interfaces:
    config:
      - name: ethernet 0/0/1
        description: Uplink to core
        speed: 1000
        duplex: full
        enabled: true
        mtu: 1500
    state: merged

# Shutdown an interface
- name: Disable interface
  xike.xikeos.xikeos_interfaces:
    config:
      - name: ethernet 0/0/24
        enabled: false
    state: merged
```

### Layer 2 Interfaces (Access / Trunk / Hybrid)

> 当前 `xikeos_l2_interfaces` 示例展示参数和计划命令生成；该模块尚未接入统一 cliconf 执行路径。

```yaml
# Access port
- name: Configure access port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: access
        access_vlan: 100
    state: merged

# Trunk port
- name: Configure trunk port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/24
        mode: trunk
        trunk_allowed_vlan: "10,20,30"
    state: merged

# Hybrid port (Xike-specific feature)
- name: Configure hybrid port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/3
        mode: hybrid
        pvid: 100
        hybrid_untagged_vlan: "10,20"
        hybrid_tagged_vlan: "30,40"
    state: merged
```

### Layer 3 VLAN Interfaces

> 当前 `xikeos_l3_interfaces` 示例展示参数和计划命令生成；该模块尚未接入统一 cliconf 执行路径。

```yaml
# Configure SVI IP address
- name: Set VLAN interface IP
  xike.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 100
        ipv4:
          - address: 192.168.100.1
            subnet_mask: 255.255.255.0
    state: merged

# IPv6 on VLAN interface
- name: Set IPv6 address
  xike.xikeos.xikeos_l3_interfaces:
    config:
      - name: vlan-interface 200
        ipv6:
          - address: "2001:db8::1/64"
    state: merged
```

### LAG (eth-trunk)

```yaml
# Create static eth-trunk
- name: Create static LAG
  xike.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 1
        mode: static
        members:
          - "0/0/1"
          - "0/0/2"
    state: merged

# Create dynamic eth-trunk with LACP
- name: Create LACP LAG
  xike.xikeos.xikeos_lag_interfaces:
    config:
      - name: eth-trunk 2
        mode: dynamic
        lacp_mode: active
        members:
          - "0/0/3"
          - "0/0/4"
    state: merged
```

### OSPF

```yaml
# Basic OSPF configuration
- name: Configure OSPF
  xike.xikeos.xikeos_ospfv2:
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
    state: merged

# OSPF with redistribution
- name: Configure OSPF with redistribution
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - network: 10.0.0.0
          wildcard: 0.0.255.255
          area: "0"
      redistribute:
        - protocol: static
          metric: 10
        - protocol: connected
          route_map: REDIST-CONNECTED
      default_info_originate: true
      default_info_originate_always: true
      passive_interfaces:
        - vlan-interface 10
        - vlan-interface 20
    state: merged
```

### Static Routes

```yaml
# Add IPv4 static route
- name: Configure static route
  xike.xikeos.xikeos_static_routes:
    config:
      - destination: 192.168.100.0
        mask: 255.255.255.0
        next_hop: 10.0.0.2
        distance: 1
        route_type: ipv4
    state: merged

# Add IPv6 static route
- name: Configure IPv6 route
  xike.xikeos.xikeos_static_routes:
    config:
      - destination: "2001:db8::"
        mask: "48"
        next_hop: "2001:db8::1"
        route_type: ipv6
    state: merged
```

### ACLs

```yaml
# Standard ACL (1-999)
- name: Create standard IP ACL
  xike.xikeos.xikeos_acls:
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

# MAC ACL (1000-1999)
- name: Create MAC ACL
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 1001
        acl_type: mac
        remark: Filter by MAC address
        rules:
          - sequence: 10
            action: permit
            source: 0011.2233.4455
            destination: 0000.0000.0000
    state: merged

# Mixed/Extended ACL (2000-2999)
- name: Create mixed ACL
  xike.xikeos.xikeos_acls:
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

### STP

```yaml
# Configure MSTP
- name: Set STP mode to MSTP
  xike.xikeos.xikeos_stp:
    config:
      stp_mode: mstp
      priority: 4096
      hello_time: 2
      forward_time: 15
      max_age: 20
      mstp:
        region_name: SWITCH-REGION
        revision: 1
        instances:
          - instance_id: 0
            priority: 4096
            vlans: [1, 100]
          - instance_id: 1
            priority: 8192
            vlans: [200, 300]
    state: merged
```

### Port Mirroring

```yaml
# Create mirror group
- name: Set up port mirroring
  xike.xikeos.xikeos_mirror:
    config:
      group_id: 1
      source_interfaces:
        - name: ethernet 0/0/1
          direction: both
        - name: ethernet 0/0/2
          direction: ingress
      destination_interface: ethernet 0/0/10
    state: present

# Remove mirror group
- name: Delete mirror group
  xike.xikeos.xikeos_mirror:
    config:
      group_id: 1
    state: absent
```

### ERPS (G.8032 Ring Protection)

```yaml
# Configure ERPS instance
- name: Configure ERPS
  xike.xikeos.xikeos_erps:
    instance_id: 1
    control_vlan: 100
    port0: "ethernet 0/0/1"
    port1: "ethernet 0/0/2"
    work_mode: revertive
    protected_instances: "1,2,5-10"
    ring_enable: true
    guard_timer: 500
    wtr_timer: 5
    state: present
```

### EAPS (Ethernet Automatic Protection Switching)

```yaml
# Configure EAPS domain
- name: Configure EAPS
  xike.xikeos.xikeos_eaps:
    domain_id: 1
    control_vlan: 100
    rings:
      - ring_id: 1
        role: master
        enabled: true
      - ring_id: 2
        role: transit
        enabled: true
    work_mode: standard
    state: present
```

### QinQ (VLAN Stacking)

```yaml
# Configure QinQ
- name: Set up QinQ
  xike.xikeos.xikeos_qinq:
    config:
      mode: customer
      inner_tpid: "0x8100"
      outer_tpid: "0x88a8"
      vlan_inserts:
        - start_vlan: 100
          end_vlan: 200
          service_vlan: 500
          priority: 0
      vlan_pass_throughs:
        - start_vlan: 300
          end_vlan: 400
    state: present
```

### Flex-Link / Monitor-Link

```yaml
# Configure Flex-Link backup
- name: Configure Flex-Link
  xike.xikeos.xikeos_flex_monitor_link:
    config:
      flex_links:
        - group_id: 1
          master_port:
            type: eth
            id: "0/0/1"
          slave_port:
            type: eth
            id: "0/0/2"
          preemption_mode: enabled
      monitor_links:
        - uplink:
            type: eth
            id: "0/0/24"
          downlinks:
            - type: eth
              id: "0/0/1"
            - type: eth
              id: "0/0/2"
    state: present
```

### Port Isolation

```yaml
# Create port isolation group
- name: Isolate access ports
  xike.xikeos.xikeos_port_isolate:
    config:
      group_id: 1
      members:
        - ethernet 0/0/1
        - ethernet 0/0/2
        - ethernet 0/0/3
    state: present
```

## Playbook Patterns

### Configuration Backup

```yaml
# backup_config.yml
---
- name: Backup Xike Switch Configuration
  hosts: xike_switches
  gather_facts: no
  tasks:
    - name: Run show running-config
      xike.xikeos.xikeos_command:
        commands:
          - show running-config
      register: config_output

    - name: Save backup to file
      ansible.builtin.copy:
        content: "{{ config_output.stdout[0] }}"
        dest: "backups/{{ inventory_hostname }}_{{ ansible_date_time.date }}.cfg"
      delegate_to: localhost
```

### Partial Deployment

> Only `xikeos_vlans` and `xikeos_config` in this example execute through the current reference path. L2/L3 modules shown here currently report planned commands and need follow-up execution-path refactors before they can be used for full deployment.

```yaml
# deploy_switch.yml
---
- name: Deploy Xike Switch Configuration
  hosts: xike_switches
  gather_facts: no
  tasks:
    - name: Create VLANs
      xike.xikeos.xikeos_vlans:
        config:
          - vlan_id: 100
            name: DATA
          - vlan_id: 200
            name: VOICE
        state: merged

    - name: Plan L3 interface configuration
      xike.xikeos.xikeos_l3_interfaces:
        config:
          - name: vlan-interface 100
            ipv4:
              - address: "{{ mgmt_ip }}"
                subnet_mask: 255.255.255.0
        state: merged

    - name: Plan access port configuration
      xike.xikeos.xikeos_l2_interfaces:
        config:
          - name: ethernet 0/0/1
            mode: access
            access_vlan: 100
          - name: ethernet 0/0/2
            mode: access
            access_vlan: 200
        state: merged

    - name: Plan trunk uplink configuration
      xike.xikeos.xikeos_l2_interfaces:
        config:
          - name: ethernet 0/0/24
            mode: trunk
            trunk_allowed_vlan: "100,200"
        state: merged

    - name: Save configuration
      xike.xikeos.xikeos_config:
        lines:
          - hostname deployed-switch
        save: true
```

### Health Check

```yaml
# health_check.yml
---
- name: Xike Switch Health Check
  hosts: xike_switches
  gather_facts: no
  tasks:
    - name: Show version
      xike.xikeos.xikeos_command:
        commands:
          - show version
      register: version

    - name: Show VLAN
      xike.xikeos.xikeos_command:
        commands:
          - show vlan
      register: vlans

    - name: Show interface status
      xike.xikeos.xikeos_command:
        commands:
          - show interface status
      register: interfaces

    - name: Show spanning-tree
      xike.xikeos.xikeos_command:
        commands:
          - show spanning-tree
      register: stp

    - name: Display health summary
      ansible.builtin.debug:
        msg: |
          === {{ inventory_hostname }} Health Check ===
          Version: {{ version.stdout[0] | first_line }}
          VLANs configured: {{ vlans.stdout[0] | count_lines }}
          STP Root: {{ stp.stdout[0] | regex_search('Root ID.*') }}
```

## Credential Management

Never store passwords in plain text. Use `ansible-vault` for encryption.

### Encrypt a Password

```bash
# Create or edit the vault file
ansible-vault create group_vars/xike_switches/vault.yml

# Add encrypted content:
# vault_switch_password: my_secret_password
# vault_enable_password: my_enable_password
```

### Reference in Inventory

```yaml
# inventory.yml
all:
  children:
    xike_switches:
      hosts:
        core-sw01:
          ansible_host: 192.168.1.100
          ansible_user: admin
          ansible_password: "{{ vault_switch_password }}"
```

### Run Playbooks with Vault

```bash
# Prompt for vault password
ansible-playbook -i inventory.yml deploy_switch.yml --ask-vault-pass

# Use vault password file
ansible-playbook -i inventory.yml deploy_switch.yml --vault-password-file ~/.vault_pass

# Use multiple vault IDs
ansible-playbook -i inventory.yml deploy_switch.yml --vault-id prod@prompt
```

## Cisco IOS Comparison

Xike switches use a Cisco IOS-like CLI with some key differences:

| Feature | Cisco IOS | Xike OS |
|---------|-----------|---------|
| **Port Mode** | `switchport mode access/trunk` | `switchport link-type access/trunk/hybrid` |
| **Hybrid Mode** | Not available | `switchport link-type hybrid` |
| **Port Channel** | `interface Port-channel1` | `interface eth-trunk 1` |
| **Port Mirroring** | `monitor session 1` | `mirror group 1` |
| **VLAN Interface** | `interface Vlan100` | `interface vlan-interface 100` |
| **Port Naming** | `GigabitEthernet0/1` | `ethernet 0/0/1` |
| **Ring Protection** | FlexLink / REP | ERPS (G.8032) / EAPS |
| **QinQ** | `switchport voice vlan` | `qinq` with explicit TPID/VLAN mapping |
| **ACL Ranges** | 1-99 (std), 100-199, 1300-2699 | 1-999 (std), 1000-1999 (MAC), 2000-2999 (mixed) |
| **STP** | `spanning-tree mode pvst` | `stp mode pvst` |
| **Save Config** | `write memory` | `write memory` |
| **Show VLAN** | `show vlan brief` | `show vlan` |
| **LACP** | `channel-group 1 mode active` | `eth-trunk 1 mode dynamic lacp-mode active` |

## Development

### Project Structure

```
xike-xikeos/
├── galaxy.yml                          # Collection metadata
├── README.md                           # This file
├── plugins/
│   ├── terminal/                       # Prompt, paging, and error handling
│   │   └── xikeos.py
│   ├── cliconf/                        # Command/config API over network_cli
│   │   └── xikeos.py
│   ├── modules/                        # Ansible modules
│   │   ├── xikeos_vlans.py             # VLAN management
│   │   ├── xikeos_interfaces.py        # Interface configuration
│   │   ├── xikeos_l2_interfaces.py     # L2 access/trunk/hybrid
│   │   ├── xikeos_l3_interfaces.py     # L3 VLAN interfaces
│   │   ├── xikeos_lag_interfaces.py    # LAG eth-trunk bundles
│   │   ├── xikeos_ospfv2.py            # OSPF routing
│   │   ├── xikeos_static_routes.py     # Static routes
│   │   ├── xikeos_acls.py              # Access Control Lists
│   │   ├── xikeos_stp.py               # Spanning Tree Protocol
│   │   ├── xikeos_mirror.py            # Port mirroring
│   │   ├── xikeos_port_isolate.py      # Port isolation
│   │   ├── xikeos_erps.py              # ERPS ring protection
│   │   ├── xikeos_eaps.py              # EAPS protection
│   │   ├── xikeos_qinq.py              # QinQ VLAN stacking
│   │   ├── xikeos_flex_monitor_link.py # Flex-Link / Monitor-Link
│   │   ├── xikeos_config.py            # Raw config push
│   │   └── xikeos_command.py           # Read-only commands
│   └── module_utils/
│       ├── xikeos.py                   # Shared utilities
│       ├── network/xikeos/xikeos.py    # Connection helper functions
│       └── facts/                      # Facts parsers
│           ├── vlans.py
│           ├── interfaces.py
│           ├── l2_interfaces.py
│           ├── l3_interfaces.py
│           ├── lag_interfaces.py
│           ├── ospfv2.py
│           ├── static_routes.py
│           ├── acls.py
│           ├── stp.py
│           ├── mirror.py
│           ├── port_isolate.py
│           ├── erps.py
│           ├── eaps.py
│           ├── qinq.py
│           └── flex_monitor_link.py
└── tests/                              # Unit tests
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

### Running Tests

```bash
# Run all tests
uv run pytest -q tests/unit

# Run with verbose output
uv run pytest tests/unit -v

# Run OpenSpec/network architecture tests
uv run pytest -q tests/unit/test_openspec_tasks.py

# Run linting
ansible-lint plugins/
```

### Adding a New Module

1. Create the module file in `plugins/modules/xikeos_<name>.py`
2. Create the facts parser in `plugins/module_utils/facts/<name>.py`
3. Add tests in `tests/unit/test_xikeos_<name>.py`
4. Update this README with the new module in the Available Modules table
5. Submit a PR

## License

MIT License. See [LICENSE](LICENSE) for details.
