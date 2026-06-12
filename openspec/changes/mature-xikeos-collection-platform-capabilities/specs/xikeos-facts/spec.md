## ADDED Requirements

### Requirement: Facts module exposes standard device facts
The collection SHALL provide `xikeos_facts` as the XikeOS facts aggregation entrypoint and SHALL return device and system facts using standard `ansible_net_*` keys.

#### Scenario: Gather minimum device facts
- **WHEN** `xikeos_facts` runs with `gather_subset` including `min`
- **THEN** the module MUST return `ansible_facts.ansible_net_hostname` when available
- **AND** it MUST return `ansible_facts.ansible_net_model` when available
- **AND** it MUST return `ansible_facts.ansible_net_version` when available
- **AND** it MUST return `ansible_facts.ansible_net_serialnum` when available
- **AND** it MUST return `ansible_facts.ansible_net_api`

#### Scenario: Report gathered device subsets
- **WHEN** `xikeos_facts` completes device facts gathering
- **THEN** the module MUST return `ansible_facts.ansible_net_gather_subset` with the normalized subset names that were gathered

### Requirement: Facts module defaults to minimum facts
The `xikeos_facts` module SHALL use conservative defaults that gather minimum device facts and no resource facts unless the caller requests more.

#### Scenario: Run facts with defaults
- **WHEN** `xikeos_facts` runs without explicit `gather_subset` or `gather_network_resources` arguments
- **THEN** it MUST gather the equivalent of `gather_subset: [min]`
- **AND** it MUST NOT gather network resources by default

### Requirement: Facts module separates device subsets from network resources
The `xikeos_facts` module SHALL use `gather_subset` for device/system facts and `gather_network_resources` for resource-shaped facts.

#### Scenario: Gather hardware without resource facts
- **WHEN** `xikeos_facts` runs with `gather_subset: [hardware]`
- **AND** no `gather_network_resources` value is requested
- **THEN** the module MUST gather hardware-related `ansible_net_*` facts
- **AND** it MUST NOT require resource parser output to succeed

#### Scenario: Gather resource facts through resource selector
- **WHEN** `xikeos_facts` runs with `gather_network_resources: [vlans]`
- **THEN** the module MUST gather VLAN resource facts under `ansible_facts.ansible_network_resources.vlans`
- **AND** it MUST include `vlans` in `ansible_facts.ansible_net_gather_network_resources`

### Requirement: Resource facts use ansible_network_resources
The `xikeos_facts` module SHALL return resource facts under `ansible_network_resources`, keyed by resource name.

#### Scenario: Gather multiple network resources
- **WHEN** `xikeos_facts` runs with `gather_network_resources: [interfaces, vlans, l2_interfaces]`
- **THEN** the result MUST include `ansible_facts.ansible_network_resources.interfaces`
- **AND** it MUST include `ansible_facts.ansible_network_resources.vlans`
- **AND** it MUST include `ansible_facts.ansible_network_resources.l2_interfaces`

#### Scenario: Resource facts use module-compatible schema
- **WHEN** `xikeos_facts` returns items under `ansible_network_resources.<resource>`
- **THEN** each returned item MUST use the same normalized schema as the corresponding resource module `config` item

### Requirement: Facts module reuses collection parser utilities
The `xikeos_facts` module SHALL gather resource facts by reusing collection-owned parser utilities rather than duplicating parser logic in the facts module.

#### Scenario: Gather VLAN resource facts
- **WHEN** `xikeos_facts` gathers VLAN resource facts
- **THEN** it MUST use the collection's VLAN parser contract for normalized VLAN fields
- **AND** it MUST NOT introduce a second incompatible VLAN schema

### Requirement: Facts module avoids raw running configuration by default
The `xikeos_facts` module SHALL NOT expose raw running configuration unless the caller explicitly requests configuration gathering.

#### Scenario: Gather facts without config subset
- **WHEN** `xikeos_facts` runs without requesting the `config` subset
- **THEN** the result MUST NOT include raw running configuration

#### Scenario: Gather configuration facts
- **WHEN** `xikeos_facts` runs with configuration gathering explicitly requested
- **THEN** returned configuration content MUST be redacted by default before it appears in module results

#### Scenario: Gather all device facts
- **WHEN** `xikeos_facts` runs with `gather_subset: [all]`
- **THEN** the module MUST NOT return unredacted raw running configuration by default
