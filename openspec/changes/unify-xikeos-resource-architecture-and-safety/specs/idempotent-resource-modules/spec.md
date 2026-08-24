## ADDED Requirements

### Requirement: Omission-sensitive modules are tested through Ansible normalization
Resource modules whose semantics depend on omitted versus explicit fields SHALL be tested with parameters after the same Ansible argument validation/default insertion used at runtime.

#### Scenario: L3 replaced omits IPv6
- **WHEN** runtime-normalized L3 `replaced` input declares IPv4 and contains Ansible-inserted `ipv6: null`
- **THEN** the canonical desired state MUST omit IPv6
- **AND** no IPv6 removal command may be rendered

#### Scenario: LAG merged declares only members
- **WHEN** runtime-normalized LAG `merged` input declares only members and contains Ansible-inserted null scalar fields
- **THEN** the canonical desired state MUST omit those scalar fields
- **AND** planning MUST neither fail nor render scalar removals

### Requirement: Base and L2 interface replacement is truthful
Base-interface and L2-interface `replaced` SHALL synchronize explicitly declared owned fields on listed interfaces and preserve unlisted interfaces.

#### Scenario: Check-mode replacement lists one interface
- **WHEN** current state contains two interfaces and desired `replaced` lists one
- **THEN** planned commands MUST target only the listed interface
- **AND** simulated after-state MUST preserve the unlisted interface

#### Scenario: Omitted interface field
- **WHEN** a listed desired interface omits an optional field
- **THEN** replacement MUST preserve the current value of that field unless an explicit supported reset is requested

### Requirement: Static route reconciliation preserves route identity and distance
Static-route gathering and planning SHALL preserve composite route identity and administrative distance so identical and ECMP routes are idempotent.

#### Scenario: Cisco-style distance is parsed
- **WHEN** route output contains `[60/0]`
- **THEN** facts MUST report administrative distance `60`
- **AND** MUST NOT substitute the default distance `1`

#### Scenario: Identical replaced route
- **WHEN** desired and current static routes have the same route type, destination, normalized mask, next hop, and distance
- **AND** state is `replaced`
- **THEN** no delete or add command may be rendered

#### Scenario: Same prefix has multiple next hops
- **WHEN** current state contains multiple static routes for the same prefix with distinct next hops
- **THEN** gathering, planning, deletion, and after-state MUST preserve each route as a distinct identity

#### Scenario: Distance changes
- **WHEN** one listed route keeps its identity but changes administrative distance
- **THEN** the module MUST render the smallest evidence-admitted remove/add transition required by XikeOS
- **AND** it MUST fail before rendering when exact removal scope or add syntax has not been admitted

### Requirement: ACL reconciliation is ordered and idempotent
ACL planning SHALL model ACL identity and use exactly one evidence-admitted sequenced or positional rule model. Sequence and remark fields SHALL be owned only when their render and gather behavior is admitted.

#### Scenario: Sequenced ACL model is admitted
- **WHEN** evidence proves sequence values round-trip through render and gather behavior
- **THEN** sequence MUST be the rule identity and numeric sequence MUST define rule order
- **AND** duplicate sequence identities MUST fail before rendering

#### Scenario: Positional ACL model is admitted
- **WHEN** evidence proves gathered device order but does not prove sequence round-trip behavior
- **THEN** rule values and positions MUST define the ordered comparison
- **AND** non-empty sequence or unsupported remark input MUST fail explicitly
- **AND** changed rules MUST use only an evidence-admitted whole-ACL or granular transition

#### Scenario: Identical replaced ACL
- **WHEN** desired and current ACL type, supported remarks, rule identities, values, and order match
- **AND** state is `replaced`
- **THEN** the module MUST return an empty command list and `changed: false`

#### Scenario: Duplicate ACL sequence
- **WHEN** the sequenced model is active and desired rules contain duplicate sequence identities
- **THEN** planning MUST fail before rendering or deleting the ACL

#### Scenario: Accepted ACL field is not implemented
- **WHEN** a caller supplies a documented ACL field that the renderer cannot safely apply
- **THEN** the module MUST fail explicitly
- **AND** it MUST NOT silently ignore the field

### Requirement: VLAN replacement preserves unlisted VLANs
VLAN `replaced` SHALL synchronize explicitly declared fields for listed VLAN identities and preserve unlisted VLANs.

#### Scenario: Replaced lists one non-default VLAN
- **WHEN** current state contains multiple VLANs and desired `replaced` lists one VLAN
- **THEN** the module MUST NOT render deletion commands for unlisted VLANs

#### Scenario: Default VLAN deletion
- **WHEN** any supported state would require deleting VLAN 1
- **THEN** the module MUST fail before applying commands

## MODIFIED Requirements

### Requirement: All migrated resource modules provide truthful idempotent results
All core Xike OS resource modules SHALL compute `changed`, commands, and simulated after-state from one canonical resource plan and SHALL NOT report a change for semantically equivalent normalized state.

#### Scenario: Migrated module detects no change
- **WHEN** canonical desired state already matches gathered current state in `merged` or `replaced`
- **THEN** it MUST return `changed: false`, an empty command list, and stable before/after state
- **AND** it MUST NOT delete and recreate an equivalent resource

#### Scenario: Migrated module detects a change
- **WHEN** canonical desired state differs from gathered current state
- **THEN** it MUST return `changed: true`, include the minimal safe command list required to converge owned state, and apply those commands outside check mode

#### Scenario: Unlisted resource in replaced state
- **WHEN** desired `replaced` omits a current resource
- **THEN** the module MUST preserve that unlisted resource
- **AND** global removal MUST require a separately defined future state
