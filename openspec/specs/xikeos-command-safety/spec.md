# xikeos-command-safety Specification

## Purpose
TBD - created by archiving change mature-xikeos-collection-platform-capabilities. Update Purpose after archive.
## Requirements
### Requirement: Command module blocks mutating commands by default
The `xikeos_command` module SHALL reject known mutating or destructive commands unless the caller explicitly enables an unsafe override.

#### Scenario: Block reload command
- **WHEN** `xikeos_command` is called with `commands: ["reload"]`
- **AND** unsafe mutating commands are not explicitly allowed
- **THEN** the module MUST fail before sending the command to the device

#### Scenario: Block configuration entry command
- **WHEN** `xikeos_command` is called with a command that enters configuration mode
- **AND** unsafe mutating commands are not explicitly allowed
- **THEN** the module MUST fail before sending the command to the device

#### Scenario: Unsafe override allows guarded command
- **WHEN** `xikeos_command` is called with a guarded command
- **AND** the caller explicitly enables the unsafe mutating command override
- **THEN** the module MAY send the command through the operational command path
- **AND** the result MUST make the unsafe override visible in warnings or equivalent metadata

### Requirement: Command safety uses conservative command classification
The collection SHALL classify known destructive or mutating command prefixes conservatively for generic command safety.

#### Scenario: Known destructive command prefix is detected
- **WHEN** a command begins with a known destructive prefix such as `reload`, `delete`, `erase`, `format`, or `reset`
- **THEN** the safety check MUST classify the command as unsafe for default `xikeos_command` execution

#### Scenario: Known configuration command prefix is detected
- **WHEN** a command begins with a known mutating prefix such as `config`, `configure`, `write`, or `copy`
- **THEN** the safety check MUST classify the command as unsafe for default `xikeos_command` execution

### Requirement: Collection modules redact sensitive returned values
Collection modules SHALL redact known sensitive values before returning module results, facts, raw configuration, command output, or diff-like output.

#### Scenario: Redact sensitive running configuration content
- **WHEN** a module return contains known sensitive configuration content
- **THEN** the returned value MUST replace the sensitive portion with a redaction marker

#### Scenario: Preserve non-sensitive observability
- **WHEN** a module redacts sensitive values
- **THEN** it MUST preserve non-sensitive context such as command names, changed status, and non-secret resource fields where possible

### Requirement: Secret inputs use Ansible secret handling
Module options that accept secret values SHALL use Ansible secret-handling mechanisms such as `no_log` for those inputs.

#### Scenario: Secret option is provided
- **WHEN** a caller provides a module option classified as secret
- **THEN** the option value MUST be protected from logs using Ansible-supported secret handling

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
