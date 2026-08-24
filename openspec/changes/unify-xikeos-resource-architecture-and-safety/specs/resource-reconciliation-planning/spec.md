## ADDED Requirements

### Requirement: Desired input normalization preserves actionable intent
The collection SHALL normalize Ansible-validated resource input before reconciliation so omitted fields are distinguishable from explicit actionable values without depending on private Ansible raw-argument internals.

#### Scenario: Ansible inserts None for omitted field
- **WHEN** Ansible argument validation inserts `None` for an optional nested resource field that the caller omitted
- **THEN** the desired-input normalizer MUST omit that field from canonical desired state
- **AND** the planner MUST NOT emit an operation for that field

#### Scenario: Explicit empty set is preserved
- **WHEN** the caller provides an explicit empty list for a set or ordered field
- **THEN** the desired-input normalizer MUST preserve the empty collection as an explicit value

#### Scenario: False and zero are preserved
- **WHEN** the caller provides boolean false or numeric zero as a valid field value
- **THEN** the desired-input normalizer MUST preserve that value
- **AND** it MUST NOT treat the value as omitted

#### Scenario: Null is not a scalar reset request
- **WHEN** an optional scalar reaches the module as `None`
- **THEN** the planner MUST treat it as omitted
- **AND** scalar removal MUST require a separate explicit typed reset/delete contract

#### Scenario: Optional field has an action-causing schema default
- **WHEN** an optional resource field has a non-null argument-spec default that would cause a device transition when the caller omits it
- **THEN** the module MUST either remove that default or document and test the default as an intentional ownership request
- **AND** it MUST NOT accidentally treat the schema-inserted value as caller intent

### Requirement: Planning seals one immutable resource plan after rendering
The planning boundary SHALL combine pure reconciliation and module-owned rendering into one immutable `ResourcePlan` containing semantic operations, rendered commands, changed status, and deterministic simulated after-state for a lifecycle execution.

#### Scenario: Plan has no operations
- **WHEN** normalized desired state already matches normalized current state
- **THEN** the plan MUST contain no operations
- **AND** it MUST contain no commands
- **AND** its changed status MUST be false
- **AND** its simulated after-state MUST equal normalized current state

#### Scenario: Renderer consumes every operation before plan sealing
- **WHEN** reconciliation emits one or more semantic operations for a mutating or check-mode execution
- **THEN** the module renderer MUST acknowledge every operation and produce a deterministic non-empty command list
- **AND** the sealed plan MUST set changed status true and compute simulated after-state from exactly the acknowledged operations

#### Scenario: Renderer cannot consume an operation
- **WHEN** any semantic operation is unsupported, silently dropped, or cannot produce an unambiguous command transition
- **THEN** plan sealing MUST fail before returning commands, changed status, or simulated after-state
- **AND** no partial plan may reach the lifecycle apply boundary

#### Scenario: Rendered preview contains commands
- **WHEN** `state=rendered` produces preview commands from a synthetic current state
- **THEN** the renderer MUST still acknowledge every operation
- **AND** the externally returned Ansible changed status MUST remain false because no mutation is attempted

### Requirement: Canonical state validation fails before rendering
The reconciler SHALL reject malformed or ambiguous canonical resource state before any XikeOS command is rendered.

#### Scenario: Duplicate resource identity
- **WHEN** desired or current state contains duplicate canonical resource identities
- **THEN** planning MUST fail with safe identity context

#### Scenario: Duplicate collection item identity
- **WHEN** a set or ordered field contains duplicate item identities or duplicate ordered sequence identities
- **THEN** planning MUST fail before producing operations

#### Scenario: Unknown owned field
- **WHEN** canonical input contains a field that is not declared by the resource policy or documented as read-only observed data
- **THEN** planning MUST fail instead of silently ignoring the field

### Requirement: Reconciler supports core resource policy kinds
The reconciler SHALL support only the policy kinds proven necessary by core modules: scalar fields, identity-based unordered sets, explicitly ordered collections, and resource existence operations.

#### Scenario: Ordered ACL rules differ
- **WHEN** desired ordered rules differ from current rules by identity, order, or supported compared value
- **THEN** the planner MUST emit deterministic ordered semantic operations according to the ACL policy

#### Scenario: Resource existence is owned
- **WHEN** a resource policy safely owns creation or deletion of a resource identity
- **THEN** the planner MAY emit explicit resource create or delete operations

#### Scenario: Resource deletion is not owned
- **WHEN** a resource policy does not declare safe resource deletion
- **THEN** the planner MUST reject a requested resource-delete operation

## MODIFIED Requirements

### Requirement: Reconciler plans semantic operations from normalized state
The collection SHALL provide an internal pure reconciler that converts validated canonical current state, validated canonical desired state, a supported state value, and a resource policy into deterministic semantic operations and a candidate simulated after-state for final plan sealing.

#### Scenario: Planner emits operations without device access
- **WHEN** the planner receives canonical current and desired resources
- **THEN** it MUST return semantic operations and candidate simulated after-state without connecting to a device
- **AND** it MUST NOT generate XikeOS CLI command strings

#### Scenario: Planner output is deterministic
- **WHEN** the planner is called repeatedly with equivalent canonical inputs
- **THEN** it MUST return equivalent operation sequences and candidate after-state in stable order

### Requirement: Replaced state is scoped to listed resources and explicit fields
The reconciler SHALL treat `replaced` as synchronization of explicitly declared owned fields for resources listed in desired state.

#### Scenario: Replaced does not delete unlisted resource
- **WHEN** current state contains two resources
- **AND** desired state lists only one resource
- **AND** the requested state is `replaced`
- **THEN** the planner MUST NOT emit operations that delete or reset the unlisted resource

#### Scenario: Replaced ignores omitted field
- **WHEN** current state contains a field that is omitted from canonical desired state
- **AND** the requested state is `replaced`
- **THEN** the planner MUST NOT emit operations for the omitted field
- **AND** an Ansible-normalized `None` value MUST have been removed as omitted before planning

#### Scenario: Replaced clears explicit empty set field
- **WHEN** canonical desired state explicitly contains an empty set or ordered field
- **AND** current state contains items in that field
- **AND** the requested state is `replaced`
- **THEN** the planner MUST emit removal operations if removal is supported

#### Scenario: Global replacement requires another state
- **WHEN** current state contains an unlisted resource
- **THEN** `replaced` MUST preserve that resource
- **AND** global removal MUST require a separately specified state such as future `overridden` or `purged`

### Requirement: Unsupported removals fail fast
The reconciler SHALL fail before producing a plan when desired state requests a removal or reset for which the policy has no explicit safe operation.

#### Scenario: Null is supplied for optional scalar
- **WHEN** Ansible-normalized desired input contains `None` for an optional scalar
- **THEN** input normalization MUST omit the field
- **AND** planning MUST NOT treat it as a removal request

#### Scenario: Explicit scalar reset lacks typed support
- **WHEN** desired state explicitly requests a typed scalar reset
- **AND** the field policy marks reset as unsupported
- **THEN** planning MUST fail with safe resource, field, and state context

#### Scenario: Remove unsupported scalar field
- **WHEN** desired state explicitly requests a typed scalar removal
- **AND** the field policy marks removal as unsupported
- **THEN** the planner MUST fail with contextual information about the resource key, field, and state
