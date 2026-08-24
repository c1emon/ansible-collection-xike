## ADDED Requirements

### Requirement: Changed resource mutations are evidence-admitted
Before a core resource migration introduces or semantically alters a mutating command transition, the collection SHALL admit the exact transition from a manually reviewed authoritative source excerpt or a captured device transcript with model and firmware context.

#### Scenario: Resource transition changes command behavior
- **WHEN** implementation changes a positive command, removal command, CLI mode, command order, reset scope, or atomic replacement sequence
- **THEN** the evidence register MUST identify the semantic operation and its exact admitted render behavior
- **AND** it MUST identify the gather output or other bounded observation used to verify convergence

#### Scenario: Existing renderer is refactored without command changes
- **WHEN** implementation preserves a pre-existing command sequence byte-for-byte while changing only planning or lifecycle structure
- **THEN** software regression evidence MAY establish preservation of existing behavior
- **AND** it MUST NOT upgrade that behavior to a physical compatibility claim

#### Scenario: Mutation evidence is insufficient
- **WHEN** a requested mutating or check-mode transition lacks admitted positive, removal, mode, ordering, or verification behavior
- **THEN** the module MUST fail before returning or applying mutation commands
- **AND** it MAY retain separately documented `state=rendered` preview behavior as software-only, non-device evidence

### Requirement: Converted manual text is not implicitly authoritative
Automatically converted manual chapters SHALL NOT become implementation evidence merely because they contain plausible XikeOS-like syntax.

#### Scenario: Unreviewed converted chapter contains a command
- **WHEN** a command appears outside the manually reviewed reference section of `docs/manual_zh.md`
- **THEN** the command MUST remain unadmitted until the relevant source excerpt is manually reconciled or a device transcript confirms it
- **AND** source code, parser fixtures, and unit tests alone MUST NOT satisfy mutation admission
