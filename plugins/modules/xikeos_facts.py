#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS facts aggregation module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: xikeos_facts
short_description: Collect Xike OS device and resource facts
version_added: "0.1.0"
description:
  - Aggregates Xike OS facts using mainstream Ansible network fact keys.
  - Device/system facts are returned under standard C(ansible_net_*) keys.
  - Resource facts are returned under C(ansible_network_resources).
notes:
  - C(_textfsm_templates) is injected internally by the plugin/action chain and is not intended as a user-facing option.
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
  _textfsm_templates:
    description:
      - Internal action-plugin injection for bundled parser templates.
      - Do not set this option in playbooks.
    type: dict
author: "clemon (@c1emon)"
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

RETURN = """
ansible_facts:
  description: Collected device and resource facts, with sensitive values redacted.
  returned: always
  type: dict
  contains:
    ansible_net_api:
      description: Facts backend identifier used by this module.
      type: str
    ansible_net_hostname:
      description: Device hostname, when available.
      type: str
    ansible_net_model:
      description: Device model, when available.
      type: str
    ansible_net_version:
      description: OS version, when available.
      type: str
    ansible_net_serialnum:
      description: Device serial number, when available.
      type: str
    ansible_net_image:
      description: Boot/system image name, when available.
      type: str
    ansible_net_config:
      description: Redacted running configuration, when C(config) is requested.
      type: str
    ansible_net_gather_subset:
      description: Normalized device subset selectors used for the run.
      type: list
      elements: str
    ansible_net_gather_network_resources:
      description: Normalized resource selectors used for the run.
      type: list
      elements: str
    ansible_network_resources:
      description: Gathered resource facts keyed by resource name.
      type: dict
"""

import re
from typing import Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.acls import AclsFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.interfaces import InterfacesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.l2_interfaces import L2InterfacesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.l3_interfaces import L3InterfacesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.lag_interfaces import LagInterfacesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.static_routes import StaticRoutesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.vlans import parse_vlan
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.errors import XikeOSError, XikeOSFactsError
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.safety import redact_text, redact_value
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import get_config, run_commands

DEVICE_SUBSETS = ("min", "hardware", "config")
DEVICE_ALIASES = {"default": "min", "device": "min", "system": "min"}
RESOURCE_NAMES = (
    "interfaces",
    "vlans",
    "l2_interfaces",
    "l3_interfaces",
    "lag_interfaces",
    "static_routes",
    "acls",
)


def _normalize_selectors(
    values: list[str],
    aliases: dict[str, str],
    all_values: tuple[str, ...],
    include_config: bool = True,
) -> list[str]:
    normalized: list[str] = []
    for value in values or []:
        item = aliases.get(str(value).lower(), str(value).lower())
        if item == "all":
            expanded = list(
                all_values
                if include_config
                else tuple(v for v in all_values if v != "config")
            )
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
            facts.update(
                _parse_show_version(
                    to_text(stdout[0] if stdout else "", errors="surrogate_or_strict")
                )
            )
        except XikeOSError as exc:
            raise XikeOSFactsError(
                "failed to gather minimum device facts",
                detail=getattr(exc, "detail", None),
                commands=getattr(exc, "commands", None),
                context="device",
            ) from exc
        except Exception as exc:
            raise XikeOSFactsError(
                "failed to gather minimum device facts",
                detail=to_text(exc),
                context="device",
            ) from exc
    if "config" in subsets:
        try:
            facts["ansible_net_config"] = redact_text(
                get_config(module, source="running")
            )
        except XikeOSError as exc:
            raise XikeOSFactsError(
                "failed to gather config facts",
                detail=getattr(exc, "detail", None),
                commands=getattr(exc, "commands", None),
                context="config",
            ) from exc
        except Exception as exc:
            raise XikeOSFactsError(
                "failed to gather config facts", detail=to_text(exc), context="config"
            ) from exc
    facts["ansible_net_gather_subset"] = subsets  # type: ignore
    return facts


