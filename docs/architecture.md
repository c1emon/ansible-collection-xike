# c1emon.xikeos Architecture

## Overview

The `c1emon.xikeos` Ansible Collection follows the standard Ansible network module architecture: playbooks use `ansible.netcommon.network_cli`, `ansible_network_os: c1emon.xikeos.xikeos`, and this collection's terminal and cliconf plugins. Netmiko Raisecom support is an optional CLI-behavior reference, not the primary backend.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Your Playbook                                     │
│                                                                              │
│   tasks:                                                                     │
│     - c1emon.xikeos.xikeos_vlans:                                             │
│         config:                                                              │
│           - vlan_id: 100                                                     │
│             name: DATA                                                       │
│         state: merged                                                        │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     c1emon.xikeos Resource Modules                             │
│                                                                              │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ Interfaces  │ │ VLANs        │ │ OSPFv2       │ │ ACLs             │    │
│  │ L2/L3/LAG   │ │ STP          │ │ Static Routes│ │ Mirror/Isolate   │    │
│  │ ERPS/EAPS   │ │ QinQ         │ │ Flex-Monitor │ │ Config/Command   │    │
│  └──────┬──────┘ └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘    │
│         │               │                │                   │              │
│         ▼               ▼                ▼                   ▼              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    generate_cli_commands()                          │    │
│  │                                                                      │    │
│  │  desired config ──► diff computation ──► CLI command list            │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              Module Utils (facts / rm_templates)                            │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Facts Parsers                                    │    │
│  │                                                                      │    │
│  │  facts/vlans.py          facts/ospfv2.py       facts/eaps.py        │    │
│  │  facts/interfaces.py     facts/stp.py          facts/erps.py        │    │
│  │  facts/l2_interfaces.py  facts/acls.py         facts/qinq.py        │    │
│  │  facts/l3_interfaces.py  facts/static_routes.py facts/mirror.py     │    │
│  │  facts/lag_interfaces.py facts/port_isolate.py facts/flex_monitor   │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    COMMAND_MAP (xikeos.py)                           │    │
│  │                                                                      │    │
│  │  show_version ──► show version                                       │    │
│  │  show_vlan ──► show vlan                                             │    │
│  │  show_interface ──► show interface                                   │    │
│  │  ...                                                                 │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│          ansible.netcommon.network_cli Platform Plugins                       │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  terminal/xikeos.py + cliconf/xikeos.py                            │    │
│  │                                                                      │    │
│  │  - Terminal plugin recognizes prompts, disables paging, detects errors │  │
│  │  - Cliconf plugin runs show commands and applies configuration       │    │
│  │  - network_cli owns the SSH transport                                │    │
│  │                                                                      │    │
│  │  Connection Flow:                                                    │    │
│  │  Module ──► cliconf ──► network_cli ──► SSH ──► Xike Switch         │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Xike Switch                                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   Cisco IOS-like CLI                                 │    │
│  │                                                                      │    │
│  │  - Similar command syntax to Cisco IOS                              │    │
│  │  - Xike-specific features (hybrid port, ERPS, EAPS, QinQ)          │    │
│  │  - Managed via SSH                                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## network_cli Platform Flow

The Ansible `network_cli` connection establishes SSH connectivity and loads this collection's platform plugins:

```
┌──────────────┐    ┌──────────────────┐    ┌──────────┐    ┌──────────────┐
│   Ansible    │───►│ cliconf/terminal │───►│network_cli│───►│  Xike Switch │
│   Module     │    │ platform plugins │    │ SSH       │    │              │
└──────────────┘    └──────────────────┘    └──────────┘    └──────────────┘
       │                    │                    │                  │
       │                    │                    │                  │
       │ send_command()     │  SSH session       │  Execute CLI     │
       │◄───────────────────┤  established       │  commands        │
       │                    │◄───────────────────┤                  │
       │                    │                    │                  │
       │ return output      │  Capture output    │  Return result   │
       │◄───────────────────┤◄───────────────────┤◄─────────────────┤
```

### Platform Plugin Implementation

The supported inventory path is:

```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: c1emon.xikeos.xikeos
```

- **Transport**: `ansible.netcommon.network_cli` over SSH
- **Terminal**: `plugins/terminal/xikeos.py` prompt, paging, privilege, and error handling
- **Cliconf**: `plugins/cliconf/xikeos.py` operational command and configuration APIs
- **References**: Netmiko Raisecom, Genie, and pyATS may inform parser and prompt work. TextFSM is a runtime dependency for complex table parsing.

### Controller-Injected Parser Templates

Modules that need bundled parser templates load those templates on the Ansible
control node through their action plugins before module execution. For VLANs,
`plugins/action/xikeos_vlans.py` reads
`plugins/module_utils/facts/textfsm_templates/show_vlan.textfsm` and injects the
template content into the module via the internal `_textfsm_templates` argument.
That argument is intentionally omitted from public module documentation and
examples.

