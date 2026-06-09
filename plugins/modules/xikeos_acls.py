#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS ACLs resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_acls
short_description: Manage Access Control Lists (ACLs) on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of ACLs on Xike (兮克) OS devices.
  - Manages Standard, MAC, and Mixed ACLs.
  - Xike OS uses different ACL numbering than Cisco IOS:
    - Standard ACL: 1-999
    - MAC ACL: 1000-1999
    - Mixed ACL: 2000-2999
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
          - Valid ranges depend on C(acl_type):
            - Standard: 1-999
            - MAC: 1000-1999
            - Mixed: 2000-2999
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
          - Description/remark for the ACL.
        type: str
        default: ''
      rules:
        description:
          - List of ACL rules.
          - Rules are applied in order (by sequence number or insertion order).
        type: list
        elements: dict
        suboptions:
          sequence:
            description:
              - Sequence number for the rule (1-65535).
              - If not specified, rules are numbered automatically (10, 20, 30, ...).
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
              - For Standard ACL: always 'ip'.
              - For MAC ACL: always 'mac'.
              - For Mixed ACL: 'ip', 'tcp', 'udp', 'icmp', etc.
            type: str
            default: 'ip'
          source:
            description:
              - Source address to match.
              - Can be an IP address, network/wildcard, or 'any'.
              - For MAC ACL: MAC address in HHHH.HHHH.HHHH format.
            type: str
            required: true
          destination:
            description:
              - Destination address to match.
              - Can be an IP address, network/wildcard, or 'any'.
              - For MAC ACL: MAC address in HHHH.HHHH.HHHH format.
              - For Standard ACL: always 'any' (implicit).
            type: str
            default: 'any'
          remark:
            description:
              - Description/remark for this specific rule.
            type: str
            default: ''
  state:
    description:
      - State of the ACL configuration.
      - C(merged) - Creates or updates ACLs as specified.
      - C(replaced) - Replaces existing ACL configuration with specified config.
      - C(deleted) - Deletes ACLs specified in config.
    type: str
    choices: ['merged', 'replaced', 'deleted']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Create standard IP ACL
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
        remark: Permit internal networks
        rules:
          - sequence: 10
            action: permit
            source: 192.168.0.0 0.0.255.255
          - sequence: 20
            action: deny
            source: any
    state: merged

- name: Create MAC ACL
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 1001
        acl_type: mac
        remark: Filter by MAC address
        rules:
          - sequence: 10
            action: permit
            source: 0011.2233.4455
            destination: 0000.0000.0000
          - sequence: 20
            action: deny
            source: any
            destination: any
    state: merged

- name: Create mixed/extended ACL
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 2001
        acl_type: mixed
        remark: Web traffic filter
        rules:
          - sequence: 10
            action: permit
            protocol: tcp
            source: 192.168.1.0 0.0.0.255
            destination: any
          - sequence: 20
            action: deny
            protocol: tcp
            source: any
            destination: any
    state: merged

- name: Replace ACL configuration
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
        rules:
          - sequence: 10
            action: permit
            source: 10.0.0.0 0.255.255.255
    state: replaced

- name: Delete specific ACL
  xike.xikeos.xikeos_acls:
    config:
      - acl_id: 100
        acl_type: standard
    state: deleted
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged) or C(replaced)
  type: list
  sample:
    - acl_id: 100
      acl_type: standard
      rules:
        - action: permit
          source: 192.168.0.0 0.0.255.255
after:
  description: The configuration after the module execution.
  returned: when I(state) is C(merged) or C(replaced)
  type: list
  sample:
    - acl_id: 100
      acl_type: standard
      rules:
        - action: permit
          source: 10.0.0.0 0.255.255.255
commands:
  description: The set of commands pushed to the device.
  returned: always
  type: list
  sample:
    - access-list 100 permit 192.168.0.0 0.0.255.255
    - access-list 100 deny any
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from typing import Any

