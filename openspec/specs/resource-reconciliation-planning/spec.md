## Purpose
Define the internal pure reconciliation planner contract for normalized Xike OS resource state, semantic operations, and simulated after-state.

## Requirements

### Requirement: Reconciler plans semantic operations from normalized state
The collection SHALL provide an internal pure reconciliation planner that converts normalized current state, normalized desired state, a supported state value, and a resource policy into deterministic semantic operations.

#### Scenario: Planner emits operations without device access
- **WHEN** the planner receives normalized current and desired resources
- **THEN** it MUST return semantic operations without connecting to a device
- **AND** it MUST NOT generate XikeOS CLI command strings

#### Scenario: Planner output is deterministic
- **WHEN** the planner is called repeatedly with equivalent normalized inputs
- **THEN** it MUST return operations in a stable order

### Requirement: Reconciler supports scalar and set field policies
The reconciler MVP SHALL support scalar fields and set fields identified by stable item identity.

#### Scenario: Scalar field differs
- **WHEN** a desired scalar field is explicitly declared and differs from current state
- **THEN** the planner MUST emit a `set_field` operation for that field

#### Scenario: Set field has desired-only item
- **WHEN** a desired set item is absent from current state
- **THEN** the planner MUST emit an `add_item` operation for that item

#### Scenario: Set field has current-only item in replaced state
- **WHEN** a set field is explicitly declared in desired state
- **AND** the resource state is `replaced`
- **AND** a current set item is absent from the desired set
- **THEN** the planner MUST emit a `remove_item` operation if removal is supported

### Requirement: Merged state is non-destructive for set fields
The reconciler SHALL treat `merged` as an additive/update state that does not remove current-only set items.

#### Scenario: Merged adds set item without removing existing item
- **WHEN** current state contains a set item not listed in desired state
- **AND** desired state contains a new set item
- **AND** the requested state is `merged`
- **THEN** the planner MUST emit `add_item` for the new desired item
- **AND** it MUST NOT emit `remove_item` for the current-only item

### Requirement: Replaced state is scoped to listed resources and explicit fields
The reconciler SHALL treat `replaced` as synchronization of explicitly declared fields for resources listed in desired state.

#### Scenario: Replaced does not delete unlisted resource
- **WHEN** current state contains two resources
- **AND** desired state lists only one resource
- **AND** the requested state is `replaced`
- **THEN** the planner MUST NOT emit operations that delete the unlisted resource

#### Scenario: Replaced ignores omitted field
- **WHEN** current state contains a field that is omitted from desired state
- **AND** the requested state is `replaced`
- **THEN** the planner MUST NOT emit operations for the omitted field

#### Scenario: Replaced clears explicit empty set field
- **WHEN** desired state explicitly declares an empty set field
- **AND** current state contains items in that set field
- **AND** the requested state is `replaced`
- **THEN** the planner MUST emit `remove_item` operations for current items if removal is supported

### Requirement: Unsupported removals fail fast
The reconciler SHALL fail before producing a plan when the requested state requires a removal for a field whose policy does not support removal.

#### Scenario: Remove unsupported scalar field
- **WHEN** desired state explicitly requests clearing a scalar field
- **AND** the field policy marks removal as unsupported
- **THEN** the planner MUST fail with contextual information about the resource key, field, and state

### Requirement: Reconciler simulates after-state from operations
The reconciler SHALL provide a deterministic helper that applies planned operations to normalized current state to produce simulated after-state.

#### Scenario: Apply add operation to after-state
- **WHEN** simulated after-state is computed for an `add_item` operation
- **THEN** the resulting resource field MUST include the added item

#### Scenario: Apply remove operation to after-state
- **WHEN** simulated after-state is computed for a `remove_item` operation
- **THEN** the resulting resource field MUST omit the removed item
