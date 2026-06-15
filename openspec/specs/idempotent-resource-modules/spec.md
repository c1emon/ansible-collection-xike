## Purpose
Define the reference behavior for idempotent Xike OS resource modules, starting with VLAN state gathering, diffing, check mode, and before/after reporting.

## Requirements

### Requirement: Resource modules gather current device state
Reference resource modules SHALL gather current device state from the target device before computing changes. Resource modules that require parser templates at runtime SHALL receive required template content through internal action-plugin injection so current-state gathering does not depend on non-Python template files being present inside the module payload.

#### Scenario: VLAN module gathers before state
- **WHEN** `xikeos_vlans` runs against a device
- **THEN** it MUST collect VLAN state from device show-command output and expose the normalized state as `before`.

#### Scenario: VLAN current-state gathering preserves normalized parser contract
- **WHEN** `xikeos_vlans` gathers current state from `show vlan` output parsed through the internal template path
- **THEN** it MUST receive the same normalized VLAN fields required for idempotent diffing, including integer VLAN IDs, names, states, VLAN types, media, and port lists.

#### Scenario: VLAN gathering works without template files in module payload
- **WHEN** `xikeos_vlans` runs from an Ansible module payload that does not include parser template data files
- **THEN** it MUST still gather VLAN state using template content injected by the action plugin.

### Requirement: Resource modules compute idempotent command diffs
Reference resource modules SHALL compare desired state with gathered current state and generate only the commands needed to reach the desired state.

#### Scenario: Desired VLAN already exists
- **WHEN** the requested VLAN state already matches the gathered device state
- **THEN** `xikeos_vlans` MUST return `changed: false` and MUST NOT send configuration commands.

#### Scenario: Desired VLAN differs
- **WHEN** the requested VLAN state differs from the gathered device state
- **THEN** `xikeos_vlans` MUST return `changed: true` and MUST generate the minimal command list needed to converge the state.

### Requirement: Resource modules respect check mode
Reference resource modules SHALL support check mode by reporting planned changes without modifying the target device.

#### Scenario: VLAN change in check mode
- **WHEN** `xikeos_vlans` runs in check mode with desired state differing from current state
- **THEN** it MUST return `changed: true` and the planned commands, and MUST NOT send configuration commands to the device.

### Requirement: Resource modules return normalized before and after state
Reference resource modules SHALL return normalized `before` and `after` state for changed and unchanged executions.

#### Scenario: VLAN change reports state transition
- **WHEN** `xikeos_vlans` computes a change
- **THEN** the result MUST include `before`, `after`, `commands`, and `changed` fields that describe the intended state transition.

### Requirement: All migrated resource modules provide truthful idempotent results
Migrated Xike OS resource modules SHALL compute `changed` from the actual command diff between normalized desired state and gathered current state, and SHALL NOT report `changed: true` unless commands would be applied outside check mode.

#### Scenario: Migrated module detects no change
- **WHEN** a migrated resource module runs with desired state matching the gathered current state
- **THEN** it MUST return `changed: false`, an empty `commands` list, and MUST NOT apply configuration commands.

#### Scenario: Migrated module detects a change
- **WHEN** a migrated resource module runs with desired state differing from the gathered current state
- **THEN** it MUST return `changed: true`, include the minimal command list required to converge state, and apply those commands when not in check mode.

### Requirement: Migrated resource modules report before and after consistently
Migrated Xike OS resource modules SHALL return normalized `before` and `after` state for mutating and non-mutating executions.

#### Scenario: Changed execution reports transition
- **WHEN** a migrated resource module applies a configuration change
- **THEN** it MUST return `before` from gathered pre-change state and `after` from post-change gathered state or from a documented simulated transition.

#### Scenario: Unchanged execution reports stable state
- **WHEN** a migrated resource module has no command diff
- **THEN** it MUST return `before` and `after` values that represent the same normalized state.

### Requirement: VLAN module is the reference lifecycle implementation
The `xikeos_vlans` module SHALL serve as the reference implementation for the resource-module lifecycle and SHALL define edge-case semantics for VLAN state, description, replacement, deletion, check mode, and after-state reporting.

#### Scenario: VLAN lifecycle remains complete
- **WHEN** `xikeos_vlans` runs in a supported mutating state
- **THEN** it MUST gather current VLAN state, compute minimal commands, honor check mode, apply through the network configuration path when not in check mode, and report normalized `before` and `after` state.

