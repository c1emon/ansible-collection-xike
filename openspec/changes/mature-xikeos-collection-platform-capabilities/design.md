## Context

`c1emon.xikeos` is the collection-level platform layer for XikeOS/SKS8300. It already contains the foundations expected from an Ansible network collection: terminal and cliconf plugins, command/config modules, resource modules, facts parser utilities, and lifecycle helpers.

The remaining problem is contract maturity. Downstream iaas code still needs local parser, render, diff, report-preparation, and generic safety logic because collection outputs are not yet standardized around the conventions used by mainstream Ansible network collections.

The desired direction is:

```text
┌──────────────────────────────────────┐
│ iaas                                 │
│                                      │
│ intent data                          │
│ inventory / credentials              │
│ approval gates                       │
│ allowed operations                   │
│ topology-specific safety rules       │
│ reports / exports                    │
└───────────────────▲──────────────────┘
                    │ consumes stable contracts
┌───────────────────┴──────────────────┐
│ c1emon.xikeos                         │
│                                      │
│ network_cli platform behavior         │
│ facts aggregation                     │
│ parser ownership                      │
│ resource lifecycle                    │
│ command rendering                     │
│ generic redaction / command safety    │
└──────────────────────────────────────┘
```

The contract should look familiar to users of `cisco.ios`, `arista.eos`, and `junipernetworks.junos` rather than inventing XikeOS-specific return structures.

## Goals / Non-Goals

**Goals:**

- Adopt mainstream Ansible network facts and resource return conventions.
- Introduce or formalize `xikeos_facts` as the facts aggregation entrypoint.
- Return device/system facts as `ansible_net_*` keys.
- Return resource facts under `ansible_network_resources`.
- Keep `before`, `after`, `gathered`, and `parsed` schema-compatible with the related resource module `config` argument.
- Keep `commands` and `rendered` as ordered XikeOS CLI string lists.
- Define which modules are core lifecycle targets and which remain specialty/future maturity targets.
- Define collection-level generic safety/redaction behavior without replacing iaas governance.
- Preserve `ansible.netcommon.network_cli` as the primary connection path.

**Non-Goals:**

- Complete every specialty resource module lifecycle state in this change.
- Build a full firmware capability registry for all future XikeOS models and versions.
- Move iaas-local policy, approval, topology, inventory, credentials, reporting, or export logic into the collection.
- Add management/security configuration resource modules.
- Force immediate iaas parser deletion before facts schema equivalence is validated.

## Decisions

### Decision 1: Use mainstream facts contract

`xikeos_facts` will expose two layers of facts:

```yaml
ansible_facts:
  ansible_net_hostname: switch01
  ansible_net_model: SKS8300
  ansible_net_version: V300SP10240912
  ansible_net_serialnum: "..."
  ansible_net_image: "..."
  ansible_net_api: cliconf
  ansible_net_gather_subset:
    - min
    - hardware
  ansible_net_gather_network_resources:
    - interfaces
    - vlans
    - l2_interfaces
  ansible_network_resources:
    interfaces:
      - name: ethernet 1/0/1
        description: uplink
        enabled: true
    vlans:
      - vlan_id: 10
        name: servers
        state: active
    l2_interfaces:
      - name: ethernet 1/0/1
        mode: access
        access:
          vlan: 10
```

Rationale: `ansible_net_*` and `ansible_network_resources` match the model used by mature network collections and allow iaas to consume facts without learning a private XikeOS-only convention.

Alternative rejected: expose only custom `xikeos_*` facts. That would be simpler locally but would make the collection less idiomatic and harder to consume by Ansible users.

Priority: `xikeos_facts` is the first P1 implementation priority for this change because it is the main blocker for iaas to reduce local facts/parser code.

### Decision 2: Separate `gather_subset` from `gather_network_resources`

`gather_subset` is for device/system facts, while `gather_network_resources` is for resource-shaped facts.

```yaml
gather_subset:
  - min
  - hardware
  - config

gather_network_resources:
  - interfaces
  - vlans
  - l2_interfaces
  - l3_interfaces
  - lag_interfaces
  - static_routes
  - acls
```

Rationale: This follows modern Ansible network collection behavior and avoids overloading `gather_subset` with resource module names.

Compatibility note: the implementation may support aliases such as `device` for user ergonomics, but the documented contract should prefer mainstream names.

Accepted: this separation is the official facts selection model for the collection.

### Decision 3: Resource facts and resource returns are config-compatible

For each resource module, these values must share the same structured schema as the module's `config` argument:

- `before`
- `after`
- `gathered`
- `parsed`
- `ansible_network_resources.<resource>`

These values must be usable by callers as normalized resource data, not as device-native text.

Rationale: schema compatibility lets iaas compare desired intent against gathered state and lets users round-trip resource data through facts, rendered output, and resource modules.

Read-only observed fields may be included when documented, such as operational state or counters, but configurable fields must keep the same names, nesting, and value types as the `config` schema. Read-only additions must not prevent callers from deriving a valid config-compatible resource item from gathered data.

### Decision 4: CLI output fields are ordered string lists

The fields below are ordered XikeOS CLI command strings:

- `commands`: commands actually applied, or planned in check mode.
- `rendered`: offline generated native CLI from structured config.

Rationale: this matches mainstream resource module return contracts and keeps report generation straightforward.

### Decision 5: Define maturity tiers instead of requiring every module at once

