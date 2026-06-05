## Purpose
Define Xike OS as a standard Ansible Network platform using `ansible.netcommon.network_cli` with collection-owned terminal and cliconf plugins.

## Requirements

### Requirement: Standard network_cli platform selection
The collection SHALL support Xike OS as a standard Ansible Network platform selected with `ansible_connection: ansible.netcommon.network_cli` and `ansible_network_os: xike.xikeos.xikeos`.

#### Scenario: Inventory selects Xike OS platform
- **WHEN** a playbook targets a host with `ansible_connection` set to `ansible.netcommon.network_cli` and `ansible_network_os` set to `xike.xikeos.xikeos`
- **THEN** Ansible MUST resolve the Xike OS terminal and cliconf plugins from this collection.

#### Scenario: Documentation describes supported inventory
- **WHEN** a user reads collection setup documentation
- **THEN** the examples MUST show the `network_cli` inventory path and MUST NOT present `netconf` as the supported default connection.

### Requirement: Terminal plugin handles Xike OS CLI interaction
The collection SHALL provide a terminal plugin that recognizes supported Xike OS prompts, disables paging where possible, and detects command errors.

#### Scenario: Prompt recognition covers common modes
- **WHEN** the device prompt is user mode, privileged mode, global configuration mode, interface configuration mode, or another documented configuration sub-mode
- **THEN** the terminal plugin MUST recognize the prompt without hanging command execution.

#### Scenario: Command errors are detected
- **WHEN** the device returns an invalid, incomplete, ambiguous, or permission-denied command response
- **THEN** the terminal plugin MUST report the response as a command error to the calling module.

### Requirement: Cliconf plugin provides command and config operations
The collection SHALL provide a cliconf plugin that can execute operational commands, retrieve running configuration, edit configuration, expose device info, and report platform capabilities.

#### Scenario: Operational command execution through cliconf
- **WHEN** a module asks the connection to run an operational command
- **THEN** the cliconf plugin MUST send the command through the network connection and return device output.

#### Scenario: Configuration editing through cliconf
- **WHEN** a module asks the connection to apply configuration commands
- **THEN** the cliconf plugin MUST enter configuration mode, send commands in order, and exit configuration mode successfully.
