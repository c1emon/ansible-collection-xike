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
