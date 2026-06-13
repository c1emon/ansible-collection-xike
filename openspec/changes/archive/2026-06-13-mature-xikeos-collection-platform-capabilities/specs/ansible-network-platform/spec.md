## ADDED Requirements

### Requirement: network_cli remains the primary platform path
The collection SHALL document `ansible.netcommon.network_cli` with `ansible_network_os: c1emon.xikeos.xikeos` as the primary supported XikeOS platform connection path.

#### Scenario: User follows platform documentation
- **WHEN** a user reads platform setup documentation
- **THEN** the primary inventory example MUST use `ansible_connection: ansible.netcommon.network_cli`
- **AND** it MUST use `ansible_network_os: c1emon.xikeos.xikeos`

### Requirement: Legacy connection compatibility is not a forward path
The collection SHALL NOT treat legacy XikeOS connection compatibility as a forward-compatibility requirement for this platform contract.

#### Scenario: User follows connection documentation
- **WHEN** users inspect collection documentation for connection options
- **THEN** the documentation MUST present `ansible.netcommon.network_cli` as the supported path
- **AND** it MUST NOT require users to select a legacy XikeOS connection plugin

#### Scenario: Legacy connection plugin is removed
- **WHEN** implementation removes a legacy XikeOS connection compatibility plugin
- **THEN** tests and runtime metadata MUST continue to support the documented `network_cli` platform path

### Requirement: Platform facts identify supported device scope
The collection SHALL document the validated platform scope for facts and lifecycle contracts, including model and firmware assumptions when known.

#### Scenario: SKS8300 firmware support is documented
- **WHEN** users read the support matrix
- **THEN** it MUST identify SKS8300 firmware versions that have been validated for platform, facts, and resource lifecycle behavior
