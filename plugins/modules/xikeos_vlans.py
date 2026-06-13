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
        description:
          - VLAN state (active/suspend).
          - C(suspend) is accepted in the configuration model, but mutating states C(merged) and C(replaced) do not render suspended VLAN configuration items and will fail if one is requested.
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
      - C(rendered) - Renders CLI commands without connecting to the device.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'gathered', 'rendered']
    default: merged
author: clemon
"""

EXAMPLES = """
- name: Create VLANs on Xike switch
  c1emon.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
        state: active
      - vlan_id: 200
        name: VOICE
        state: active
    state: merged

- name: Replace VLAN configuration
  c1emon.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: SALES
        state: active
    state: replaced

- name: Delete VLANs
  c1emon.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
      - vlan_id: 200
    state: deleted

- name: Gather VLANs
  c1emon.xikeos.xikeos_vlans:
    state: gathered
"""

RETURN = """
changed:
  description: Whether the module changed the device configuration.
  returned: always
  type: bool
commands:
  description: List of commands sent to the device
  returned: when I(state) is C(merged), C(replaced), C(deleted), or C(rendered)
  type: list
  sample:
    - vlan 100
    - description DATA
    - vlan 200
    - description VOICE
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), or C(deleted)
  type: list
after:
  description: The configuration after the module execution.
  returned: when I(state) is C(merged), C(replaced), or C(deleted)
  type: list
gathered:
  description: VLAN state gathered from the device when I(state=gathered)
  returned: when state is gathered
  type: list
  elements: dict
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.vlans import parse_vlan
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config, run_commands
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import gather_with_error_boundary, run_resource_module_lifecycle


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
    """Normalize VLAN records to the keys used by lifecycle helpers."""
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
    """Index normalized VLAN records by VLAN ID."""
    return {item["vlan_id"]: _normalize_vlan(item) for item in vlans}


def get_commands(config: list[dict[str, Any]], state: str, current: Optional[list[dict[str, Any]]] = None) -> list[str]:
    """Generate minimal CLI commands from VLAN configuration and current state."""
    commands = []
    current_by_id = _index_vlans(current or [])

    if state == "merged":
        for vlan in config:
            requested_name = vlan.get("name")
            vlan = _normalize_vlan(vlan)
            vlan_id = vlan["vlan_id"]
            name = requested_name or ""
            existing = current_by_id.get(vlan_id)
            name_matches = True if not name else existing and existing.get("name", "") == name
            state_matches = existing and existing.get("state", "active") == vlan.get("state", "active")
            if existing and name_matches and state_matches:
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
            requested_name = vlan.get("name")
            vlan = _normalize_vlan(vlan)
            vlan_id = vlan["vlan_id"]
            name = requested_name or ""
            existing = current_by_id.get(vlan_id)
            name_matches = True if not name else existing and existing.get("name", "") == name
            state_matches = existing and existing.get("state", "active") == vlan.get("state", "active")
            if existing and name_matches and state_matches:
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


def validate_vlan_request(module: Any, config: list[dict[str, Any]], state: str) -> None:
    """Fail fast for VLAN lifecycle edge cases that are not safe to mutate."""
    if state == "gathered":
        return

    for vlan in config:
        vlan_id = int(vlan["vlan_id"])
        vlan_state = vlan.get("state") or vlan.get("status") or "active"
        if vlan_state == "suspend":
            module.fail_json(
                msg=(
                    "VLAN suspend state is not supported by xikeos_vlans mutating states; "
                    "use state=gathered to inspect current suspended VLANs"
                )
            )
            return
        if state == "deleted" and vlan_id == 1:
            module.fail_json(msg="Deleting default VLAN 1 is not supported")
            return


def gather_vlans(module: Any) -> list[dict[str, Any]]:
    """Collect VLAN state from the device and normalize parsed records."""
    def _gather() -> list[dict[str, Any]]:
        stdout = run_commands(module, ["show vlan"], check_rc=True)
        output = to_text(stdout[0] if stdout else "", errors="surrogate_or_strict")
        return [
            _normalize_vlan(vlan)
            for vlan in parse_vlan(output, textfsm_templates=module.params.get("_textfsm_templates"))
        ]

    return gather_with_error_boundary(
        module,
        _gather,
        "failed to gather VLAN state with 'show vlan'",
        "vlans",
        [],
        include_exception_in_msg=True,
    )


def build_after_state(before: list[dict[str, Any]], desired: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    """Compute the expected VLAN state after a lifecycle operation."""
    after = _index_vlans(before)
    if state in ("merged", "replaced"):
        if state == "replaced":
            desired_ids = {int(vlan["vlan_id"]) for vlan in desired}
            after = {vlan_id: vlan for vlan_id, vlan in after.items() if vlan_id in desired_ids or vlan_id == 1}
        for vlan in desired:
            normalized = _normalize_vlan(vlan)
            if not vlan.get("name") and normalized["vlan_id"] in after:
                normalized["name"] = after[normalized["vlan_id"]].get("name", "")
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
                    default=None,
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
            choices=["merged", "replaced", "deleted", "gathered", "rendered"],
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
    validate_vlan_request(module, config or [], state)

    run_resource_module_lifecycle(
        module=module,
        config=config,
        state=state,
        gather=gather_vlans,
        build_commands=get_commands,
        build_after=build_after_state,
        mutating_states=("merged", "replaced", "deleted"),
        gathered_states=("gathered",),
        rendered_states=("rendered",),
        apply_config=load_config,
    )


if __name__ == "__main__":
    main()
