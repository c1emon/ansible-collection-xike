# XikeOS Platform Contract

This collection follows mainstream Ansible network collection conventions for XikeOS/SKS8300 devices.

## Supported platform path

Use `ansible.netcommon.network_cli` with the collection cliconf plugin:

```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: c1emon.xikeos.xikeos
```

Legacy XikeOS-specific connection compatibility is not the forward path. Documentation and examples should prefer the `network_cli` platform path above.

Validated target scope is SKS8300-class XikeOS firmware, including version strings observed as `V300SP10240912`. Treat other models or firmware trains as compatible only after parser and lifecycle golden outputs are validated.

## Facts contract

`xikeos_facts` is the collection-owned facts aggregation entrypoint.

Minimum facts use standard Ansible network keys:

| Key | Source | Missing value behavior |
| --- | --- | --- |
| `ansible_net_hostname` | `show version` hostname/system-name/uptime formats | Returned as `null` when unavailable |
| `ansible_net_model` | `show version` model/device model | Returned as `null` when unavailable |
| `ansible_net_version` | `show version` software/version | Returned as `null` when unavailable |
| `ansible_net_serialnum` | `show version` serial/SN | Returned as `null` when unavailable |
| `ansible_net_image` | `show version` image/boot image | Returned as `null` when unavailable |
| `ansible_net_api` | collection platform | Always `cliconf` |
| `ansible_net_gather_subset` | normalized request | Returned as gathered subset list |
| `ansible_net_gather_network_resources` | normalized request | Returned as gathered resource list |

Supported `gather_subset` values: `min`, `hardware`, `config`, and `all`. `all` expands to `min` and `hardware`; raw config requires explicit `config`. Aliases `default`, `device`, and `system` normalize to `min`.

Default execution is conservative:

```yaml
gather_subset:
  - min
gather_network_resources: []
```

Supported `gather_network_resources` values are `interfaces`, `vlans`, `l2_interfaces`, `l3_interfaces`, `lag_interfaces`, `static_routes`, `acls`, and `all`.

Resource facts are returned under `ansible_facts.ansible_network_resources.<resource>` and reuse the same normalized schema as the corresponding resource module `config` item where configurable fields exist.

Raw running configuration is omitted unless `gather_subset: [config]` is explicitly requested. Returned raw config is redacted by default.

## Resource lifecycle contract

| Module | P1 states | Deleted semantics | `after` source |
| --- | --- | --- | --- |
| `xikeos_vlans` | `gathered`, `merged`, `replaced`, `deleted` | Delete requested VLANs; VLAN 1 is protected | Simulated unless post-gather is enabled |
| `xikeos_interfaces` | `merged`, `replaced` | Not exposed until safe interface reset semantics exist | Post-apply gathered |
| `xikeos_l2_interfaces` | `merged`, `replaced` | Not exposed until safe L2 default/reset semantics exist | Post-apply gathered |
| `xikeos_l3_interfaces` | `merged`, `replaced` | Not exposed until address deletion semantics are complete | Post-apply gathered |
| `xikeos_lag_interfaces` | `merged`, `replaced` | Not exposed until bundle/member deletion semantics are complete | Post-apply gathered |
| `xikeos_static_routes` | `merged`, `replaced`, `deleted` | Delete matching route entries | Post-apply gathered |
| `xikeos_acls` | `merged`, `replaced`, `deleted` | Delete matching ACL entries | Post-apply gathered |

`rendered` is the target non-mutating CLI rendering state for core modules. It is P1 where exposed and otherwise should be documented or rejected explicitly until implemented.

P2-only states are `parsed`, `overridden`, and `purged`. `parsed` requires documented offline parser input and must not connect to the device. `overridden` requires explicit unmanaged-configuration removal semantics per module. `purged` requires safe resource-object deletion semantics and is only meaningful for resource types that can safely remove whole objects.

All unsupported states must either be omitted from argument choices or fail fast. Modules must not silently report changes for unsupported behavior.

Schema rules:

- `before`, `after`, `gathered`, future `parsed`, and `ansible_network_resources.<resource>` use the module `config` item schema for configurable fields.
- Read-only observed fields may be present only when documented and must not change configurable field names, nesting, or value types.
- `commands` and `rendered` are ordered XikeOS CLI string lists.
- Required current-state parser failures are fail-fast because idempotent diffing would otherwise be unsafe.

## Command safety and redaction

`xikeos_command` is read-only by default. It blocks known mutating/destructive command prefixes unless `unsafe_allow_mutating_commands: true` is set.

Guarded prefixes include `config`, `configure`, `copy`, `delete`, `erase`, `format`, `reload`, `reset`, and `write`.

When the unsafe override is used, the module emits a warning so reports can identify break-glass execution.

Returned command output, facts, raw running configuration, and diff-like output should be redacted with `<redacted>` for known sensitive values while preserving non-sensitive context. Secret input fields, when added to modules, must use Ansible-supported secret handling such as `no_log`.

## Save/write behavior

`xikeos_config` is the explicit raw configuration fallback. It does not save/write by default; callers must request save behavior explicitly. Modeled resource modules apply device configuration but do not implicitly issue save/write commands.
