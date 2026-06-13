## 1. Contract Baseline

- [x] 1.1 Audit existing facts parser utilities and resource modules against the adopted mainstream facts/resource return contract.
- [x] 1.2 Define the required `ansible_net_*` keys for SKS8300 minimum facts, including behavior when a value is unavailable.
- [x] 1.3 Define the supported `gather_subset` values and aliases for device/system facts.
- [x] 1.4 Define the supported `gather_network_resources` values for core resource facts.
- [x] 1.5 Define the core module state support matrix for `gathered`, `rendered`, `merged`, `replaced`, and `deleted`.
- [x] 1.6 Document P2-only states such as `parsed`, `overridden`, and `purged` with module-level prerequisites.
- [x] 1.7 Define `all` semantics for `gather_subset` and `gather_network_resources`, including whether raw config is excluded from `all` by default.
- [x] 1.8 Define field-level P1 schemas for device facts, VLANs, interfaces, L2 interfaces, L3 interfaces, LAGs, static routes, and ACLs.
- [x] 1.9 Define module-specific `deleted` semantics for all P1 core modules.
- [x] 1.10 Define whether each core module's `after` state is post-apply gathered or simulated when post-gather is unavailable.
- [x] 1.11 Define parser failure behavior as fail-fast when required current-state parsing fails.

## 2. Facts Aggregation

- [x] 2.1 Add or formalize the `xikeos_facts` module argument model for `gather_subset` and `gather_network_resources`.
- [x] 2.2 Implement minimum device facts collection using standard `ansible_net_*` return keys.
- [x] 2.3 Implement `ansible_net_gather_subset` and `ansible_net_gather_network_resources` reporting.
- [x] 2.4 Map `gather_network_resources.interfaces` to the existing interfaces parser contract.
- [x] 2.5 Map `gather_network_resources.vlans` to the existing VLAN parser contract.
- [x] 2.6 Map `gather_network_resources.l2_interfaces` to the existing L2 interface parser contract.
- [x] 2.7 Map `gather_network_resources.l3_interfaces`, `lag_interfaces`, `static_routes`, and `acls` where parser support is available.
- [x] 2.8 Ensure `ansible_network_resources.<resource>` items use schemas compatible with the corresponding resource module `config` item.
- [x] 2.9 Ensure raw running configuration is omitted unless explicitly requested and redacted when returned.
- [x] 2.10 Ensure default `xikeos_facts` execution gathers only `min` device facts and no network resources.

## 3. Resource Return Contract

- [x] 3.1 Audit `xikeos_vlans` return values for `before`, `after`, `commands`, `gathered`, and `rendered` contract compliance.
- [x] 3.2 Audit `xikeos_interfaces` return values for contract compliance.
- [x] 3.3 Audit `xikeos_l2_interfaces` return values for contract compliance.
- [x] 3.4 Audit `xikeos_l3_interfaces` return values for contract compliance.
- [x] 3.5 Audit `xikeos_lag_interfaces` return values for contract compliance.
- [x] 3.6 Audit `xikeos_static_routes` return values for contract compliance.
- [x] 3.7 Audit `xikeos_acls` return values for contract compliance.
- [x] 3.8 Normalize `before`, `after`, `gathered`, and future `parsed` values to match each module's `config` schema.
- [x] 3.9 Normalize `commands` and `rendered` values as ordered XikeOS CLI string lists.
- [x] 3.10 Make unsupported states explicit through argument choices, fail-fast behavior, or documentation.

## 4. Command Safety and Redaction

- [x] 4.1 Define conservative mutating/destructive command patterns for generic command safety.
- [x] 4.2 Add default mutating command rejection behavior for `xikeos_command`.
- [x] 4.3 Add an intentionally unsafe override option for guarded `xikeos_command` execution.
- [x] 4.4 Add wait-condition behavior for `xikeos_command`, including `wait_for`, `match`, `retries`, and `interval`.
- [x] 4.5 Define sensitive field metadata and redaction markers for module returns.
- [x] 4.6 Redact sensitive values from raw running configuration, command output, facts, and diff-like outputs.
- [x] 4.7 Protect secret input fields using Ansible-supported secret handling.

## 5. Platform Foundation Documentation

- [x] 5.1 Document `ansible.netcommon.network_cli` with `ansible_network_os: c1emon.xikeos.xikeos` as the primary supported connection path.
- [x] 5.2 Remove or de-document the legacy XikeOS connection compatibility plugin after verifying the `network_cli` platform path remains intact.
- [x] 5.3 Document explicit save/write behavior for `xikeos_config` and resource modules.
- [x] 5.4 Document validated SKS8300 firmware assumptions for platform, facts, and lifecycle behavior.

## 6. Tests and Golden Data

- [x] 6.1 Add unit tests for `xikeos_facts` minimum device facts output.
- [x] 6.2 Add unit tests for `gather_network_resources` output under `ansible_network_resources`.
- [x] 6.3 Add golden SKS8300 output expectations for device, VLAN, interface, L2 interface, and other supported core resources.
- [x] 6.4 Add tests that verify resource facts are compatible with resource module `config` schemas.
- [x] 6.5 Add tests for `xikeos_command` mutating command blocking and unsafe override behavior.
- [x] 6.6 Add tests for redaction of sensitive values in returned output.
- [x] 6.7 Run existing unit tests and Ansible sanity checks relevant to the modified modules.

## 7. iaas Migration Guidance

- [x] 7.1 Document how iaas can replace local `switch_facts` consumers with `xikeos_facts`.
- [x] 7.2 Document how iaas should consume `ansible_network_resources` for resource state.
- [x] 7.3 Document how iaas should consume `before`, `after`, and `commands` for reports.
- [x] 7.4 Document which iaas responsibilities remain local: inventory, credentials, approval gates, allowed operations, topology constraints, reports, exports, and OpenSpec workflow.
- [x] 7.5 Document conditions that must be met before iaas deletes local compatibility parsers.
