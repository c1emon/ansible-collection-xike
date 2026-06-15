## 1. Reconciler MVP Tests

- [x] 1.1 Add unit tests for planner determinism, semantic operation output, and no CLI/device coupling.
- [x] 1.2 Add unit tests for scalar field `set_field` behavior and unsupported `unset_field` failure.
- [x] 1.3 Add unit tests for set field `add_item` and `remove_item` planning.
- [x] 1.4 Add unit tests proving `merged` does not remove current-only set items.
- [x] 1.5 Add unit tests proving `replaced` affects only listed resources and explicitly declared fields.
- [x] 1.6 Add unit tests for applying operations to normalized current state to produce simulated `after` state.

## 2. Reconciler MVP Implementation

- [x] 2.1 Add `plugins/module_utils/network/xikeos/reconcile.py` with `FieldPolicy`, `ResourcePolicy`, `Operation`, and reconciliation error types.
- [x] 2.2 Implement resource and set-item identity helpers for normalized resource data.
- [x] 2.3 Implement `plan_operations()` for `merged` and `replaced` scalar/set semantics.
- [x] 2.4 Implement fail-fast behavior for malformed policy/input and unsupported removals.
- [x] 2.5 Implement `apply_operations_to_state()` for deterministic simulated after-state.

## 3. L3 Interfaces Migration

- [x] 3.1 Add L3-specific normalization helpers and `L3_POLICY` for IPv4 and IPv6 set fields.
- [x] 3.2 Add L3 operation renderer tests for IPv4/IPv6 add and remove commands.
- [x] 3.3 Add L3 regression tests proving `merged` adds IPv4/IPv6 without removing existing addresses.
- [x] 3.4 Add L3 regression tests proving `replaced` syncs explicitly declared address fields and preserves unlisted interfaces/omitted fields.
- [x] 3.5 Update `xikeos_l3_interfaces` command and after-state builders to use the reconciler and L3 renderer.

## 4. LAG Interfaces Migration

- [x] 4.1 Add LAG-specific normalization helpers, member normalization, and `LAG_POLICY` for mode, lacp_mode, and members.
- [x] 4.2 Add LAG operation renderer tests for mode, lacp_mode, member add, and member remove commands.
- [x] 4.3 Add LAG regression tests proving `merged` adds members without removing existing members.
- [x] 4.4 Add LAG regression tests proving `replaced` syncs explicitly declared members, preserves unlisted trunks, and treats member order as idempotent.
- [x] 4.5 Add validator coverage for unsafe LAG mode/LACP transitions if the implementation chooses fail-fast behavior. (Not applicable; this implementation does not add transition-specific fail-fast validation.)
- [x] 4.6 Update `xikeos_lag_interfaces` command and after-state builders to use the reconciler and LAG renderer.

## 5. Verification

- [x] 5.1 Run targeted reconciler, L3, and LAG unit tests.
- [x] 5.2 Run the full unit test suite with `uv run pytest tests/unit`.
- [x] 5.3 Verify `xikeos_vlans`, `xikeos_acls`, `xikeos_static_routes`, OSPF, L2, and base interface modules are not modified by this change unless required for imports/tests.
- [x] 5.4 Run OpenSpec validation/status checks for this change before implementation is considered complete.
