# iaas Migration Guidance

This collection owns XikeOS platform behavior, parser contracts, resource lifecycle helpers, generic command safety, and generic redaction. iaas should continue to own intent, inventory, credentials, approval gates, allowed operations, topology constraints, reports, exports, and OpenSpec workflow.

## Replace local switch_facts consumers

Use `c1emon.xikeos.xikeos_facts` for device facts:

```yaml
- name: Gather XikeOS device facts
  c1emon.xikeos.xikeos_facts:
    gather_subset:
      - min
```

Read standard facts from `ansible_facts.ansible_net_*`, including hostname, model, version, serial, image, API, gathered subsets, and gathered network resources.

## Consume resource state

Request resource facts explicitly:

```yaml
- name: Gather resource facts
  c1emon.xikeos.xikeos_facts:
    gather_network_resources:
      - interfaces
      - vlans
      - l2_interfaces
```

Consume resource data from `ansible_facts.ansible_network_resources.<resource>`. The configurable fields are schema-compatible with the corresponding resource module `config` item, so iaas can compare desired intent with gathered state without local parser-specific adapters.

## Consume lifecycle reports

For modeled resource modules, reports should use `before`, `after`, `commands`, `gathered`, and `rendered` where exposed.

## Keep local iaas responsibilities

iaas remains responsible for inventory, credentials, approval gates, operation authorization, topology-specific safety rules, reports, exports, local allowed-operation policy, and OpenSpec workflow.

## Compatibility parser deletion criteria

Do not delete iaas local compatibility parsers until all of the following are true:

1. Golden SKS8300 outputs for the relevant facts/resource areas are covered in collection tests.
2. `ansible_network_resources.<resource>` output is equivalent to iaas' required normalized state for the fields iaas consumes.
3. Resource module `before`, `after`, and `commands` produce the data needed by iaas reports.
4. Redaction behavior preserves required observability while hiding secrets.
5. Any topology-specific policy remains implemented in iaas rather than assumed by the collection.
