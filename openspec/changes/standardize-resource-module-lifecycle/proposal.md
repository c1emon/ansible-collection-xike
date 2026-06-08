## Why

Current Xike OS resource modules follow the right Ansible Network Collection direction, but their runtime behavior is inconsistent: some modules gather and apply changes through the network connection, some only render planned commands, some use local command execution paths, and some facts providers silently return empty state. This creates unsafe idempotency, misleading `changed` results, and a risk that playbooks report success without modifying the device.

This change standardizes the resource-module lifecycle so declarative modules have a single, reliable contract for current-state gathering, diffing, check mode, device configuration, and after-state reporting.

## What Changes

- Define a shared resource-module lifecycle contract: validate input, gather `before`, normalize desired state, compute commands, honor check mode, apply through the Xike OS network connection, and gather/report `after`.
- Require configuration changes from resource modules to use the collection network execution path, not local process execution.
- Require facts failures to fail explicitly instead of silently returning empty state.
- Make `xikeos_vlans` the reference implementation for the lifecycle contract after tightening edge-case semantics.
- Migrate high-risk/high-value resource modules toward the lifecycle contract, especially static routes, ACLs, L2/L3 interfaces, base interfaces, and LAG interfaces.
- Define behavior for incomplete resource modules: either implement the lifecycle, expose explicitly non-mutating rendered behavior, or fail fast rather than reporting false device changes.
- Add validation and tests for idempotency, check mode, command application, facts failures, and prevention of local `module.run_command()` configuration paths.

## Capabilities

### New Capabilities
- `resource-module-lifecycle`: Defines the standard lifecycle and safety contract for Xike OS declarative resource modules.

### Modified Capabilities
- `idempotent-resource-modules`: Extends idempotency requirements beyond VLANs to require consistent lifecycle behavior, facts failure handling, check mode, and truthful `before`/`after` reporting across resource modules.
- `device-command-execution`: Clarifies that resource-module configuration changes must go through the Ansible network connection/cliconf path and must not use local command execution.

## Impact

- Affected modules: `xikeos_vlans`, `xikeos_static_routes`, `xikeos_acls`, `xikeos_interfaces`, `xikeos_l2_interfaces`, `xikeos_l3_interfaces`, `xikeos_lag_interfaces`, and specialty modules such as STP, ERPS, EAPS, QinQ, mirror, port isolation, flex monitor link, and OSPFv2.
- Affected utilities: `plugins/module_utils/network/xikeos/xikeos.py`, facts providers under `plugins/module_utils/facts/`, and any new shared lifecycle helper introduced under module utils.
- Affected tests: unit tests for command generation and parser behavior, plus new lifecycle tests for check mode, facts failure, command application, and idempotency.
- User-visible behavior: modules that previously reported planned changes without applying them may either apply changes correctly, expose an explicit rendered/non-mutating state, or fail fast until fully supported.
