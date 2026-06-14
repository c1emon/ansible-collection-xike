## ADDED Requirements

### Requirement: Lifecycle modules use reconciler-planned command diffs
Declarative resource modules that adopt the internal reconciler SHALL use it to compute command diffs and simulated after-state while preserving the standard lifecycle for gather, check mode, apply, and post-apply verification.

#### Scenario: Reconciler-planned check mode does not apply configuration
- **WHEN** a reconciler-backed resource module runs in check mode with pending operations
- **THEN** it MUST return `changed: true`, the rendered command list, and simulated `after` state
- **AND** it MUST NOT call the network configuration apply path

#### Scenario: Reconciler-backed module preserves lifecycle result contract
- **WHEN** a reconciler-backed resource module runs in a mutating state
- **THEN** the result MUST continue to include `before`, `after`, `commands`, and `changed` according to the standard lifecycle contract

### Requirement: Rendered resource planning does not gather device state
Reconciler-backed modules that support `rendered` SHALL plan commands from empty or explicitly supplied synthetic current state without gathering live device state.

#### Scenario: Rendered state uses synthetic current
- **WHEN** a reconciler-backed module runs with `state: rendered`
- **THEN** it MUST render commands without calling its current-state gather function
