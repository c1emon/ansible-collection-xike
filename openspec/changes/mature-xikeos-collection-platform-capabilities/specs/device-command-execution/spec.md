## ADDED Requirements

### Requirement: Command module is read-only by default
The `xikeos_command` module SHALL be treated as the read-only operational command module and SHALL NOT enter configuration mode during default execution.

#### Scenario: Show command remains unchanged
- **WHEN** a playbook runs `xikeos_command` with read-only show commands
- **THEN** the module MUST execute the commands through the operational network command path
- **AND** it MUST return `changed: false`

#### Scenario: Configuration mode command is rejected by default
- **WHEN** a playbook runs `xikeos_command` with a command that would enter configuration mode
- **THEN** the module MUST reject the command unless unsafe mutating commands are explicitly allowed

### Requirement: Command module supports wait conditions
The `xikeos_command` module SHALL support wait-condition behavior consistent with Ansible network command modules.

#### Scenario: Wait condition succeeds
- **WHEN** `xikeos_command` is called with `wait_for` conditions that match command output within the configured retries and interval
- **THEN** the module MUST complete successfully
- **AND** it MUST return the command output

#### Scenario: Wait condition fails
- **WHEN** `xikeos_command` is called with `wait_for` conditions that do not match command output within the configured retries and interval
- **THEN** the module MUST fail with failed condition details

### Requirement: Config fallback remains explicit
The `xikeos_config` module SHALL remain an explicit raw configuration fallback path rather than the preferred interface for modeled resources.

#### Scenario: Resource module exists for desired behavior
- **WHEN** a modeled resource module supports the requested resource behavior
- **THEN** documentation MUST prefer the modeled resource module over raw `xikeos_config`

#### Scenario: Save behavior is not implicit
- **WHEN** `xikeos_config` applies configuration commands without an explicit save option
- **THEN** it MUST NOT issue save or write commands