Parser helpers prefer injected template content, then local template files for
direct development or unit-test use. If neither source is available, they raise
an explicit missing-template error naming the template and expected path instead
of silently falling back to duplicated built-in template strings. This keeps the
file templates as the parser source of truth while avoiding reliance on
non-Python template files being present in the AnsiballZ module payload.

## Resource Module Lifecycle

Each resource module follows a consistent lifecycle:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Resource Module Lifecycle                                  │
│                                                                              │
│  ┌─────────────┐                                                             │
│  │ 1. Gather   │  Run "show" commands on device                              │
│  │    Facts    │  Parse output using facts parsers                           │
│  └──────┬──────┘                                                             │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 2. Compute  │  Compare desired config with existing config                │
│  │    Diff     │  Determine what needs to change                             │
│  └──────┬──────┘                                                             │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 3. Generate │  Transform diff into CLI commands                           │
│  │    Commands │  Use setval templates or programmatic generation            │
│  └──────┬──────┘                                                             │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 4. Push     │  Send commands to device via cliconf                        │
│  │    Commands │  Execute via network_cli SSH session                        │
│  └──────┬──────┘                                                             │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 5. Verify   │  Re-gather facts (optional)                                 │
│  │    State    │  Compare before/after state                                 │
│  └─────────────┘                                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Lifecycle Details

#### 1. Gather Facts
- Modules run "show" commands (e.g., `show vlan`, `show interface brief`)
- Output is parsed using facts parsers in `plugins/module_utils/facts/`
- Each parser extracts structured data from CLI output
- Example: `facts/vlans.py` parses `show vlan` output

#### 2. Compute Diff
- Compare desired configuration (from playbook) with existing configuration (from facts)
- Determine what needs to be added, modified, or removed
- Generate a minimal set of changes needed

#### 3. Generate Commands
- Transform the computed diff into CLI commands
- Use command generation functions or setval templates
- Commands are formatted to match Xike switch CLI syntax
- Example: `interface ethernet 0/0/1` + `switchport pvid 100`

#### 4. Push Commands
- Send generated commands to the device
- Commands are executed via the cliconf plugin over `network_cli`
- `network_cli` sends commands over SSH
- Commands are sent in sequence, respecting configuration mode

#### 5. Verify State
- Re-gather facts after applying changes (when supported)
- Compare before and after states
- Return `changed: true` if modifications were made

## How rm_templates Work

### Facts Parsing (getval)

Facts parsers extract structured data from CLI output:

```python
# Example: facts/interfaces.py

def parse_interface_brief(output):
    """
    Parse 'show interface brief' output.
    
    Input (CLI output):
        Port    Desc   Link shutdn Speed         Pri PVID Mode TagVlan    UtVlan
        e0/0/1  test   up   enable  1000(FD)      0  1    TRK  100        -
    
    Output (structured data):
        [
            {
                'name': 'ethernet 0/0/1',
                'description': 'test',
                'speed': '1000',
                'duplex': 'full',
                'mode': 'TRK',
                ...
            }
        ]
    """
```

**Key patterns in facts parsers:**
- Regex patterns to match CLI output format
- TTP templates for key-value output, configuration blocks, and simple tables
- TextFSM templates for complex tables with continuation rows, such as `show vlan`
- Normalization of field values (e.g., `e0/0/1` → `ethernet 0/0/1`)
- Handling of `-` or empty values as `None`
- Conversion of abbreviations (e.g., `FD` → `full`, `ACC` → `access`)

### Command Generation (setval)

Command generation transforms desired configuration into CLI commands:

```python
# Example: xikeos_l2_interfaces.py

def build_commands(config, state, existing_config):
    """Build CLI commands from config."""
    commands = []
    
    # Enter interface mode
    commands.append('interface {0}'.format(config['name']))
    
    # Set link-type if changed
    if mode and mode != existing_mode:
        commands.append('switchport link-type {0}'.format(mode))
    
    # Set PVID if changed
    if pvid and pvid != existing_pvid:
        commands.append('switchport pvid {0}'.format(pvid))
    
    return commands
```

**Key patterns in command generation:**
- Enter interface/vlan/instance mode first
- Set properties only when they differ from existing
- Use `no` prefix to remove configurations
- Respect command ordering dependencies

### The COMMAND_MAP

The `COMMAND_MAP` in `plugins/module_utils/xikeos.py` provides a mapping between logical command names and actual CLI commands:

```python
COMMAND_MAP = {
    'show_version': 'show version',
    'show_vlan': 'show vlan',
    'show_interface': 'show interface',
    'show_interface_brief': 'show interface brief',
    'show_ip_route': 'show ip route',
    'show_stp': 'show stp interface brief',
    'show_running_config': 'show running-config',
    # ... more mappings
}
```

