## ADDED Requirements

### Requirement: Resource modules use mainstream return contracts
Core XikeOS resource modules SHALL use mainstream Ansible network resource module return keys for mutating, gathered, rendered, and parsed states.

#### Scenario: Mutating state returns transition contract
- **WHEN** a core resource module runs in a mutating state such as `merged`, `replaced`, or `deleted`
- **THEN** the result MUST include `before`
- **AND** it MUST include `after`
- **AND** it MUST include `commands`
- **AND** `commands` MUST be an ordered list of XikeOS CLI command strings

#### Scenario: Gathered state returns gathered key
- **WHEN** a core resource module runs with `state: gathered`
- **THEN** the result MUST include `gathered`
- **AND** the module MUST NOT modify the device

#### Scenario: Rendered state returns rendered key
- **WHEN** a core resource module runs with `state: rendered`
- **THEN** the result MUST include `rendered`
- **AND** `rendered` MUST be an ordered list of XikeOS CLI command strings
- **AND** the module MUST NOT modify the device

#### Scenario: Parsed state returns parsed key
- **WHEN** a resource module supports `state: parsed`
- **THEN** the result MUST include `parsed`
- **AND** the module MUST NOT connect to or modify the device

### Requirement: Resource state data is config-compatible
Core resource modules SHALL return `before`, `after`, `gathered`, and `parsed` values using the same normalized schema as the module `config` argument.

#### Scenario: VLAN gathered data can be reused as config
- **WHEN** `xikeos_vlans` returns VLAN items in `gathered`
- **THEN** each item MUST be valid as a `xikeos_vlans.config` item for the supported fields

#### Scenario: Interface transition data matches config schema
- **WHEN** a core resource module returns `before` and `after`
- **THEN** both values MUST use the same item shape as the module's `config` list

#### Scenario: Gathered data includes read-only observed fields
- **WHEN** a resource module includes documented read-only observed fields in `gathered`, `before`, `after`, or `parsed`
- **THEN** configurable fields MUST remain schema-compatible with the module `config` argument
- **AND** read-only fields MUST NOT change the names, nesting, or value types of configurable fields

### Requirement: Core and specialty resource maturity are explicit
The collection SHALL document which resource modules are core lifecycle targets and which resource modules are specialty or future maturity targets.

#### Scenario: Core module maturity is documented
- **WHEN** users read the resource module support matrix
- **THEN** the matrix MUST identify core lifecycle modules
- **AND** it MUST list the supported states for each core module

#### Scenario: Unsupported state is explicit
- **WHEN** a resource module receives a state that is not safely implemented
- **THEN** it MUST fail explicitly or omit that state from its argument choices
- **AND** it MUST NOT silently report applied changes for unsupported behavior

### Requirement: Risky full-replacement states require explicit semantics
Resource states that can remove unmanaged configuration, such as `overridden` or `purged`, SHALL only be exposed after the module defines explicit safe semantics for that resource type.

#### Scenario: Overridden state is not defined
- **WHEN** a module has not defined safe `overridden` semantics
- **THEN** the module MUST NOT expose `overridden` as a supported state

#### Scenario: Purged state is not meaningful
- **WHEN** a resource type cannot safely delete the resource object itself
- **THEN** the module MUST NOT expose `purged` as a supported state
