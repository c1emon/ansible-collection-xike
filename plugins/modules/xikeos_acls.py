#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS ACLs resource module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
# pylint: disable=unsupported-binary-operation

DOCUMENTATION = """
module: xikeos_acls
short_description: Manage Access Control Lists (ACLs) on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of ACLs on Xike (兮克) OS devices.
  - Manages Standard, MAC, and Mixed ACLs.
  - Xike OS uses different ACL numbering than Cisco IOS.
  - Standard ACL range is 1-999.
  - MAC ACL range is 1000-1999.
  - Mixed ACL range is 2000-2999.
options:
  config:
    description:
      - List of ACL configurations.
      - Each entry defines an ACL with its ID, type, and rules.
    type: list
    elements: dict
    suboptions:
      acl_id:
        description:
          - ACL identifier number.
          - Valid ranges depend on C(acl_type).
          - Standard ACL range is 1-999.
          - MAC ACL range is 1000-1999.
          - Mixed ACL range is 2000-2999.
        type: int
        required: true
      acl_type:
        description:
          - Type of ACL.
          - C(standard) for standard IP ACLs (1-999).
          - C(mac) for MAC address ACLs (1000-1999).
          - C(mixed) for mixed/extended ACLs (2000-2999).
        type: str
        choices: ['standard', 'mac', 'mixed']
        required: true
      remark:
        description:
          - Not supported by the evidence-admitted positional ACL model; non-empty values fail before rendering.
        type: str
        default: null
      rules:
        description:
          - List of ACL rules.
          - Rules are applied in insertion order.
        type: list
        elements: dict
        suboptions:
          sequence:
            description:
              - Not supported by the evidence-admitted positional ACL model; non-empty values fail before rendering.
            type: int
          action:
            description:
              - Action to take when the rule matches.
              - C(permit) to allow traffic.
              - C(deny) to block traffic.
            type: str
            choices: ['permit', 'deny']
            required: true
          protocol:
            description:
              - Protocol to match.
              - For Standard ACL, always 'ip'.
              - For MAC ACL, always 'mac'.
              - For Mixed ACL, 'ip', 'tcp', 'udp', 'icmp', etc.
            type: str
            default: 'ip'
          source:
            description:
              - Source address to match.
              - Can be an IP address, network/wildcard, or 'any'.
              - For MAC ACL, MAC address in HHHH.HHHH.HHHH format.
            type: str
            required: true
          destination:
            description:
              - Destination address to match.
              - Can be an IP address, network/wildcard, or 'any'.
              - For MAC ACL, MAC address in HHHH.HHHH.HHHH format.
              - For Standard ACL, always 'any' (implicit).
            type: str
            default: 'any'
          remark:
            description:
              - Not supported by the evidence-admitted positional ACL model; non-empty values fail before rendering.
            type: str
            default: null
  state:
    description:
      - State of the ACL configuration.
      - C(merged) - Creates or updates ACLs as specified.
      - C(replaced) - Replaces existing ACL configuration with specified config.
      - C(deleted) - Deletes ACLs specified in config.
      - C(gathered) - Gathers ACL state without changing the device.
      - C(rendered) - Renders CLI commands without connecting to the device.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'gathered', 'rendered']
    default: merged
author: "clemon (@c1emon)"
"""

EXAMPLES = """
- name: Create standard IP ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
        rules:
          - action: permit
            source: 192.168.0.0 0.0.255.255
          - action: deny
            source: any
    state: merged

- name: Create MAC ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 1001
        acl_type: mac
        rules:
          - action: permit
            source: 0011.2233.4455
            destination: 0000.0000.0000
          - action: deny
            source: any
            destination: any
    state: merged

- name: Create mixed/extended ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 2001
        acl_type: mixed
        rules:
          - action: permit
            protocol: tcp
            source: 192.168.1.0 0.0.0.255
            destination: any
          - action: deny
            protocol: tcp
            source: any
            destination: any
    state: merged

- name: Replace ACL configuration
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
        rules:
          - action: permit
            source: 10.0.0.0 0.255.255.255
    state: replaced

- name: Delete specific ACL
  c1emon.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
    state: deleted
"""