def _dict_values_with_names(value: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name, fields in sorted(value.items()):
        item = dict(fields)
        item.setdefault("name", name)
        items.append(item)
    return items


def gather_vlans(module: AnsibleModule) -> list[dict[str, Any]]:
    """Gather VLAN facts without importing the VLAN module implementation."""
    stdout = run_commands(module, ["show vlan"], check_rc=True) or []
    output = to_text(stdout[0] if stdout else "", errors="surrogate_or_strict")
    return parse_vlan(output, textfsm_templates=module.params.get("_textfsm_templates"))


def gather_interfaces(module: AnsibleModule) -> dict[str, Any]:
    """Gather base interface facts through the facts-layer contract."""
    return InterfacesFacts(module).get_facts()


def gather_l2_interfaces(module: AnsibleModule) -> dict[str, Any]:
    """Gather L2 interface facts through the facts-layer contract."""
    return L2InterfacesFacts(module).get_facts()


def gather_l3_interfaces(module: AnsibleModule) -> dict[str, Any]:
    """Gather L3 interface facts through the facts-layer contract."""
    return L3InterfacesFacts(module).get_facts()


def gather_lag_interfaces(module: AnsibleModule) -> dict[str, Any]:
    """Gather LAG interface facts through the facts-layer contract."""
    return LagInterfacesFacts(module).get_facts()


def gather_resource_facts(
    module: AnsibleModule, resources: list[str]
) -> dict[str, Any]:
    """Gather resource facts through the module-utils facts contracts."""
    gathered: dict[str, Any] = {}
    for resource in resources:
        try:
            if resource == "vlans":
                gathered[resource] = gather_vlans(module)
            elif resource == "interfaces":
                gathered[resource] = _dict_values_with_names(gather_interfaces(module))
            elif resource == "l2_interfaces":
                gathered[resource] = _dict_values_with_names(
                    gather_l2_interfaces(module)
                )
            elif resource == "l3_interfaces":
                gathered[resource] = _dict_values_with_names(
                    gather_l3_interfaces(module)
                )
            elif resource == "lag_interfaces":
                gathered[resource] = _dict_values_with_names(
                    gather_lag_interfaces(module)
                )
            elif resource == "static_routes":
                gathered[resource] = StaticRoutesFacts(module).facts.get(
                    "static_routes", []
                )
            elif resource == "acls":
                gathered[resource] = AclsFacts(module).facts.get("acls", [])
        except XikeOSError as exc:
            raise XikeOSFactsError(
                "failed to gather resource facts",
                detail=getattr(exc, "detail", None),
                commands=getattr(exc, "commands", None),
                context=resource,
            ) from exc
        except Exception as exc:
            raise XikeOSFactsError(
                "failed to gather resource facts", detail=to_text(exc), context=resource
            ) from exc
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

    subsets = _normalize_selectors(
        module.params.get("gather_subset") or ["min"],
        DEVICE_ALIASES,
        DEVICE_SUBSETS,
        include_config=False,
    )
    resources = _normalize_selectors(
        module.params.get("gather_network_resources") or [], {}, RESOURCE_NAMES
    )
    invalid_subsets = [item for item in subsets if item not in DEVICE_SUBSETS]
    invalid_resources = [item for item in resources if item not in RESOURCE_NAMES]
    if invalid_subsets or invalid_resources:
        module.fail_json(
            msg="unsupported facts selector",
            invalid_subsets=invalid_subsets,
            invalid_resources=invalid_resources,
        )
        return

    try:
        ansible_facts = gather_device_facts(module, subsets)
        ansible_facts["ansible_net_gather_network_resources"] = resources
        if resources:
            ansible_facts["ansible_network_resources"] = gather_resource_facts(
                module, resources
            )
    except XikeOSFactsError as exc:
        module.fail_json(
            msg=str(exc),
            error=redact_text(str(exc)),
            detail=redact_value(getattr(exc, "detail", None)),
            context=getattr(exc, "context", None),
            commands=redact_value(getattr(exc, "commands", None)),
            gather_subset=subsets,
            gather_network_resources=resources,
        )
        return
    module.exit_json(changed=False, ansible_facts=redact_value(ansible_facts))


if __name__ == "__main__":
    main()
