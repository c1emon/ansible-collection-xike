## Why

`c1emon.xikeos` already contains platform plugins, command/config modules, parser helpers, lifecycle helpers, and multiple resource modules, but downstream iaas code still needs local facts parsing, rendering, diff preparation, and safety handling because the collection does not yet expose a stable mainstream Ansible network collection contract.

This change standardizes the collection around the conventions used by widely adopted network collections such as `cisco.ios`, `arista.eos`, and `junipernetworks.junos`, so iaas can gradually depend on the collection for XikeOS platform behavior while retaining local intent, approval, topology, and reporting policy.

## What Changes

- Add `xikeos_facts` as the collection-owned facts aggregation entrypoint.
- Return device/system facts through standard `ansible_net_*` keys.
- Return resource facts through `ansible_network_resources` using schemas compatible with each resource module's `config` argument.
- Standardize core resource module return contracts around mainstream network resource module keys:
  - `before`
  - `after`
  - `commands`
  - `gathered`
  - `rendered`
  - `parsed`
- Distinguish device/system collection through `gather_subset` from resource collection through `gather_network_resources`.
- Define core module maturity expectations separately from specialty module future maturity.
- Add a collection-level command safety and redaction contract for generic destructive command blocking and sensitive output handling.
- Clarify that `ansible.netcommon.network_cli` with `ansible_network_os: c1emon.xikeos.xikeos` remains the primary supported connection path.
- Document iaas migration expectations for consuming facts, resource returns, and safety behavior.

Non-goals:

- Implement all P2/P3 specialty modules to full lifecycle maturity in one batch.
- Build a complete multi-model, multi-firmware capability registry.
- Add management/security configuration modules such as AAA, RADIUS/TACACS, SNMP, NTP, DNS, timezone, or local users.
- Move iaas-local inventory, credentials, approval gates, allowed operations, topology-specific safety rules, reports, exports, or OpenSpec workflows into the collection.
- Remove iaas orchestration roles or force immediate deletion of iaas compatibility parsers.

## Capabilities

### New Capabilities

- `xikeos-facts`: Defines the `xikeos_facts` aggregation module, `ansible_net_*` device facts, `gather_subset`, `gather_network_resources`, and `ansible_network_resources` resource facts contract.
- `xikeos-command-safety`: Defines generic collection-level destructive command detection, unsafe override behavior, sensitive field metadata, and redaction requirements for command/config/facts outputs.

### Modified Capabilities

- `resource-module-lifecycle`: Align core resource module states and return keys with mainstream Ansible network resource module conventions, including schema compatibility between `config`, `before`, `after`, `gathered`, and `parsed`.
- `device-command-execution`: Extend command/config behavior expectations to include read-only command semantics, wait condition support, explicit save behavior, and safety hooks.
- `ansible-network-platform`: Clarify `network_cli` as the primary platform path and define the supported/deprecated boundary for legacy connection compatibility.

## Impact

- Affected collection entrypoints:
  - `plugins/modules/xikeos_facts.py` or equivalent facts module entrypoint
  - `plugins/modules/xikeos_command.py`
  - `plugins/modules/xikeos_config.py`
  - core resource modules such as `xikeos_vlans`, `xikeos_interfaces`, `xikeos_l2_interfaces`, `xikeos_l3_interfaces`, `xikeos_lag_interfaces`, `xikeos_static_routes`, and `xikeos_acls`
- Affected module utilities:
  - facts parser utilities
  - lifecycle helpers
  - future safety/redaction helpers
- Affected documentation:
  - inventory and platform setup examples
  - facts contract documentation
  - resource state support matrix
  - iaas migration guidance
- Downstream impact:
  - iaas can gradually replace local `switch_facts`, parser, render/diff, and generic safety helpers with collection-provided contracts while keeping local governance and topology policy.
