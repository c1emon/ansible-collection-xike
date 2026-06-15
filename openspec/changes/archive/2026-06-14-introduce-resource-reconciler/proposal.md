## Why

Several resource modules currently hard-code diff logic, state semantics, after-state simulation, and CLI rendering in each module, which has already produced inconsistent `merged`/`replaced` behavior for L3 and LAG resources. This change introduces a small internal reconciler so resource state planning is centralized, testable, and separated from XikeOS CLI rendering.

## What Changes

- Add a pure internal resource reconciliation utility for normalized resource data: `current + desired + state + policy -> operations`.
- Add operation-based simulated after-state support for check mode and command planning.
- Define a minimal MVP policy model for scalar and set fields only.
- Migrate `xikeos_l3_interfaces` to use the reconciler so `merged` adds desired IP addresses without removing existing addresses, while `replaced` synchronizes explicitly declared address fields for listed interfaces.
- Migrate `xikeos_lag_interfaces` to use the reconciler so `merged` adds desired members without removing existing members, while `replaced` synchronizes explicitly declared LAG fields for listed trunks.
- Keep CLI rendering module-specific: the reconciler emits operations, and each module renders those operations into XikeOS commands.
- Defer VLAN, ACL, static route, OSPF, L2, and base interface migration to later changes.

## Capabilities

### New Capabilities
- `resource-reconciliation-planning`: Internal pure planning contract for normalized resource state, operations, and simulated after-state.

### Modified Capabilities
- `resource-module-lifecycle`: lifecycle modules may use a common planner for command diff and check-mode after-state while preserving existing lifecycle execution flow.
- `idempotent-resource-modules`: L3 and LAG modules must use non-destructive `merged` semantics and listed-resource `replaced` semantics.

## Impact

- New internal module utility under `plugins/module_utils/network/xikeos/`.
- Affected modules: `plugins/modules/xikeos_l3_interfaces.py` and `plugins/modules/xikeos_lag_interfaces.py`.
- Affected tests: new reconciler unit tests plus L3/LAG command/lifecycle regression tests.
- No external dependencies are expected.
- No changes to Galaxy release workflow, command safety, OSPF facts execution, or legacy connection packaging; those remain in `harden-xikeos-release-safety`.
