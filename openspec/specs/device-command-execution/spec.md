## Purpose
Define how Xike OS command and config modules execute operational and configuration commands through the Ansible network connection.
## Requirements
### Requirement: Command module executes device commands
The `xikeos_command` module SHALL execute requested commands on the target Xike OS device through the Ansible network connection and return the resulting output.

#### Scenario: Show command returns stdout
- **WHEN** a playbook runs `xikeos_command` with one or more show commands
- **THEN** the module MUST execute each command on the network device and return `stdout` and `stdout_lines` entries corresponding to each command.

#### Scenario: Command failure fails the module
- **WHEN** the device reports an error for a requested command
- **THEN** the module MUST fail with the command and device error response included in the failure context.

#### Scenario: Transport command error is contextualized by module
- **WHEN** lower-level command execution raises a typed Xike OS command or connection error
- **THEN** `xikeos_command` MUST fail with command-module context instead of leaking an uncaught exception.

### Requirement: Config module applies configuration commands
The `xikeos_config` module SHALL apply configuration commands to the target Xike OS device through the Ansible network connection.

#### Scenario: Config commands are pushed
- **WHEN** a playbook runs `xikeos_config` with configuration lines
- **THEN** the module MUST send those lines to the device through cliconf and report the applied command list.

#### Scenario: Check mode does not modify device
- **WHEN** a playbook runs `xikeos_config` in check mode
- **THEN** the module MUST report the commands that would be sent and MUST NOT modify the device.

### Requirement: Config save behavior is explicit
The `xikeos_config` module SHALL expose save behavior only through an explicit module option and SHALL use the validated Xike OS save command for the supported device scope.

#### Scenario: Save requested after change
- **WHEN** configuration commands changed the device and save is requested
- **THEN** the module MUST run the validated save command and report that save was attempted.

#### Scenario: Save command is not validated
- **WHEN** the save command is not validated for the target support scope
- **THEN** implementation MUST keep the behavior documented as an open validation item or guard it behind a conservative option.

#### Scenario: Save fails after successful apply
- **WHEN** configuration commands are applied successfully and the explicit save command fails
- **THEN** the module MUST fail with `changed: true`, `saved: false`, the applied command context, and a message indicating configuration was applied but save failed.

### Requirement: Config apply failure preserves task context
The `xikeos_config` module SHALL convert lower-level configuration apply errors into contextual module failures.

#### Scenario: Config apply fails before save
- **WHEN** `xikeos_config` attempts to apply configuration lines and the lower-level config helper raises a typed Xike OS error
- **THEN** the module MUST fail with configuration-apply context and MUST NOT attempt the save command.

### Requirement: Resource modules use network configuration execution
Xike OS resource modules SHALL apply device configuration changes through the collection's Ansible network connection and cliconf configuration path.

#### Scenario: Resource module applies configuration commands
- **WHEN** a resource module has computed configuration commands for a mutating state and is not running in check mode
- **THEN** it MUST send those commands through the Xike OS network configuration path rather than executing them as local controller commands.

#### Scenario: Local process execution is not used for device configuration
- **WHEN** a resource module applies device configuration
- **THEN** it MUST NOT use local controller process execution APIs such as `module.run_command()` to send device configuration commands.

### Requirement: Resource modules use operational execution for facts
Xike OS resource modules and facts providers SHALL use the network operational command path for show commands and current-state collection.

#### Scenario: Facts provider gathers show command output
- **WHEN** a facts provider needs device operational output for parsing current state
- **THEN** it MUST execute the show command through the Ansible network connection and return or parse the network device output.

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
