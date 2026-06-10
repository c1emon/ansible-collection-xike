## MODIFIED Requirements

### Requirement: Resource modules gather current device state
Reference resource modules SHALL gather current device state from the target device before computing changes. Resource modules that require parser templates at runtime SHALL receive required template content through internal action-plugin injection so current-state gathering does not depend on non-Python template files being present inside the module payload.

#### Scenario: VLAN module gathers before state
- **WHEN** `xikeos_vlans` runs against a device
- **THEN** it MUST collect VLAN state from device show-command output and expose the normalized state as `before`.

#### Scenario: VLAN current-state gathering preserves normalized parser contract
- **WHEN** `xikeos_vlans` gathers current state from `show vlan` output parsed through the internal template path
- **THEN** it MUST receive the same normalized VLAN fields required for idempotent diffing, including integer VLAN IDs, names, states, VLAN types, media, and port lists.

#### Scenario: VLAN gathering works without template files in module payload
- **WHEN** `xikeos_vlans` runs from an Ansible module payload that does not include parser template data files
- **THEN** it MUST still gather VLAN state using template content injected by the action plugin.
