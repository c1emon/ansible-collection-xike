#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS facts aggregation module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from typing import Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_vlans import gather_vlans
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_interfaces import gather_interfaces
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_l2_interfaces import gather_l2_interfaces
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_l3_interfaces import gather_l3_interfaces
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_lag_interfaces import gather_lag_interfaces
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.static_routes import StaticRoutesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.acls import AclsFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import run_commands, get_config
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.safety import redact_text, redact_value


DOCUMENTATION = """
module: xikeos_facts
short_description: Collect Xike OS device and resource facts
version_added: "0.1.0"
description:
  - Aggregates Xike OS facts using mainstream Ansible network fact keys.
  - Device/system facts are returned under standard C(ansible_net_*) keys.
  - Resource facts are returned under C(ansible_network_resources).
options:
  gather_subset:
    description: Device/system fact subsets to gather. C(all) expands to C(min) and C(hardware); raw config requires explicit C(config).
    type: list
    elements: str
    default: ['min']
  gather_network_resources:
    description: Resource facts to gather. C(all) expands to all supported P1 resources.
    type: list
    elements: str
    default: []
author: clemon
"""

EXAMPLES = """
- name: Gather minimum facts
  c1emon.xikeos.xikeos_facts:

- name: Gather VLAN and interface resource facts
  c1emon.xikeos.xikeos_facts:
    gather_network_resources:
      - vlans
      - interfaces
"""

DEVICE_SUBSETS = ("min", "hardware", "config")
DEVICE_ALIASES = {"default": "min", "device": "min", "system": "min"}
RESOURCE_NAMES = ("interfaces", "vlans", "l2_interfaces", "l3_interfaces", "lag_interfaces", "static_routes", "acls")


def _normalize_selectors(values: list[str], aliases: dict[str, str], all_values: tuple[str, ...], include_config: bool = True) -> list[str]:
    normalized: list[str] = []
    for value in values or []:
        item = aliases.get(str(value).lower(), str(value).lower())
        if item == "all":
            expanded = list(all_values if include_config else tuple(v for v in all_values if v != "config"))
            for expanded_item in expanded:
                if expanded_item not in normalized:
                    normalized.append(expanded_item)
            continue
        if item not in normalized:
            normalized.append(item)
    return normalized


def _parse_show_version(output: str) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    patterns = {
        "ansible_net_hostname": r"(?:Hostname|System name)\s*[: ]\s*(\S+)",
        "ansible_net_model": r"(?:Model|Device model)\s*[: ]\s*(.+)$",
        "ansible_net_version": r"(?:Version|Software version)\s*[: ]\s*([^\s,]+)",
        "ansible_net_serialnum": r"(?:Serial(?: number)?|SN)\s*[: ]\s*(\S+)",
        "ansible_net_image": r"(?:Image|Boot image|System image)\s*[: ]\s*(\S+)",
    }
    uptime_hostname = re.search(r"^\s*(\S+)\s+uptime", output, re.I | re.M)
    if uptime_hostname:
        facts["ansible_net_hostname"] = uptime_hostname.group(1)
    for key, pattern in patterns.items():
        if key in facts:
            continue
        match = re.search(pattern, output, re.I | re.M)
        facts[key] = match.group(1).strip() if match else None
    facts["ansible_net_api"] = "cliconf"
    return facts


def gather_device_facts(module: AnsibleModule, subsets: list[str]) -> dict[str, Any]:
    """Gather minimum, hardware, and optional redacted config facts."""
    facts = {"ansible_net_api": "cliconf"}
    if "min" in subsets or "hardware" in subsets:
        try:
            stdout = run_commands(module, ["show version"], check_rc=True) or []
            facts.update(_parse_show_version(to_text(stdout[0] if stdout else "", errors="surrogate_or_strict")))
        except Exception as exc:
            module.fail_json(msg="failed to gather minimum device facts: {0}".format(to_text(exc)))
            return {}
    if "config" in subsets:
        facts["ansible_net_config"] = redact_text(get_config(module, source="running"))
    facts["ansible_net_gather_subset"] = subsets # type: ignore
    return facts


def _dict_values_with_names(value: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name, fields in sorted(value.items()):
        item = dict(fields)
        item.setdefault("name", name)
        items.append(item)
    return items


def gather_resource_facts(module: AnsibleModule, resources: list[str]) -> dict[str, Any]:
    """Gather resource facts by reusing collection parser/module contracts."""
    gathered: dict[str, Any] = {}
    for resource in resources:
        if resource == "vlans":
            gathered[resource] = gather_vlans(module)
        elif resource == "interfaces":
            gathered[resource] = _dict_values_with_names(gather_interfaces(module))
        elif resource == "l2_interfaces":
            gathered[resource] = _dict_values_with_names(gather_l2_interfaces(module))
        elif resource == "l3_interfaces":
            gathered[resource] = _dict_values_with_names(gather_l3_interfaces(module))
        elif resource == "lag_interfaces":
            gathered[resource] = _dict_values_with_names(gather_lag_interfaces(module))
        elif resource == "static_routes":
            gathered[resource] = StaticRoutesFacts(module).facts.get("static_routes", [])
        elif resource == "acls":
            gathered[resource] = AclsFacts(module).facts.get("acls", [])
    return gathered


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            gather_subset=dict(type="list", elements="str", default=["min"]),
            gather_network_resources=dict(type="list", elements="str", default=[]),
            _textfsm_templates=dict(type="dict", required=False),
        ),
        supports_check_mode=True,
    )

    subsets = _normalize_selectors(module.params.get("gather_subset") or ["min"], DEVICE_ALIASES, DEVICE_SUBSETS, include_config=False)
    resources = _normalize_selectors(module.params.get("gather_network_resources") or [], {}, RESOURCE_NAMES)
    invalid_subsets = [item for item in subsets if item not in DEVICE_SUBSETS]
    invalid_resources = [item for item in resources if item not in RESOURCE_NAMES]
    if invalid_subsets or invalid_resources:
        module.fail_json(msg="unsupported facts selector", invalid_subsets=invalid_subsets, invalid_resources=invalid_resources)
        return

    ansible_facts = gather_device_facts(module, subsets)
    ansible_facts["ansible_net_gather_network_resources"] = resources
    if resources:
        ansible_facts["ansible_network_resources"] = gather_resource_facts(module, resources)
    module.exit_json(changed=False, ansible_facts=redact_value(ansible_facts))


if __name__ == "__main__":
    main()
