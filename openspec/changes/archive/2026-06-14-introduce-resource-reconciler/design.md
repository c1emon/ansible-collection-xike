## Context

The collection has a shared lifecycle helper, but individual resource modules still own their own diff algorithms, state semantics, simulated `after` data, and CLI rendering. This has caused inconsistent behavior: `xikeos_l3_interfaces state=merged` can remove existing IP addresses, and `xikeos_lag_interfaces state=merged` can remove existing trunk members. A larger generic diff library would not understand network resource ownership or XikeOS CLI semantics, so the safer approach is a small internal reconciler that plans normalized resource operations and leaves CLI rendering to each module.

## Goals / Non-Goals

**Goals:**

- Introduce a pure, unit-testable reconciler for normalized resource data.
- Support MVP field kinds needed by L3 and LAG: scalar fields and set fields.
- Emit semantic operations such as `set_field`, `add_item`, and `remove_item` instead of direct CLI strings.
- Generate deterministic simulated `after` state from operations, especially for check mode.
- Migrate L3 and LAG modules to non-destructive `merged` semantics and listed-resource `replaced` semantics.
- Preserve the existing `run_resource_module_lifecycle()` execution flow.

**Non-Goals:**

- Do not migrate VLAN, ACL, static routes, OSPF, L2, or base interface modules in this change.
- Do not implement `overridden` or global destructive replacement semantics.
- Do not use DeepDiff/dictdiffer as the command-planning engine.
- Do not generate CLI commands inside the generic reconciler.
- Do not introduce new runtime dependencies.

## Decisions

### Reconciler is a pure internal utility

Add an internal module such as `plugins/module_utils/network/xikeos/reconcile.py`. It will accept normalized current state, normalized desired state, a state name, and a resource policy. It will return operations and provide a helper to apply those operations to normalized current state.

The reconciler must not import AnsibleModule, call device connections, or render CLI. This keeps it easy to unit test and prevents it from becoming a second lifecycle framework.

### MVP supports only scalar and set fields

The MVP policy model should be intentionally small:

- `FieldPolicy(kind="scalar")` for fields like LAG `mode` and `lacp_mode`.
- `FieldPolicy(kind="set", identity=(...))` for fields like L3 `ipv4`/`ipv6` and LAG `members`.

Map/list fields are deferred because ordered ACL rules and richer nested structures need separate semantics.

### Operations are semantic, not CLI contexts

The reconciler MVP emits field-level operations:

- `set_field`
- `unset_field`
- `add_item`
- `remove_item`

Resource-level create/delete operations such as `ensure_resource_present` and
`ensure_resource_absent` are deferred until a module migration needs those
semantics.

It should not emit `replace`, `enter_context`, or `exit_context`. Replacement is a state-level behavior that expands into smaller operations. CLI contexts such as `interface eth-trunk 1` belong in module-specific renderers.

### State semantics are explicit and conservative

For this MVP:

- `merged` adds or updates explicitly declared desired fields and never removes current-only set items.
- `replaced` synchronizes explicitly declared fields for resources listed in desired and does not remove unlisted resources.
- `deleted` can be supported by the reconciler but is not required for L3/LAG migration because those modules do not currently expose `deleted`.
- `rendered` is an execution mode: modules may call the planner with empty or synthetic current data and then render operations without gathering from the device.

Omitted fields and explicit empty fields are different. Omitted means no-op. Explicit empty set in `replaced` means clear that owned set field if removal is supported.

### CLI rendering remains module-specific

Each migrated module should provide a renderer:

- L3 renderer groups operations by interface and emits `interface vlan-interface ...`, `ip address ...`, `no ip address ...`, `ipv6 address ...`, and `no ipv6 address ...`.
- LAG renderer groups operations by trunk and emits `interface eth-trunk ...`, `link-aggregation mode ...`, `lacp mode ...`, `no lacp mode`, and member add/remove commands.

Renderer-level validators may reject unsafe device-specific transitions such as mode changes that would leave stale LACP state unless the desired input explicitly handles them.

### Existing lifecycle helper remains in place

`run_resource_module_lifecycle()` already owns gather, check mode, apply, post-apply gather, and error handling. This change should replace module-local diff/after simulation with reconciler calls, not rewrite the lifecycle helper.

The planner may initially be called once for commands and once for `build_after_state`; this is acceptable for the MVP. A later change can introduce a plan object if duplication becomes a maintenance issue.

## Risks / Trade-offs

- **Risk:** The policy abstraction grows into a second schema that drifts from Ansible `argument_spec`. → **Mitigation:** MVP supports only scalar/set fields and policies live near module code or obvious module utility code.
- **Risk:** Generic planning generates unsafe removals. → **Mitigation:** Field policies include removal support, omitted fields are no-op, and unsupported removals fail fast.
- **Risk:** Simulated `after` diverges from actual device behavior. → **Mitigation:** Use simulated `after` for check mode and continue to prefer post-apply gather where modules already support it.
- **Risk:** LAG mode/LACP transitions have device-specific side effects. → **Mitigation:** Keep device-specific validators in the LAG module renderer path rather than hiding them in generic diff logic.
- **Risk:** Migration becomes too broad. → **Mitigation:** Only migrate L3 and LAG in this change; leave other modules untouched.

## Migration Plan

1. Add reconciler unit tests first for scalar/set planning, omitted-vs-empty behavior, unsupported removal, ordering, and simulated after-state.
2. Implement the internal reconciler MVP.
3. Add L3 policies, normalization helpers, operation rendering, and regression tests.
4. Migrate `xikeos_l3_interfaces` command and after-state generation to the reconciler.
5. Add LAG policies, member normalization, operation rendering, validator coverage, and regression tests.
6. Migrate `xikeos_lag_interfaces` command and after-state generation to the reconciler.
7. Run unit tests and verify unchanged modules are not impacted.

Rollback: revert the new utility and the L3/LAG module migrations. No persisted data migration is involved.

## Resolved Questions

- LAG `dynamic -> static` with existing `lacp_mode` preserves omitted `lacp_mode` as no-op. Users can explicitly set `lacp_mode: null` to render `no lacp mode`.
- `deleted` is deferred until a module migration requires it. L3 and LAG do not expose `deleted` in this MVP.
