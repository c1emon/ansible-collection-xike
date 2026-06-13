## MODIFIED Requirements

### Requirement: Resource modules follow a standard lifecycle
Declarative Xike OS resource modules SHALL follow a standard lifecycle for mutating states: validate input, gather current state as `before`, normalize current and desired state, compute configuration commands, honor check mode, apply changes through the Xike OS network configuration path, and report `after` state.

#### Scenario: Mutating resource module changes device
- **WHEN** a resource module runs in a mutating state and desired state differs from gathered current state
- **THEN** it MUST return `changed: true`, include the command list, apply those commands through the network configuration path when not in check mode, and return `before` and `after` state.

#### Scenario: Mutating resource module has no diff
- **WHEN** a resource module runs in a mutating state and desired state already matches gathered current state
- **THEN** it MUST return `changed: false`, MUST NOT apply configuration commands, and MUST return `before` and `after` state representing no state transition.

#### Scenario: Apply fails after command execution starts
- **WHEN** a resource module starts applying configuration commands and the lower-level apply path fails
- **THEN** it MUST fail with `changed: true`, include the attempted command list, and indicate that device state may be partially changed.

#### Scenario: Post-apply gather fails
- **WHEN** a resource module successfully applies configuration commands but cannot gather final state
- **THEN** it MUST fail with `changed: true`, include the attempted command list and safe before/planned context, and indicate that final device state could not be verified.

### Requirement: Resource facts failures are explicit
Declarative Xike OS resource modules that require current state for diffing SHALL fail explicitly when required facts cannot be gathered or parsed.

#### Scenario: Required facts command fails
- **WHEN** a resource module cannot execute the show or configuration retrieval command required to gather current state
- **THEN** it MUST fail with context about the failed gather operation and MUST NOT continue with empty current state.

#### Scenario: Required facts parser fails
- **WHEN** a resource module receives device output but cannot parse the fields required for idempotent diffing
- **THEN** it MUST fail with parser context and MUST NOT compute a diff against empty current state.

#### Scenario: Facts provider raises typed error
- **WHEN** a facts provider raises a typed Xike OS facts, parse, command, or connection error during required state gathering
- **THEN** the resource gather wrapper or lifecycle helper MUST fail with resource-specific gather context and MUST NOT continue with empty current state.