RETURN = """
changed:
  description: Whether the module changed the device configuration.
  returned: always
  type: bool
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), or C(deleted)
  type: list
  sample:
    - acl_id: 100
      acl_type: standard
      rules:
        - action: permit
          source: 192.168.0.0 0.0.255.255
after:
  description: The configuration after the module execution.
  returned: when I(state) is C(merged), C(replaced), or C(deleted)
  type: list
  sample:
    - acl_id: 100
      acl_type: standard
      rules:
        - action: permit
          source: 10.0.0.0 0.255.255.255
commands:
  description: The set of commands pushed to the device.
  returned: when I(state) is C(merged), C(replaced), C(deleted), or C(rendered)
  type: list
  sample:
    - access-list 100 permit 192.168.0.0 0.0.255.255
    - access-list 100 deny any
gathered:
  description: ACL state gathered from the device when I(state) is C(gathered).
  returned: when I(state) is C(gathered)
  type: list
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.acls import AclsFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    load_config,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import (
    gather_with_error_boundary,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import (
    run_resource_module_lifecycle,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.reconcile import (
    FieldPolicy,
    Operation,
    ReconciliationInputError,
    ResourcePlan,
    ResourcePolicy,
    plan_operations,
    seal_resource_plan,
)
from typing import Any

AclRule = dict[str, Any]
AclConfig = dict[str, Any]
RuleKey = tuple[Any, Any, Any, Any]

ACL_POLICY = ResourcePolicy(
    identity=("acl_id", "acl_type"),
    fields={
        "rules": FieldPolicy(
            kind="ordered",
            identity=("action", "protocol", "source", "destination"),
            removal_supported=False,
        ),
        "present": FieldPolicy(kind="scalar", removal_supported=False),
    },
)

# Valid ACL ID ranges
STANDARD_ACL_RANGE = (1, 999)
MAC_ACL_RANGE = (1000, 1999)
MIXED_ACL_RANGE = (2000, 2999)


def validate_acl_id(acl_id: int, acl_type: str) -> tuple[bool, str]:
    """Validate ACL ID is within the correct range for the given type.

    Args:
        acl_id: The ACL identifier
        acl_type: The ACL type ('standard', 'mac', 'mixed')

    Returns:
        tuple: (is_valid, error_message)
    """
    if acl_type == "standard":
        if not (STANDARD_ACL_RANGE[0] <= acl_id <= STANDARD_ACL_RANGE[1]):
            return False, (
                "Standard ACL ID must be between {0} and {1}, got {2}".format(
                    STANDARD_ACL_RANGE[0], STANDARD_ACL_RANGE[1], acl_id
                )
            )
    elif acl_type == "mac":
        if not (MAC_ACL_RANGE[0] <= acl_id <= MAC_ACL_RANGE[1]):
            return False, (
                "MAC ACL ID must be between {0} and {1}, got {2}".format(
                    MAC_ACL_RANGE[0], MAC_ACL_RANGE[1], acl_id
                )
            )
    elif acl_type == "mixed":
        if not (MIXED_ACL_RANGE[0] <= acl_id <= MIXED_ACL_RANGE[1]):
            return False, (
                "Mixed ACL ID must be between {0} and {1}, got {2}".format(
                    MIXED_ACL_RANGE[0], MIXED_ACL_RANGE[1], acl_id
                )
            )
    else:
        return False, "Unknown ACL type: {0}".format(acl_type)

    return True, ""


def rule_key(rule: AclRule) -> RuleKey:
    """Generate a unique key for a rule entry for comparison."""
    return (
        rule.get("action", ""),
        rule.get("protocol", "ip"),
        rule.get("source", ""),
        rule.get("destination", "any"),
    )


def _validate_positional_acl_config(config: list[AclConfig]) -> None:
    """Reject inputs whose semantics cannot round-trip from admitted evidence."""
    seen_acls: set[int] = set()
    for acl in config:
        acl_id = acl["acl_id"]
        if acl_id in seen_acls:
            raise ReconciliationInputError("duplicate ACL identity: {0}".format(acl_id))
        seen_acls.add(acl_id)
        if acl.get("remark"):
            raise ReconciliationInputError(
                "ACL remarks are not admitted by the command evidence register"
            )
        seen_rules: set[RuleKey] = set()
        for rule in acl.get("rules", []):
            if rule.get("sequence") is not None:
                raise ReconciliationInputError(
                    "ACL sequence is not admitted by the positional ACL model"
                )
            if rule.get("remark"):
                raise ReconciliationInputError(
                    "ACL rule remarks are not admitted by the command evidence register"
                )
            key = rule_key(rule)
            if key in seen_rules:
                raise ReconciliationInputError(
                    "duplicate ACL rule identity for ACL {0}: {1}".format(acl_id, key)
                )
            seen_rules.add(key)


def build_acl_commands(
    config: list[AclConfig], existing_acls: list[AclConfig]
) -> list[str]:
    """Build CLI commands for ACL configuration.

    Args:
        config: list of desired ACL configurations
        existing_acls: list of existing ACL configurations

    Returns:
        list: CLI commands to apply
    """
    return list(build_lifecycle_plan(config, "merged", existing_acls).commands)


def _build_rule_commands(
    acl_id: int,
    acl_type: str,
    desired_rules: list[AclRule],
    existing_rules: list[AclRule],
) -> list[str]:
    """Build commands to configure rules for an ACL."""
    commands: list[str] = []

    # Create set of existing rule keys
    existing_rule_keys: set[RuleKey] = set()
    for rule in existing_rules:
        existing_rule_keys.add(rule_key(rule))

    # Add rules that don't exist yet
    for rule in desired_rules:
        key = rule_key(rule)
        if key not in existing_rule_keys:
            cmd = _build_access_list_cmd(acl_id, acl_type, rule)
            if cmd:
                commands.append(cmd)

    return commands


def _build_access_list_cmd(acl_id: int, acl_type: str, rule: AclRule) -> str | None:
    """Build a single 'access-list' command.

    Format: access-list <id> <permit|deny> [<protocol>] <src> [<dst>]
    """
    action = rule.get("action", "permit")
    protocol = rule.get("protocol", "ip")
    source = rule.get("source", "any")
    destination = rule.get("destination", "any")

    if acl_type == "standard":
        # Standard ACL: access-list <id> <permit|deny> <source>
        # Protocol is always 'ip' (implicit)
        return "access-list {0} {1} {2}".format(acl_id, action, source)

    elif acl_type == "mac":
        # MAC ACL: access-list <id> <permit|deny> <src_mac> <dst_mac>
        return "access-list {0} {1} {2} {3}".format(acl_id, action, source, destination)

    elif acl_type == "mixed":
        # Mixed/Extended ACL: access-list <id> <permit|deny> <protocol> <src> <dst>
        return "access-list {0} {1} {2} {3} {4}".format(
            acl_id, action, protocol, source, destination
        )

    return None


def build_delete_commands(
    config: list[AclConfig], existing_acls: list[AclConfig]
) -> list[str]:
    """Build CLI commands to delete ACLs.

    Args:
        config: list of ACL configurations to delete
        existing_acls: list of existing ACL configurations

    Returns:
        list: CLI commands to apply
    """
    return list(build_lifecycle_plan(config, "deleted", existing_acls).commands)


def build_replaced_commands(
    config: list[AclConfig], existing_acls: list[AclConfig]
) -> list[str]:
    """Build CLI commands for 'replaced' state.

    Removes existing ACLs in the config range and adds desired ones.
    """
    return list(build_lifecycle_plan(config, "replaced", existing_acls).commands)


def _acl_state_for_plan(acls: list[AclConfig], label: str) -> dict[tuple[int, str], AclConfig]:
    """Canonicalize positional ACL facts for shared ordered reconciliation."""
    _validate_positional_acl_config(acls)
    state: dict[tuple[int, str], AclConfig] = {}
    for acl in acls:
        key = (acl["acl_id"], acl["acl_type"])
        if key in state:
            raise ReconciliationInputError("duplicate ACL identity: {0}".format(key))
        rules = []
        for rule in acl.get("rules", []):
            normalized_rule = dict(rule)
            normalized_rule.setdefault("protocol", "ip")
            normalized_rule.setdefault("destination", "any")
            rules.append(normalized_rule)
        state[key] = {
            "acl_id": acl["acl_id"],
            "acl_type": acl["acl_type"],
            "rules": rules,
            "present": True,
        }
    return state


def _public_acl_state(state: dict[Any, AclConfig]) -> list[AclConfig]:
    """Return the documented ACL fact shape without planner-only presence."""
    public = []
    for acl in state.values():
        if acl.get("present", True):
            public.append(
                {
                    "acl_id": acl["acl_id"],
                    "acl_type": acl["acl_type"],
                    "rules": [dict(rule) for rule in acl.get("rules", [])],
                }
            )
    return sorted(public, key=lambda acl: (acl["acl_id"], acl["acl_type"]))


def _render_acl_operation(operation: Operation) -> list[str]:
    """Render one shared ordered-policy ACL operation."""
    resource = dict(operation.resource)
    acl_id = resource["acl_id"]
    acl_type = resource["acl_type"]
    if operation.field == "present" and operation.value is False:
        return ["no access-list {0}".format(acl_id)]
    if operation.field == "rules" and operation.action == "add_item":
        command = _build_access_list_cmd(acl_id, acl_type, operation.value)
        if command:
            return [command]
    if operation.field == "rules" and operation.action == "replace_ordered":
        commands = ["no access-list {0}".format(acl_id)]
        for rule in operation.value:
            command = _build_access_list_cmd(acl_id, acl_type, rule)
            if command:
                commands.append(command)
        return commands
    raise ReconciliationInputError("unsupported ACL operation: {0}".format(operation))


def build_lifecycle_plan(
    config: list[AclConfig], state: str, existing_acls: list[AclConfig]
) -> ResourcePlan:
    """Build an immutable plan under the admitted positional ACL model."""
    current = _acl_state_for_plan(existing_acls, "current")
    desired = _acl_state_for_plan(config, "desired")
    if state == "deleted":
        if not config:
            raise ReconciliationInputError(
                "empty ACL deletion is unsafe; specify exact ACL identities"
            )
        desired = {
            key: {"acl_id": value["acl_id"], "acl_type": value["acl_type"], "present": False}
            for key, value in desired.items()
        }
        planning_state = "replaced"
    elif state in ("merged", "replaced", "rendered"):
        planning_state = state
    else:
        raise ReconciliationInputError("unsupported ACL lifecycle state: {0}".format(state))
    operations = plan_operations(current, desired, planning_state, ACL_POLICY)
    plan = seal_resource_plan(
        current, operations, ACL_POLICY, _render_acl_operation, state
    )
    return ResourcePlan(plan.operations, plan.commands, _public_acl_state(plan.after), plan.changed)


def build_after_state(
    before: list[AclConfig], desired: list[AclConfig], state: str
) -> list[AclConfig]:
    """Compatibility wrapper around the ACL sealed plan."""
    return list(build_lifecycle_plan(desired, state, before).after)


def build_lifecycle_commands(
    config: list[AclConfig], state: str, existing_acls: list[AclConfig]
) -> list[str]:
    """Compatibility wrapper around the ACL sealed plan."""
    return list(build_lifecycle_plan(config, state, existing_acls).commands)


def gather_acls(module):
    """Gather ACL facts with the shared error boundary."""
    return gather_with_error_boundary(
        module,
        lambda: AclsFacts(module).facts.get("acls", []),
        "failed to gather ACL facts",
        "acls",
        [],
    )


def main() -> None:
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type="list",
            elements="dict",
            options=dict(
                acl_id=dict(
                    type="int",
                    required=True,
                ),
                acl_type=dict(
                    type="str",
                    choices=["standard", "mac", "mixed"],
                    required=True,
                ),
                remark=dict(type="str", default=None),
                rules=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        sequence=dict(
                            type="int",
                        ),
                        action=dict(
                            type="str",
                            choices=["permit", "deny"],
                            required=True,
                        ),
                        protocol=dict(
                            type="str",
                            default="ip",
                        ),
                        source=dict(
                            type="str",
                            required=True,
                        ),
                        destination=dict(
                            type="str",
                            default="any",
                        ),
                        remark=dict(type="str", default=None),
                    ),
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["merged", "replaced", "deleted", "gathered", "rendered"],
            default="merged",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get("config", []) or []
    state = module.params.get("state", "merged")

    # Validate ACL IDs
    for acl_config in config:
        acl_id = acl_config["acl_id"]
        acl_type = acl_config.get("acl_type", "standard")
        is_valid, error_msg = validate_acl_id(acl_id, acl_type)
        if not is_valid:
            module.fail_json(msg=error_msg)
    try:
        _validate_positional_acl_config(config)
    except ReconciliationInputError as exc:
        module.fail_json(msg="invalid ACL configuration", error=str(exc))
    run_resource_module_lifecycle(
        module=module,
        config=config,
        state=state,
        gather=gather_acls,
        build_commands=build_lifecycle_commands,
        build_after=build_after_state,
        mutating_states=("merged", "replaced", "deleted"),
        gathered_states=("gathered",),
        rendered_states=("rendered",),
        rendered_current=[],
        apply_config=load_config,
        gather_after_apply=True,
        build_plan=build_lifecycle_plan,
    )


if __name__ == "__main__":
    main()
