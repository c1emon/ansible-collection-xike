## Context

The collection already follows the correct high-level Ansible Network pattern: users select Xike OS through `ansible_connection: ansible.netcommon.network_cli` and `ansible_network_os: xike.xikeos.xikeos`; terminal/cliconf plugins provide CLI interaction; modules call collection module utilities to run operational commands or apply configuration.

The weak point is the resource-module layer. `xikeos_vlans` is close to a complete declarative lifecycle, but other resource modules diverge: some only build command lists, some do not call the device configuration path, some use `module.run_command()` which executes locally rather than through the network connection, and several facts providers either return empty data or swallow failures. This breaks the core declarative-resource promise that modules compare desired state against real current state and truthfully report whether the device changed.

## Goals / Non-Goals

**Goals:**
- Establish a mandatory lifecycle contract for resource modules.
- Route all resource-module configuration changes through the Xike OS network/cliconf execution path.
- Make facts collection trustworthy by failing explicitly when required state cannot be gathered.
- Use `xikeos_vlans` as the first reference module and migrate high-risk modules in priority order.
- Prevent modules from reporting `changed: true` for commands that were only planned but not applied, except in explicit non-mutating states such as `rendered` or check mode.
- Add test coverage that proves idempotency, check mode, command application, after-state reporting, and facts failure behavior.

**Non-Goals:**
- Rewriting terminal or cliconf architecture from scratch.
- Adding broad new resource-module features unrelated to lifecycle correctness.
- Guaranteeing every specialty module is fully production-ready in the first migration pass.
- Introducing a new connection plugin as the default path.

## Decisions

### Decision 1: Use the existing network module utility as the only device execution boundary

Resource modules will use `run_commands()` for show/operational commands and `load_config()` for configuration commands. They will not use `module.run_command()` for device configuration.

Alternative considered: allow each module to choose its own execution path. This preserves short-term flexibility but keeps the current inconsistency and makes testing harder.

### Decision 2: Define a shared lifecycle before expanding module count

The standard lifecycle is:

```text
validate input
    │
    ▼
gather before
    │
    ▼
normalize desired/current state
    │
    ▼
compute commands
    │
    ├── check mode: return changed/commands/before/after without applying
    │
    ▼
apply via load_config
    │
    ▼
gather after
```

Alternative considered: fix modules individually without shared lifecycle. That is faster for one or two modules but likely reproduces drift across the larger module set.

### Decision 3: Treat facts failure as unsafe, not empty

Facts providers required for diffing will fail the module when they cannot gather or parse required state. Returning empty current state is only valid when the device output was successfully gathered and parsed as truly empty.

Alternative considered: continue best-effort empty facts. This makes modules appear more tolerant but can produce destructive diffs and false idempotency.

### Decision 4: Support explicit non-mutating output through state semantics, not accidental behavior

If a module supports rendering planned commands without applying them, it should expose an explicit non-mutating state such as `rendered`. Mutating states such as `merged`, `replaced`, `overridden`, and `deleted` must either apply through `load_config()` or fail fast if unsupported.

Alternative considered: keep current planned-command behavior in mutating states. This is misleading because Ansible users expect mutating states to modify the device unless check mode is enabled.

### Decision 5: Migrate modules by risk tier

Migration priority:

```text
Tier 1: xikeos_vlans reference hardening
Tier 2: xikeos_static_routes, xikeos_acls
Tier 3: xikeos_interfaces, xikeos_l2_interfaces, xikeos_l3_interfaces, xikeos_lag_interfaces
Tier 4: xikeos_stp, xikeos_erps, xikeos_eaps, xikeos_qinq, xikeos_mirror,
        xikeos_port_isolate, xikeos_flex_monitor_link, xikeos_ospfv2
```

The first tiers remove the highest correctness risk: local command execution, fake after-state, and empty facts.

## Risks / Trade-offs

- [Risk] Some modules may temporarily become stricter and fail where they previously returned planned commands. → Mitigation: document unsupported lifecycle states clearly and offer explicit `rendered` behavior where command rendering is useful.
- [Risk] Full after-state gathering may add device round trips. → Mitigation: gather only when needed and keep parser/facts code efficient; accept correctness before optimization.
- [Risk] A shared lifecycle helper could become too abstract too early. → Mitigation: first harden VLAN as a concrete reference, then extract only repeated lifecycle mechanics.
- [Risk] Facts parser gaps may block resource-module migration. → Mitigation: prioritize minimal parser support needed for idempotent diffing and fail fast for unsupported resources.

## Migration Plan

1. Harden the `xikeos_vlans` lifecycle and document it as the reference behavior.
2. Add tests that encode the lifecycle contract and prevent local command execution for device config.
3. Fix `xikeos_static_routes` and `xikeos_acls` to use the network configuration path and to compute commands before check-mode exit.
4. Introduce a small shared lifecycle helper only after repeated patterns are clear.
5. Migrate interface-related modules to the helper and implement required facts/parsers.
6. Classify specialty modules as implemented, rendered-only, or fail-fast until fully supported.

Rollback is straightforward because the change is module-behavior scoped: individual modules can be reverted to the previous implementation if a migration introduces regressions, while keeping the specs as the target contract.

## Open Questions

- Should all resource modules eventually support the full standard network-resource state set: `gathered`, `parsed`, `rendered`, `merged`, `replaced`, `overridden`, and `deleted`?
- For modules with incomplete facts support, should initial implementation prefer `rendered` support or fail-fast only?
- Should `after` always be re-gathered from the device after apply, or can selected modules return a clearly documented simulated `after` for performance-sensitive cases?
