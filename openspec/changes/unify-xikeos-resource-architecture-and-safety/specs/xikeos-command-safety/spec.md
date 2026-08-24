## ADDED Requirements

### Requirement: Generic command input is one device command per item
The `xikeos_command` module SHALL accept only one device command per `commands` list item and SHALL reject input that can conceal additional commands from prefix classification.

#### Scenario: Command contains a newline
- **WHEN** a command item contains carriage-return or newline characters
- **THEN** the module MUST fail before network execution
- **AND** it MUST NOT classify only the first line and send the compound value

#### Scenario: Unsupported compound separator is present
- **WHEN** a command item contains a separator that the supported XikeOS CLI can use to execute another command
- **THEN** the module MUST fail before network execution unless the complete compound grammar is safely classified

### Requirement: Wait parameters fail before execution when invalid
The `xikeos_command` module SHALL validate retry and interval bounds before calling the network command path.

#### Scenario: Retry count is non-positive
- **WHEN** `retries` is zero or negative
- **THEN** the module MUST fail before executing commands

#### Scenario: Interval is negative
- **WHEN** `interval` is negative
- **THEN** the module MUST fail before executing commands

## MODIFIED Requirements

### Requirement: Command safety uses conservative command classification
The collection SHALL validate each command as a single command and classify known destructive or mutating prefixes conservatively before default `xikeos_command` execution.

#### Scenario: Known destructive command prefix is detected
- **WHEN** a single command begins with a known destructive prefix such as `reload`, `delete`, `erase`, `format`, or `reset`
- **THEN** the safety check MUST classify the command as unsafe for default execution

#### Scenario: Known configuration command prefix is detected
- **WHEN** a single command begins with a known mutating prefix such as `config`, `configure`, `write`, or `copy`
- **THEN** the safety check MUST classify the command as unsafe for default execution

#### Scenario: Command cannot be classified as one command
- **WHEN** validation cannot prove that a list item represents one command
- **THEN** the module MUST fail closed before network execution

### Requirement: Collection modules redact sensitive returned values
Collection modules SHALL apply shared recursive sanitization before returning success, check-mode, warning, or failure payloads containing commands, facts, raw configuration, command output, device responses, diff-like output, or exception detail.

#### Scenario: Common username credential syntax is returned
- **WHEN** returned text contains a username command with optional modifiers followed by password or secret material
- **THEN** the credential operand MUST be replaced with the redaction marker
- **AND** non-sensitive username and command context SHOULD remain visible

#### Scenario: Radius or TACACS host key is returned
- **WHEN** returned text contains a radius-server or tacacs-server host command followed by a key operand
- **THEN** the key value MUST be replaced with the redaction marker

#### Scenario: Config module returns commands or response
- **WHEN** `xikeos_config` returns planned/applied commands, device responses, or apply/save failure context
- **THEN** every nested returned value MUST pass through shared sanitization

#### Scenario: Command module returns unsafe override context
- **WHEN** `xikeos_command` returns or warns about commands allowed through the unsafe override
- **THEN** secret operands MUST be redacted even though the command structure remains visible

#### Scenario: Redact sensitive running configuration content
- **WHEN** a module return contains known sensitive configuration content
- **THEN** the returned value MUST replace every recognized sensitive operand with a redaction marker

#### Scenario: Preserve non-sensitive observability
- **WHEN** a module sanitizes sensitive values
- **THEN** it MUST preserve non-sensitive context such as command names, changed status, partial-change status, and non-secret resource fields where possible
