## 1. Baseline and Safety Checks

- [x] 1.1 Inventory resource modules and classify each as lifecycle-complete, rendered-only, or unsupported for mutating states.
- [x] 1.2 Add a test or static check that resource modules do not use `module.run_command()` for device configuration.
- [x] 1.3 Add lifecycle test helpers/mocks for network `run_commands()` and `load_config()` calls.

## 2. Reference VLAN Lifecycle

- [x] 2.1 Tighten `xikeos_vlans` state semantics for `merged`, `replaced`, `deleted`, and `gathered`.
- [x] 2.2 Define explicit behavior for VLAN `active`/`suspend` and unsupported VLAN edge cases.
- [x] 2.3 Ensure VLAN check mode computes commands and `changed` before exiting without applying config.
- [x] 2.4 Ensure VLAN changed executions apply through `load_config()` and report normalized `before`/`after`.
- [x] 2.5 Add VLAN tests for no-op idempotency, changed path, check mode, facts failure, and edge-case behavior.

## 3. Fix High-Risk Execution Paths

- [x] 3.1 Update `xikeos_static_routes` to compute commands before check-mode exit and apply through `load_config()` outside check mode.
- [x] 3.2 Update `xikeos_static_routes` facts handling so gather failures fail explicitly instead of returning empty state silently.
- [x] 3.3 Update `xikeos_acls` to apply configuration through `load_config()` outside check mode.
- [x] 3.4 Update `xikeos_acls` facts handling so gather or parse failures fail explicitly when required for diffing.
- [x] 3.5 Add static-routes and ACL tests for command application, check mode, facts failure, and no local command execution.

## 4. Shared Lifecycle Helper

- [x] 4.1 Extract repeated lifecycle mechanics from the reference module into a small shared helper under module utils.
- [x] 4.2 Support common result fields: `changed`, `commands`, `before`, and `after`.
- [x] 4.3 Support mutating-state flow, check-mode flow, gathered/rendered flow where applicable, and fail-fast unsupported-state handling.
- [x] 4.4 Add unit tests for the shared lifecycle helper independent of individual resource modules.

## 5. Interface Resource Migration

- [x] 5.1 Implement or harden facts gathering for base interfaces using network operational/config retrieval paths.
- [x] 5.2 Migrate `xikeos_interfaces` to the standard lifecycle contract.
- [x] 5.3 Implement or harden L2 interface facts parsing from device output.
- [x] 5.4 Migrate `xikeos_l2_interfaces` to apply through the standard lifecycle contract.
- [x] 5.5 Implement or harden L3 interface facts parsing from device output.
- [x] 5.6 Migrate `xikeos_l3_interfaces` to apply through the standard lifecycle contract.
- [x] 5.7 Implement or harden LAG interface facts parsing from device output.
- [x] 5.8 Migrate `xikeos_lag_interfaces` to apply through the standard lifecycle contract.
- [x] 5.9 Add interface-family lifecycle tests for idempotency, changed path, check mode, and facts failure.

## 6. Specialty Module Classification

- [x] 6.1 Classify STP, ERPS, EAPS, QinQ, mirror, port isolation, flex monitor link, and OSPFv2 modules as lifecycle-complete, rendered-only, or unsupported for mutating states.
- [x] 6.2 For modules not ready to mutate safely, fail fast for mutating states or expose an explicit non-mutating `rendered` state.
- [x] 6.3 For modules ready to mutate, migrate them to the standard lifecycle contract.
- [x] 6.4 Add tests proving unsupported modules do not report false `changed: true` for unapplied commands.

## 7. Documentation and Validation

- [x] 7.1 Document the resource-module lifecycle contract for maintainers.
- [x] 7.2 Update module documentation to distinguish mutating states from non-mutating rendered/gathered behavior.
- [x] 7.3 Run the relevant unit test suite and Ansible sanity checks.
- [x] 7.4 Run OpenSpec validation for `standardize-resource-module-lifecycle`.
