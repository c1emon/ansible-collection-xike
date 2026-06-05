## ADDED Requirements

### Requirement: Resource modules gather current device state
Reference resource modules SHALL gather current device state from the target device before computing changes.

#### Scenario: VLAN module gathers before state
- **WHEN** `xikeos_vlans` runs against a device
- **THEN** it MUST collect VLAN state from device show-command output and expose the normalized state as `before`.

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