This allows modules to use logical names while the actual CLI commands are defined in one place.

## Data Flow Between Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Data Flow Diagram                                    │
│                                                                              │
│  Playbook                Module                  Facts Parser                │
│  ────────                ──────                  ────────────                │
│                                                                              │
│  desired_config ─────► ┌──────────┐                                           │
│                        │ Module   │                                           │
│                        │ main()   │                                           │
│                        └────┬─────┘                                           │
│                             │                                                 │
│                             │ 1. Gather facts                                 │
│                             ▼                                                 │
│                        ┌──────────┐     ┌──────────────┐                     │
│                        │ run show │────►│ Facts Parser │                     │
│                        │ commands │     │ (getval)     │                     │
│                        └──────────┘     └──────┬───────┘                     │
│                                                │                              │
│                                                ▼                              │
│                        ┌──────────┐     ┌──────────────┐                     │
│                        │ Compute  │◄────│ existing     │                     │
│                        │ Diff     │     │ config       │                     │
│                        └────┬─────┘     └──────────────┘                     │
│                             │                                                 │
│                             │ 3. Generate commands                            │
│                             ▼                                                 │
│                        ┌──────────┐                                           │
│                        │ Generate │                                           │
│                        │ Commands │                                           │
│                        │ (setval) │                                           │
│                        └────┬─────┘                                           │
│                             │                                                 │
│                             │ 4. Push commands                                │
│                             ▼                                                 │
│                        ┌──────────┐     ┌──────────────┐                     │
│                        │ Connection│────►│ Xike Switch  │                     │
│                        │ Plugin   │     │              │                     │
│                        └──────────┘     └──────────────┘                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## State Models

### Resource Module States (merged/replaced/deleted)

| State | Behavior |
|-------|----------|
| `merged` | Add or update configuration items. Existing items not in config are left unchanged. |
| `replaced` | Replace entire configuration for the resource. Items not in config may be removed. |
| `deleted` | Remove specified configuration items. |

### Xike-Specific Module States (present/absent)

| State | Behavior |
|-------|----------|
| `present` | Create or update the resource configuration. |
| `absent` | Remove the resource configuration. |

## Key Differences from Cisco IOS

| Feature | Cisco IOS | Xike OS |
|---------|-----------|---------|
| Interface naming | `interface GigabitEthernet0/1` | `interface ethernet 0/0/1` |
| VLAN interface | `interface Vlan100` | `interface vlan-interface 100` |
| Port modes | access, trunk | access, trunk, **hybrid** |
| STP commands | `spanning-tree` | `stp` |
| ERPS | Not native | `erps` (ITU-T G.8032) |
| EAPS | Not native | `eaps` |
| QinQ | Limited | Full support |
| LAG | `interface Port-channel` | `interface eth-trunk` |
| ACL numbering | 1-199, 1300-2699 | 1-999, 1000-1999, 2000-2999 |

## Technology Stack

| Component | Requirement | Purpose |
|-----------|-------------|---------|
| **Ansible** | >= 2.15 | Core automation engine |
| **ansible.netcommon** | >= 5.0 | `network_cli`, terminal, and cliconf support |
| **Netmiko** | optional | Reference for Raisecom-like CLI behavior only |
| **Python** | >= 3.10 | Runtime dependency |

## Directory Structure

```
c1emon.xikeos/
├── galaxy.yml                    # Collection metadata
├── README.md                     # Documentation
├── plugins/
│   ├── terminal/
│   │   └── xikeos.py            # Prompt, paging, error handling
│   ├── cliconf/
│   │   └── xikeos.py            # Command/config API over network_cli
│   ├── modules/
│   │   ├── xikeos_interfaces.py
│   │   ├── xikeos_l2_interfaces.py
│   │   ├── xikeos_l3_interfaces.py
│   │   ├── xikeos_lag_interfaces.py
│   │   ├── xikeos_vlans.py
│   │   ├── xikeos_ospf_v2.py
│   │   ├── xikeos_static_routes.py
│   │   ├── xikeos_acls.py
│   │   ├── xikeos_stp.py
│   │   ├── xikeos_mirror.py
│   │   ├── xikeos_port_isolate.py
│   │   ├── xikeos_erps.py
│   │   ├── xikeos_eaps.py
│   │   ├── xikeos_qinq.py
│   │   ├── xikeos_flex_monitor_link.py
│   │   ├── xikeos_config.py
│   │   └── xikeos_command.py
│   └── module_utils/
│       ├── __init__.py
│       ├── xikeos.py             # COMMAND_MAP and constants
│       └── facts/
│           ├── __init__.py
│           ├── interfaces.py
│           ├── l2_interfaces.py
│           ├── l3_interfaces.py
│           ├── lag_interfaces.py
│           ├── vlans.py
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
└── docs/
    ├── architecture.md
    ├── modules.md
    ├── faq.md
    └── development.md
```
