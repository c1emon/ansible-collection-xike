## ADDED Requirements

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
