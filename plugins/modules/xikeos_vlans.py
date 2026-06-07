#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS VLANs resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Optional

DOCUMENTATION = """
module: xikeos_vlans
short_description: Manage VLANs on Xike OS switches
version_added: "0.1.0"
description:
  - This module provides declarative management of VLANs on Xike OS devices.
  - VLANs can be created, modified, or deleted using this module.
options:
  config:
    description:
      - List of VLAN configurations.
      - Each entry defines a VLAN with its ID, name, and state.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description: VLAN ID (1-4094)
        type: int
        required: true
      name:
        description: VLAN name/description
        type: str
        required: false
      state:
        description: VLAN state (active/suspend)
        type: str
        choices: ['active', 'suspend']
        default: active
  state:
    description:
      - State of the VLAN configuration.
      - C(merged) - Creates or updates VLANs as specified.
      - C(replaced) - Replaces existing VLAN configuration with specified config.
      - C(deleted) - Deletes VLANs specified in config.
      - C(gathered) - Gathers VLAN state without changing the device.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'gathered']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Create VLANs on Xike switch
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
        state: active
      - vlan_id: 200
        name: VOICE
        state: active
    state: merged

- name: Replace VLAN configuration
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: SALES
        state: active
    state: replaced

- name: Delete VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
      - vlan_id: 200
    state: deleted

- name: Gather VLANs
  xike.xikeos.xikeos_vlans:
    state: gathered
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - vlan 100
    - description DATA
    - vlan 200
    - description VOICE
gathered:
  description: VLAN state gathered from the device when I(state=gathered)
  returned: when state is gathered
  type: list
  elements: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.xike.xikeos.plugins.module_utils.facts.vlans import parse_vlan
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config, run_commands


def vlan_id_range(vlan_ids: list[int]) -> str:
    """Convert a list of VLAN IDs to a range string (e.g., 100-200, 300)."""
    if not vlan_ids:
        return ""
    sorted_ids = sorted(set(vlan_ids))
    ranges = []
    start = sorted_ids[0]
    end = sorted_ids[0]

    for vid in sorted_ids[1:]:
        if vid == end + 1:
            end = vid
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = vid
            end = vid

    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ",".join(ranges)


def _normalize_vlan(vlan: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "vlan_id": int(vlan["vlan_id"]),
        "name": vlan.get("name") or "",
        "state": vlan.get("state") or vlan.get("status") or "active",
    }
    if "ports" in vlan:
        normalized["ports"] = list(vlan.get("ports") or [])
    if "type" in vlan:
        normalized["type"] = vlan.get("type")
    if "media" in vlan:
        normalized["media"] = vlan.get("media")
    return normalized


def _index_vlans(vlans: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {item["vlan_id"]: _normalize_vlan(item) for item in vlans}


def get_commands(config: list[dict[str, Any]], state: str, current: Optional[list[dict[str, Any]]] = None) -> list[str]:
    """Generate minimal CLI commands from VLAN configuration and current state."""
    commands = []
    current_by_id = _index_vlans(current or [])

    if state == "merged":
        for vlan in config:
            vlan = _normalize_vlan(vlan)
            vlan_id = vlan["vlan_id"]
            name = vlan.get("name", "")
            existing = current_by_id.get(vlan_id)
            if existing and existing.get("name", "") == name and existing.get("state", "active") == vlan.get("state", "active"):
                continue

            commands.append(f"vlan {vlan_id}")
            if name:
                commands.append(f"description {name}")
            commands.append("exit")

    elif state == "replaced":
        desired_ids = {int(vlan["vlan_id"]) for vlan in config}
        for vlan_id in sorted(set(current_by_id) - desired_ids):
            if vlan_id != 1:
                commands.append(f"no vlan {vlan_id}")
        for vlan in config:
            vlan = _normalize_vlan(vlan)
            vlan_id = vlan["vlan_id"]
            name = vlan.get("name", "")
            existing = current_by_id.get(vlan_id)
            if existing and existing.get("name", "") == name and existing.get("state", "active") == vlan.get("state", "active"):
                continue
            commands.append(f"vlan {vlan_id}")
            if name:
                commands.append(f"description {name}")
            commands.append("exit")

    elif state == "deleted":
        for vlan in config:
            vlan_id = vlan["vlan_id"]
            if vlan_id in current_by_id or not current:
                commands.append(f"no vlan {vlan_id}")

    return commands


def gather_vlans(module: Any) -> list[dict[str, Any]]:
    try:
        stdout = run_commands(module, ["show vlan"], check_rc=True)
    except Exception as exc:
        module.fail_json(msg="failed to gather VLAN state with 'show vlan': %s" % to_text(exc))
        return []
    output = to_text(stdout[0] if stdout else "", errors="surrogate_or_strict")
    return [
        _normalize_vlan(vlan)
        for vlan in parse_vlan(output, textfsm_templates=module.params.get("_textfsm_templates"))
    ]


def build_after_state(before: list[dict[str, Any]], desired: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    after = _index_vlans(before)
    if state in ("merged", "replaced"):
        if state == "replaced":
            desired_ids = {int(vlan["vlan_id"]) for vlan in desired}
            after = {vlan_id: vlan for vlan_id, vlan in after.items() if vlan_id in desired_ids or vlan_id == 1}
        for vlan in desired:
            normalized = _normalize_vlan(vlan)
            after[normalized["vlan_id"]] = normalized
    elif state == "deleted":
        for vlan in desired:
            after.pop(int(vlan["vlan_id"]), None)
    return [after[vlan_id] for vlan_id in sorted(after)]


def main() -> None:
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type="list",
            elements="dict",
            options=dict(
                vlan_id=dict(
                    type="int",
                    required=True,
                ),
                name=dict(
                    type="str",
                    required=False,
                    default="",
                ),
                state=dict(
                    type="str",
                    choices=["active", "suspend"],
                    default="active",
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["merged", "replaced", "deleted", "gathered"],
            default="merged",
        ),
        _textfsm_templates=dict(
            type="dict",
            required=False,
            no_log=True,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get("config", [])
    state = module.params.get("state", "merged")

    result = {
        "changed": False,
        "commands": [],
        "before": [],
        "after": [],
    }

    before = gather_vlans(module)
    result["before"] = before

    if state == "gathered":
        module.exit_json(changed=False, gathered=before)

    if not config:
        result["after"] = before
        module.exit_json(**result)

    commands = get_commands(config, state, before)
    result["commands"] = commands
    result["changed"] = bool(commands)
    result["after"] = build_after_state(before, config, state) if commands else before

    if module.check_mode:
        module.exit_json(**result)

    if commands:
        load_config(module, commands)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
