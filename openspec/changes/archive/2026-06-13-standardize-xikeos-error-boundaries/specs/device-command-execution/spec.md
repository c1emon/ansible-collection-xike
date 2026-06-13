## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Config apply failure preserves task context
The `xikeos_config` module SHALL convert lower-level configuration apply errors into contextual module failures.

#### Scenario: Config apply fails before save
- **WHEN** `xikeos_config` attempts to apply configuration lines and the lower-level config helper raises a typed Xike OS error
- **THEN** the module MUST fail with configuration-apply context and MUST NOT attempt the save command.
