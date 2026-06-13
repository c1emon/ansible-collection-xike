## Purpose
Define the standard lifecycle and safety contract for Xike OS declarative resource modules.
## Requirements
### Requirement: Resource modules follow a standard lifecycle
Declarative Xike OS resource modules SHALL follow a standard lifecycle for mutating states: validate input, gather current state as `before`, normalize current and desired state, compute configuration commands, honor check mode, apply changes through the Xike OS network configuration path, and report `after` state.

#### Scenario: Mutating resource module changes device
- **WHEN** a resource module runs in a mutating state and desired state differs from gathered current state
- **THEN** it MUST return `changed: true`, include the command list, apply those commands through the network configuration path when not in check mode, and return `before` and `after` state.

#### Scenario: Mutating resource module has no diff
- **WHEN** a resource module runs in a mutating state and desired state already matches gathered current state
- **THEN** it MUST return `changed: false`, MUST NOT apply configuration commands, and MUST return `before` and `after` state representing no state transition.

### Requirement: Resource modules honor check mode after diff calculation
Declarative Xike OS resource modules SHALL compute the planned command diff before exiting in check mode and SHALL NOT modify the target device in check mode.

#### Scenario: Check mode with pending resource change
- **WHEN** a resource module runs in check mode and desired state differs from gathered current state
- **THEN** it MUST return `changed: true`, include the planned command list, and MUST NOT call the network configuration apply path.

#### Scenario: Check mode without pending resource change
- **WHEN** a resource module runs in check mode and desired state matches gathered current state
- **THEN** it MUST return `changed: false`, include an empty command list, and MUST NOT call the network configuration apply path.

### Requirement: Resource facts failures are explicit
Declarative Xike OS resource modules that require current state for diffing SHALL fail explicitly when required facts cannot be gathered or parsed.

#### Scenario: Required facts command fails
- **WHEN** a resource module cannot execute the show or configuration retrieval command required to gather current state
- **THEN** it MUST fail with context about the failed gather operation and MUST NOT continue with empty current state.

#### Scenario: Required facts parser fails
- **WHEN** a resource module receives device output but cannot parse the fields required for idempotent diffing
- **THEN** it MUST fail with parser context and MUST NOT compute a diff against empty current state.

### Requirement: Incomplete resource modules do not report false mutation
Resource modules that cannot safely gather, diff, or apply a mutating state SHALL either fail fast for that state or expose an explicitly non-mutating state such as `rendered`.

#### Scenario: Unsupported mutating state
- **WHEN** a resource module receives a mutating state that is not implemented safely
- **THEN** it MUST fail with an unsupported-state message and MUST NOT return `changed: true` for unapplied commands.

#### Scenario: Rendered state returns commands only
- **WHEN** a resource module supports an explicit `rendered` state
- **THEN** it MUST return rendered commands without modifying the device and MUST NOT represent the result as an applied device change.

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

