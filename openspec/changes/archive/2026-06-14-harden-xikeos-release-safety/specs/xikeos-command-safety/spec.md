## ADDED Requirements

### Requirement: Check mode does not execute unsafe mutating commands
The `xikeos_command` module SHALL NOT send known mutating or destructive commands to the device while Ansible check mode is active, even when the caller explicitly enables the unsafe mutating command override.

#### Scenario: Unsafe override in check mode does not send command
- **WHEN** `xikeos_command` is called in check mode with a guarded mutating command
- **AND** unsafe mutating commands are explicitly allowed
- **THEN** the module MUST NOT call the network command execution path for that guarded command
- **AND** the result MUST include the planned command context for operator visibility

#### Scenario: Read-only command in check mode remains allowed
- **WHEN** `xikeos_command` is called in check mode with a read-only show command
- **THEN** the module MAY execute the read-only operational command through the network command path
- **AND** it MUST continue to report `changed: false`
