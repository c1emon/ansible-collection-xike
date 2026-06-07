## MODIFIED Requirements

### Requirement: Resource modules gather current device state
Reference resource modules SHALL gather current device state from the target device before computing changes.

#### Scenario: VLAN module gathers before state
- **WHEN** `xikeos_vlans` runs against a device
- **THEN** it MUST collect VLAN state from device show-command output and expose the normalized state as `before`.

#### Scenario: VLAN current-state gathering preserves normalized parser contract
- **WHEN** `xikeos_vlans` gathers current state from `show vlan brief` output parsed through the internal TTP template path
- **THEN** it MUST receive the same normalized VLAN fields required for idempotent diffing, including integer VLAN IDs, names, states, and port lists.
