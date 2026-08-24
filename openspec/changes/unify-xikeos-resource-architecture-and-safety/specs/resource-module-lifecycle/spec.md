## ADDED Requirements

### Requirement: Core lifecycle modules share one planning architecture
The VLAN, base-interface, L2-interface, L3-interface, LAG-interface, static-route, and ACL modules SHALL use the common canonical normalization, reconciliation plan, lifecycle, and sanitization boundaries for every supported mutating state.

#### Scenario: Core module plans a mutation
- **WHEN** a core lifecycle module receives a supported mutating state
- **THEN** it MUST normalize desired and current data into its canonical policy
- **AND** it MUST obtain acknowledged operations, rendered commands, changed status, and simulated after-state from one sealed resource plan

#### Scenario: Core module cannot express safe semantics
- **WHEN** a core module cannot safely gather, identify, remove, reset, or render a requested transition
- **THEN** it MUST fail before applying commands or remove that state from its supported choices

### Requirement: Lifecycle result payloads are sanitized
The resource lifecycle boundary SHALL sanitize commands, before/after state, device responses, typed error context, and generic exception details before calling `exit_json` or `fail_json`.

#### Scenario: Resource command contains credential operand
- **WHEN** a lifecycle result or failure includes a command containing a known credential operand
- **THEN** the returned command context MUST preserve non-secret command structure
- **AND** it MUST replace the credential value with the collection redaction marker

#### Scenario: Partial apply failure contains device detail
- **WHEN** apply fails after command execution may have started
- **THEN** partial-change metadata MUST be retained
- **AND** every returned nested value MUST pass through shared sanitization

## MODIFIED Requirements

### Requirement: Lifecycle modules use reconciler-planned command diffs
All core declarative resource modules SHALL use one shared `ResourcePlan` to compute semantic operations, rendered command diffs, changed status, and simulated check-mode after-state while preserving gather, apply, and post-apply verification in the lifecycle helper.

#### Scenario: Reconciler-planned check mode does not apply configuration
- **WHEN** a core resource module runs in check mode with pending operations
- **THEN** it MUST return `changed: true`, the rendered command list, and simulated after-state from the same plan
- **AND** every operation MUST be acknowledged by the renderer before the plan reaches the lifecycle helper
- **AND** it MUST NOT call the network configuration apply path

#### Scenario: Reconciler-planned no-op
- **WHEN** canonical desired state already matches current state
- **THEN** the plan and rendered command list MUST be empty
- **AND** the module MUST return `changed: false`
- **AND** it MUST NOT apply configuration

#### Scenario: Non-check execution verifies actual after-state
- **WHEN** a core module successfully applies commands and supports post-apply gather
- **THEN** post-apply gathered state MUST replace simulated after-state as the returned authoritative `after`

#### Scenario: Reconciler-backed module preserves lifecycle result contract
- **WHEN** a reconciler-backed resource module runs in a mutating state
- **THEN** the result MUST continue to include sanitized `before`, `after`, `commands`, and `changed` values according to the standard lifecycle contract

#### Scenario: Rendered state previews without reporting a mutation
- **WHEN** a core module runs with `state=rendered`
- **THEN** it MAY return non-empty preview commands from a completely rendered plan
- **AND** it MUST return `changed: false` and MUST NOT call gather or apply paths

### Requirement: Resource modules honor check mode after diff calculation
Declarative Xike OS resource modules SHALL compute one complete resource plan before exiting in check mode and SHALL NOT modify the target device in check mode.

#### Scenario: Check mode with pending resource change
- **WHEN** a resource module runs in check mode and canonical desired state differs from current state
- **THEN** it MUST return `changed: true`, include commands rendered from the plan, and return after-state produced by applying the same plan operations
- **AND** it MUST NOT call the network configuration apply path

#### Scenario: Check mode preserves unlisted resources
- **WHEN** a listed-resource `replaced` operation is planned in check mode
- **THEN** simulated after-state MUST preserve unlisted resources
- **AND** it MUST NOT claim any transition for which the plan has no operation

#### Scenario: Check mode without pending resource change
- **WHEN** a resource module runs in check mode and its resource plan has no operations
- **THEN** it MUST return `changed: false`, include an empty command list, and return stable before/after state
- **AND** it MUST NOT call the network configuration apply path
