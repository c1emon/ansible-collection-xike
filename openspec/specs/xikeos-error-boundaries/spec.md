## Purpose
Define the collection-wide boundary where lower layers raise typed Xike OS errors and Ansible orchestration layers convert them into module failures.

## Requirements

### Requirement: Lower layers raise typed Xike OS errors
Collection-owned lower layers SHALL raise typed Xike OS exceptions instead of directly failing an Ansible module.

#### Scenario: Transport command execution fails
- **WHEN** a transport helper cannot execute a device command through the Ansible network connection
- **THEN** the helper MUST raise a typed Xike OS command or connection error that includes safe command context.

#### Scenario: Transport config application fails
- **WHEN** a transport helper cannot apply configuration through the Ansible network connection
- **THEN** the helper MUST raise a typed Xike OS config or connection error that includes safe command context.

#### Scenario: Facts parsing fails
- **WHEN** a collection-owned facts provider cannot parse required device output
- **THEN** the provider MUST raise a typed Xike OS facts or parse error instead of calling `module.fail_json`.

### Requirement: Ansible orchestration layers own module failures
Ansible module entrypoints, resource gather wrappers, and resource lifecycle helpers SHALL convert typed Xike OS errors into contextual `module.fail_json` responses.

#### Scenario: Module catches lower-layer error
- **WHEN** a module entrypoint catches a typed Xike OS error from a lower layer
- **THEN** it MUST fail the Ansible module with operation-specific context and any safe result fields relevant to the operation.

#### Scenario: Resource gather wrapper catches facts error
- **WHEN** a resource gather wrapper catches a typed Xike OS facts, parse, command, or connection error
- **THEN** it MUST fail with context identifying the resource facts gather operation that failed.

### Requirement: Failure payloads preserve redaction boundaries
Module failure payloads SHALL NOT expose sensitive command output or running configuration without applying collection redaction rules.

#### Scenario: Failure includes command output or config text
- **WHEN** a failure payload includes device output, running configuration, or exception text derived from those values
- **THEN** the payload MUST redact sensitive values before returning the module failure.

### Requirement: Optional parser dependencies keep friendly failures
Optional parser dependency failures SHALL remain user-friendly and MUST NOT be converted into import-time crashes during module documentation or Galaxy import.

#### Scenario: TextFSM or TTP is unavailable
- **WHEN** a facts parser requires TextFSM or TTP and the dependency is unavailable at runtime
- **THEN** the collection MUST report a friendly parser dependency failure without breaking ansible-doc or Galaxy import compatibility.