Core lifecycle targets:

- `xikeos_vlans`
- `xikeos_interfaces`
- `xikeos_l2_interfaces`
- `xikeos_l3_interfaces`
- `xikeos_lag_interfaces`
- `xikeos_static_routes`
- `xikeos_acls`

Specialty/future maturity targets:

- `xikeos_stp`
- `xikeos_mirror`
- `xikeos_qinq`
- `xikeos_erps`
- `xikeos_eaps`
- `xikeos_port_isolate`
- `xikeos_flex_monitor_link`
- `xikeos_ospfv2`

P1 core state expectations:

- `gathered`
- `rendered`
- `merged`
- `replaced`
- `deleted`

P2 alignment states:

- `parsed`
- `overridden`
- `purged`, only where deleting the resource object itself is meaningful.

Rationale: core modules map directly to iaas parser/render/diff reduction. Specialty modules can mature later without blocking the stable platform contract.

### Decision 6: `xikeos_command` remains read-only by default

`xikeos_command` should not enter configuration mode and should reject known mutating/destructive commands unless an explicitly unsafe override is set.

Examples of guarded prefixes include:

- `config`
- `configure`
- `write`
- `copy`
- `reload`
- `delete`
- `erase`
- `format`
- `reset`

The override should be intentionally named to signal danger, for example `unsafe_allow_mutating_commands`.

Rationale: this preserves `xikeos_command` as a safe read-only facts/smoke-test foundation while still allowing controlled break-glass usage if necessary.

Accepted: default command execution must block mutating commands.

### Decision 7: Raw running config is opt-in and redacted by default

Facts and config-related returns should avoid exposing raw running configuration unless explicitly requested. When returned, raw config should be redacted by default.

Rationale: collection-level redaction provides a generic first layer of defense while iaas remains responsible for local report/export policy.

### Decision 8: `network_cli` is the only forward path

The supported platform path remains:

```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: c1emon.xikeos.xikeos
```

Legacy connection compatibility is not a forward-compatibility goal for this change. Documentation should present only the `network_cli` path, and implementation may remove the legacy XikeOS connection compatibility plugin after verifying tests and runtime metadata do not depend on it.

Rationale: this matches Ansible network collection norms and keeps terminal/cliconf behavior collection-owned.

### Decision 9: Default facts gathering is conservative

By default, `xikeos_facts` should gather only the minimum device facts and no network resources:

```yaml
gather_subset:
  - min
gather_network_resources: []
```

Rationale: default facts gathering should be fast, safe, and avoid surprising command volume. Callers can explicitly request hardware, config, or resource facts.

### Decision 10: Raw configuration is never unredacted by default

`gather_subset: [config]` may return running configuration, but the returned configuration must be redacted by default. Unredacted sensitive configuration must require an explicitly unsafe option if it is supported at all.

Rationale: running configuration can contain credentials and operational secrets. The collection provides a generic safety layer; iaas remains responsible for local report/export governance.

## Risks / Trade-offs

- Facts schema drift → Mitigation: define stable field-level schemas and golden SKS8300 outputs before iaas deletes local parser compatibility.
- Over-scoping the change → Mitigation: keep specialty modules, full capability registry, and management/security modules out of the initial implementation scope.
- `overridden` or `purged` causing unexpected removal → Mitigation: treat these as P2 states and require explicit module-level semantics before enabling.
- Redaction hiding useful report details → Mitigation: use selective redaction instead of blanket `no_log` for non-secret output; reserve `no_log` for secret input fields.
- Existing consumers relying on legacy connection behavior → Mitigation: document the compatibility/deprecation boundary and keep `network_cli` examples as the primary path.
- Parser inconsistency between resource modules and `xikeos_facts` → Mitigation: implement `xikeos_facts` as a thin aggregation layer over existing per-resource parsers instead of duplicating parser logic.

## Migration Plan

1. Define the facts and resource schemas without removing existing iaas compatibility paths.
2. Add or formalize `xikeos_facts` as an aggregation layer over existing parser utilities.
3. Validate `ansible_network_resources` output against golden SKS8300 samples.
4. Audit core resource modules against the standard return contract and document unsupported states explicitly.
5. Add generic command safety and redaction behavior in the collection.
6. Update documentation with migration examples for iaas:
   - replace local `switch_facts` consumers with `xikeos_facts`
   - consume `ansible_network_resources`
   - consume `before` / `after` / `commands` from resource modules
7. Allow iaas to delete local parser/render/diff compatibility only after schema equivalence is verified.

Rollback strategy: because this change is additive and contract-standardizing, rollback should preserve existing modules and avoid deleting compatibility paths until downstream iaas migration is complete.

## Open Questions

- Which exact `ansible_net_*` keys are mandatory for SKS8300 when data is missing or unavailable?
- Should `gather_subset: [all]` include raw config, or should raw config always require explicit `config` plus redaction behavior?
- Which core modules should support `deleted` in P1 versus only `merged`/`replaced`/`rendered` initially?
- Should `parsed` be included in P1 for modules that already have strong parser coverage, or kept uniformly P2?
- What exact field-level schemas should be used for P1 resources, especially XikeOS hybrid L2 interface semantics?
- For each mutating module, should `after` be gathered from the device after apply or simulated from `before` plus planned commands when post-gather is unavailable?
- Should `gather_subset: [all]` exclude raw config by default, with config requiring explicit `config` selection?
