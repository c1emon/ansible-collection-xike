## ADDED Requirements

### Requirement: Command module executes device commands
The `xikeos_command` module SHALL execute requested commands on the target Xike OS device through the Ansible network connection and return the resulting output.

#### Scenario: Show command returns stdout
- **WHEN** a playbook runs `xikeos_command` with one or more show commands
- **THEN** the module MUST execute each command on the network device and return `stdout` and `stdout_lines` entries corresponding to each command.

#### Scenario: Command failure fails the module
- **WHEN** the device reports an error for a requested command
- **THEN** the module MUST fail with the command and device error response included in the failure context.

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
