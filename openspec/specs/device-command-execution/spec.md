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