#### Scenario: VLAN unsupported edge case is explicit
- **WHEN** a requested VLAN behavior cannot be represented safely by supported Xike OS commands
- **THEN** `xikeos_vlans` MUST fail explicitly or document and return a non-mutating rendered result, rather than silently ignoring the requested behavior.

### Requirement: L3 interfaces merged state is additive
The `xikeos_l3_interfaces` module SHALL treat `state: merged` as additive for IPv4 and IPv6 address sets.

#### Scenario: L3 merged adds IPv4 without removing existing IPv4
- **WHEN** current L3 interface state contains IPv4 address `10.0.0.1 255.255.255.0`
- **AND** desired config for the same interface contains IPv4 address `10.0.0.2 255.255.255.0`
- **AND** the module runs with `state: merged`
- **THEN** it MUST render a command to add `10.0.0.2 255.255.255.0`
- **AND** it MUST NOT render a command to remove `10.0.0.1 255.255.255.0`

#### Scenario: L3 merged adds IPv6 without removing existing IPv6
- **WHEN** current L3 interface state contains IPv6 address `2001:db8::1/64`
- **AND** desired config for the same interface contains IPv6 address `2001:db8::2/64`
- **AND** the module runs with `state: merged`
- **THEN** it MUST render a command to add `2001:db8::2/64`
- **AND** it MUST NOT render a command to remove `2001:db8::1/64`

### Requirement: L3 interfaces replaced state synchronizes listed explicit fields
The `xikeos_l3_interfaces` module SHALL treat `state: replaced` as exact synchronization of explicitly declared address fields for listed interfaces only.

#### Scenario: L3 replaced synchronizes IPv4 for listed interface
- **WHEN** current L3 interface state contains IPv4 addresses `10.0.0.1 255.255.255.0` and `10.0.0.2 255.255.255.0`
- **AND** desired config for the same interface explicitly contains only IPv4 address `10.0.0.3 255.255.255.0`
- **AND** the module runs with `state: replaced`
- **THEN** it MUST render commands to remove the two current IPv4 addresses
- **AND** it MUST render a command to add the desired IPv4 address

#### Scenario: L3 replaced does not affect unlisted interface
- **WHEN** current L3 interface state contains `vlan-interface 10` and `vlan-interface 20`
- **AND** desired config lists only `vlan-interface 10`
- **AND** the module runs with `state: replaced`
- **THEN** simulated after-state MUST preserve `vlan-interface 20`

#### Scenario: L3 replaced ignores omitted IPv6 field
- **WHEN** current L3 interface state contains IPv4 and IPv6 addresses
- **AND** desired config explicitly declares IPv4 but omits IPv6
- **AND** the module runs with `state: replaced`
- **THEN** the module MUST NOT render commands that remove IPv6 addresses

### Requirement: LAG interfaces merged state is additive for members
The `xikeos_lag_interfaces` module SHALL treat `state: merged` as additive for LAG members.

#### Scenario: LAG merged adds member without removing existing members
- **WHEN** current LAG state for `eth-trunk 1` contains members `0/0/1` and `0/0/2`
- **AND** desired config for `eth-trunk 1` contains member `0/0/3`
- **AND** the module runs with `state: merged`
- **THEN** it MUST render a command to add member `0/0/3`
- **AND** it MUST NOT render commands to remove members `0/0/1` or `0/0/2`

### Requirement: LAG interfaces replaced state synchronizes listed explicit fields
The `xikeos_lag_interfaces` module SHALL treat `state: replaced` as exact synchronization of explicitly declared fields for listed LAG resources only.

#### Scenario: LAG replaced synchronizes members
- **WHEN** current LAG state for `eth-trunk 1` contains members `0/0/1` and `0/0/2`
- **AND** desired config for `eth-trunk 1` explicitly contains members `0/0/2` and `0/0/3`
- **AND** the module runs with `state: replaced`
- **THEN** it MUST render a command to remove member `0/0/1`
- **AND** it MUST render a command to add member `0/0/3`

#### Scenario: LAG replaced does not affect unlisted trunk
- **WHEN** current LAG state contains `eth-trunk 1` and `eth-trunk 2`
- **AND** desired config lists only `eth-trunk 1`
- **AND** the module runs with `state: replaced`
- **THEN** simulated after-state MUST preserve `eth-trunk 2`

#### Scenario: LAG member order is idempotent
- **WHEN** current LAG members match desired LAG members with different ordering
- **THEN** the module MUST report no member change for that ordering difference alone
