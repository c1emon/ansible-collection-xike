## ADDED Requirements

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