AclRule = dict[str, Any]
AclConfig = dict[str, Any]
RuleKey = tuple[Any, Any, Any, Any]

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.acls import (
        AclsFacts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


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
    if acl_type == 'standard':
        if not (STANDARD_ACL_RANGE[0] <= acl_id <= STANDARD_ACL_RANGE[1]):
            return False, (
                "Standard ACL ID must be between {0} and {1}, got {2}".format(
                    STANDARD_ACL_RANGE[0], STANDARD_ACL_RANGE[1], acl_id
                )
            )
    elif acl_type == 'mac':
        if not (MAC_ACL_RANGE[0] <= acl_id <= MAC_ACL_RANGE[1]):
            return False, (
                "MAC ACL ID must be between {0} and {1}, got {2}".format(
                    MAC_ACL_RANGE[0], MAC_ACL_RANGE[1], acl_id
                )
            )
    elif acl_type == 'mixed':
        if not (MIXED_ACL_RANGE[0] <= acl_id <= MIXED_ACL_RANGE[1]):
            return False, (
                "Mixed ACL ID must be between {0} and {1}, got {2}".format(
                    MIXED_ACL_RANGE[0], MIXED_ACL_RANGE[1], acl_id
                )
            )
    else:
        return False, "Unknown ACL type: {0}".format(acl_type)

    return True, ''


def rule_key(rule: AclRule) -> RuleKey:
    """Generate a unique key for a rule entry for comparison."""
    return (
        rule.get('action', ''),
        rule.get('protocol', 'ip'),
        rule.get('source', ''),
        rule.get('destination', 'any'),
    )


def build_acl_commands(config: list[AclConfig], existing_acls: list[AclConfig]) -> list[str]:
    """Build CLI commands for ACL configuration.

    Args:
        config: list of desired ACL configurations
        existing_acls: list of existing ACL configurations

    Returns:
        list: CLI commands to apply
    """
    commands: list[str] = []

    # Build existing ACL map
    existing_by_id: dict[int, AclConfig] = {}
    for acl in existing_acls:
        existing_by_id[acl['acl_id']] = acl

    for acl_config in config:
        acl_id = acl_config['acl_id']
        acl_type = acl_config.get('acl_type', 'standard')
        remark = acl_config.get('remark', '')
        rules = acl_config.get('rules', [])

        existing = existing_by_id.get(acl_id, {})
        existing_rules = existing.get('rules', [])

        # Build rule commands
        rule_cmds = _build_rule_commands(acl_id, acl_type, rules, existing_rules)
        commands.extend(rule_cmds)

    return commands


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
    action = rule.get('action', 'permit')
    protocol = rule.get('protocol', 'ip')
    source = rule.get('source', 'any')
    destination = rule.get('destination', 'any')

    if acl_type == 'standard':
        # Standard ACL: access-list <id> <permit|deny> <source>
        # Protocol is always 'ip' (implicit)
        return 'access-list {0} {1} {2}'.format(acl_id, action, source)

    elif acl_type == 'mac':
        # MAC ACL: access-list <id> <permit|deny> <src_mac> <dst_mac>
        return 'access-list {0} {1} {2} {3}'.format(
            acl_id, action, source, destination
        )

    elif acl_type == 'mixed':
        # Mixed/Extended ACL: access-list <id> <permit|deny> <protocol> <src> <dst>
        return 'access-list {0} {1} {2} {3} {4}'.format(
            acl_id, action, protocol, source, destination
        )

    return None


def build_delete_commands(config: list[AclConfig], existing_acls: list[AclConfig]) -> list[str]:
    """Build CLI commands to delete ACLs.

    Args:
        config: list of ACL configurations to delete
        existing_acls: list of existing ACL configurations

    Returns:
        list: CLI commands to apply
    """
    commands: list[str] = []

    # If config is empty, delete all ACLs
    if not config:
        for acl in existing_acls:
            acl_id = acl['acl_id']
            commands.append('no access-list {0}'.format(acl_id))
        return commands

    # Delete specific ACLs
    delete_ids: set[int] = set()
    for acl_config in config:
        delete_ids.add(acl_config['acl_id'])

    for acl in existing_acls:
        acl_id = acl['acl_id']
        if acl_id in delete_ids:
            commands.append('no access-list {0}'.format(acl_id))

    return commands


def build_replaced_commands(config: list[AclConfig], existing_acls: list[AclConfig]) -> list[str]:
    """Build CLI commands for 'replaced' state.

    Removes existing ACLs in the config range and adds desired ones.
    """
    commands: list[str] = []

    # Build existing ACL map
    existing_by_id: dict[int, AclConfig] = {}
    for acl in existing_acls:
        existing_by_id[acl['acl_id']] = acl

    for acl_config in config:
        acl_id = acl_config['acl_id']
        acl_type = acl_config.get('acl_type', 'standard')
        rules = acl_config.get('rules', [])

        # If the ACL exists, remove it first
        if acl_id in existing_by_id:
            commands.append('no access-list {0}'.format(acl_id))

        # Add all rules as new
        for rule in rules:
            cmd = _build_access_list_cmd(acl_id, acl_type, rule)
            if cmd:
                commands.append(cmd)

    return commands


def build_after_state(
    before: list[AclConfig],
    desired: list[AclConfig],
    state: str,
) -> list[AclConfig]:
    """Build a normalized simulated after-state for ACL lifecycle results."""
    after_by_id = {acl['acl_id']: dict(acl) for acl in before}

    if state in ('merged', 'replaced'):
        for acl in desired:
            acl_id = acl['acl_id']
            if state == 'replaced' or acl_id not in after_by_id:
                after_by_id[acl_id] = dict(acl)
                after_by_id[acl_id]['rules'] = list(acl.get('rules', []))
                continue
            existing = after_by_id[acl_id]
            existing_rules = list(existing.get('rules', []))
            existing_keys = {rule_key(rule) for rule in existing_rules}
            for rule in acl.get('rules', []):
                if rule_key(rule) not in existing_keys:
                    existing_rules.append(rule)
            existing['rules'] = existing_rules
    elif state == 'deleted':
        if desired:
            for acl in desired:
                after_by_id.pop(acl['acl_id'], None)
        else:
            after_by_id = {}

    return [after_by_id[acl_id] for acl_id in sorted(after_by_id)]


def main() -> None:
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type='list',
            elements='dict',
            options=dict(
                acl_id=dict(
                    type='int',
                    required=True,
                ),
                acl_type=dict(
                    type='str',
                    choices=['standard', 'mac', 'mixed'],
                    required=True,
                ),
                remark=dict(
                    type='str',
                    default='',
                ),
                rules=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        sequence=dict(
                            type='int',
                        ),
                        action=dict(
                            type='str',
                            choices=['permit', 'deny'],
                            required=True,
                        ),
                        protocol=dict(
                            type='str',
                            default='ip',
                        ),
                        source=dict(
                            type='str',
                            required=True,
                        ),
                        destination=dict(
                            type='str',
                            default='any',
                        ),
                        remark=dict(
                            type='str',
                            default='',
                        ),
                    ),
                ),
            ),
        ),
        state=dict(
            type='str',
            choices=['merged', 'replaced', 'deleted'],
            default='merged',
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    config = module.params.get('config', []) or []
    state = module.params.get('state', 'merged')

    result = {
        'changed': False,
        'commands': [],
        'before': [],
        'after': [],
    }

    # Validate ACL IDs
    for acl_config in config:
        acl_id = acl_config['acl_id']
        acl_type = acl_config.get('acl_type', 'standard')
        is_valid, error_msg = validate_acl_id(acl_id, acl_type)
        if not is_valid:
            module.fail_json(msg=error_msg)

    if not HAS_FACTS:
        module.fail_json(msg='ACL facts support is required for diffing')
        return

    try:
        facts = AclsFacts(module)
        existing_acls = facts.facts.get('acls', [])
    except Exception as exc:
        module.fail_json(msg='failed to gather ACL facts: {0}'.format(exc))
        return

    result['before'] = existing_acls

    # Generate commands based on state
    if state == 'merged':
        commands = build_acl_commands(config, existing_acls)
    elif state == 'replaced':
        commands = build_replaced_commands(config, existing_acls)
    elif state == 'deleted':
        commands = build_delete_commands(config, existing_acls)
    else:
        commands = []

    result['commands'] = commands
    result['changed'] = bool(commands)
    result['after'] = build_after_state(existing_acls, config, state) if commands else existing_acls

    if module.check_mode:
        module.exit_json(**result)

    if commands:
        load_config(module, commands)
        try:
            facts_after = AclsFacts(module)
            result['after'] = facts_after.facts.get('acls', [])
        except Exception as exc:
            module.fail_json(msg='failed to gather ACL facts after apply: {0}'.format(exc))
            return

    module.exit_json(**result)


if __name__ == '__main__':
    main()
