## ADDED Requirements

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
