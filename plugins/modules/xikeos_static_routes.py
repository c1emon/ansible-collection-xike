#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS Static Routes resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_static_routes
short_description: Manage static routes on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of static routes on Xike (兮克) OS devices.
  - Manages both IPv4 and IPv6 static routes.
  - Xike OS uses the same static route syntax as Cisco IOS.
options:
  config:
    description:
      - List of static route configurations.
      - Each entry defines a static route with destination, mask, next hop, and optional parameters.
    type: list
    elements: dict
    suboptions:
      destination:
        description:
          - Network destination address.
          - For IPv4: dotted-decimal format (e.g., '192.168.1.0').
          - For IPv6: standard IPv6 format (e.g., '2001:db8::').
        type: str
        required: true
      mask:
        description:
          - Subnet mask or prefix length.
          - For IPv4: dotted-decimal mask (e.g., '255.255.255.0') or CIDR prefix (e.g., '24').
          - For IPv6: prefix length as string (e.g., '64').
        type: str
        required: true
      next_hop:
        description:
          - Next hop IP address or gateway.
        type: str
        required: true
      distance:
        description:
          - Administrative distance for the route.
          - Valid range: 1-255.
          - Default is 1 for static routes.
        type: int
        default: 1
      route_type:
        description:
          - Type of static route.
          - C(ipv4) for IPv4 static routes.
          - C(ipv6) for IPv6 static routes.
        type: str
        choices: ['ipv4', 'ipv6']
        default: ipv4
  state:
    description:
      - State of the static route configuration.
      - C(merged) - Adds or updates static routes as specified.
      - C(replaced) - Replaces existing static routes with specified config.
      - C(deleted) - Deletes static routes specified in config.
    type: str
    choices: ['merged', 'replaced', 'deleted']
    default: merged
author: Andy
"""

EXAMPLES = """
- name: Add IPv4 static routes
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 192.168.100.0
        mask: 255.255.255.0
        next_hop: 10.0.0.2
        distance: 1
        route_type: ipv4
      - destination: 10.10.0.0
        mask: 255.255.0.0
        next_hop: 10.0.0.3
        distance: 10
        route_type: ipv4
    state: merged

- name: Add default route
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 0.0.0.0
        mask: 0.0.0.0
        next_hop: 10.0.0.1
        route_type: ipv4
    state: merged

- name: Add IPv6 static route
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 2001:db8::
        mask: 32
        next_hop: 2001:db8::1
        route_type: ipv6
    state: merged

- name: Replace all static routes
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 0.0.0.0
        mask: 0.0.0.0
        next_hop: 10.0.0.1
        route_type: ipv4
    state: replaced

- name: Delete specific static routes
  c1emon.xikeos.xikeos_static_routes:
    config:
      - destination: 192.168.100.0
        mask: 255.255.255.0
        next_hop: 10.0.0.2
        route_type: ipv4
    state: deleted

- name: Delete all static routes (empty config)
  c1emon.xikeos.xikeos_static_routes:
    config: []
    state: deleted
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged) or C(replaced)
  type: list
  sample:
    - destination: 0.0.0.0
      mask: 0.0.0.0
      next_hop: 10.0.0.1
      distance: 1
      route_type: ipv4
after:
  description: The configuration after the module execution.
  returned: when I(state) is C(merged) or C(replaced)
  type: list
  sample:
    - destination: 0.0.0.0
      mask: 0.0.0.0
      next_hop: 10.0.0.1
      distance: 1
      route_type: ipv4
commands:
  description: The set of commands pushed to the device.
  returned: always
  type: list
  sample:
    - ip route 0.0.0.0 0.0.0.0 10.0.0.1
    - ip route 192.168.100.0 255.255.255.0 10.0.0.2 10
    - ipv6 route 2001:db8::/32 2001:db8::1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from typing import Any

RouteConfig = dict[str, Any]
RouteKey = tuple[Any, Any, Any]

try:
    from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.static_routes import (
        StaticRoutesFacts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


# Valid distance range
MIN_DISTANCE = 1
MAX_DISTANCE = 255


def normalize_route(route: RouteConfig) -> RouteConfig:
    """Normalize a route entry for comparison.

    Ensures consistent format for mask (CIDR for IPv6, dotted-decimal for IPv4).
    """
    normalized = dict(route)

    route_type = route.get('route_type', 'ipv4')
    destination = route.get('destination', '')
    mask = route.get('mask', '')

    if route_type == 'ipv4':
        # Ensure mask is in dotted-decimal format
        if mask.isdigit():
            normalized['mask'] = prefix_to_ipv4_mask(int(mask))
    elif route_type == 'ipv6':
        # Ensure mask is a prefix length string
        if not mask.isdigit():
            # Try to convert dotted-decimal to prefix
            prefix = ipv4_mask_to_prefix(mask)
            if prefix >= 0:
                normalized['mask'] = str(prefix)

    return normalized


def route_key(route: RouteConfig) -> RouteKey:
    """Generate a unique key for a route entry."""
    r = normalize_route(route)
    return (
        r.get('destination', ''),
        r.get('mask', ''),
        r.get('route_type', 'ipv4'),
    )


def build_static_route_commands(
    config: list[RouteConfig],
    existing_routes: list[RouteConfig],
) -> list[str]:
    """Build CLI commands for static route configuration.

    Args:
        config: list of desired route configurations
        existing_routes: list of existing route configurations

    Returns:
        list: CLI commands to apply
    """
    commands: list[str] = []

    # Normalize existing routes for comparison
    existing_by_key: dict[RouteKey, RouteConfig] = {}
    for route in existing_routes:
        key = route_key(route)
        existing_by_key[key] = route

    for route in config:
        normalized_route = normalize_route(route)
        existing = existing_by_key.get(route_key(normalized_route))
        if existing:
            existing = normalize_route(existing)
            if (
                existing.get('next_hop') == normalized_route.get('next_hop')
                and existing.get('distance', 1) == normalized_route.get('distance', 1)
            ):
                continue
        route_type = route.get('route_type', 'ipv4')
        destination = route.get('destination', '')
        mask = route.get('mask', '')
        next_hop = route.get('next_hop', '')
        distance = route.get('distance', 1)

        if route_type == 'ipv4':
            cmd = 'ip route {0} {1} {2}'.format(destination, mask, next_hop)
            if distance and distance != 1:
                cmd += ' {0}'.format(distance)
            commands.append(cmd)
        elif route_type == 'ipv6':
            # IPv6 uses CIDR notation
            if mask.isdigit():
                dest_with_prefix = '{0}/{1}'.format(destination, mask)
            else:
                dest_with_prefix = '{0}/{1}'.format(destination, mask)
            commands.append('ipv6 route {0} {1}'.format(dest_with_prefix, next_hop))

    return commands


def build_delete_commands(
    config: list[RouteConfig],
    existing_routes: list[RouteConfig],
) -> list[str]:
    """Build CLI commands to delete static routes.

    Args:
        config: list of route configurations to delete
        existing_routes: list of existing route configurations

    Returns:
        list: CLI commands to apply
    """
    commands: list[str] = []

    # Create set of routes to delete
    delete_keys: set[RouteKey] = set()
    for route in config:
        delete_keys.add(route_key(route))

    # If config is empty, delete all static routes
    if not config:
        for route in existing_routes:
            route_type = route.get('route_type', 'ipv4')
            destination = route.get('destination', '')
            mask = route.get('mask', '')
            next_hop = route.get('next_hop', '')

            cmd = _build_no_route_cmd(route_type, destination, mask, next_hop)
            if cmd:
                commands.append(cmd)
        return commands

    # Delete specific routes
    for route in existing_routes:
        key = route_key(route)
        if key in delete_keys:
            route_type = route.get('route_type', 'ipv4')
            destination = route.get('destination', '')
            mask = route.get('mask', '')
            next_hop = route.get('next_hop', '')

            cmd = _build_no_route_cmd(route_type, destination, mask, next_hop)
            if cmd:
                commands.append(cmd)

    return commands


def _build_no_route_cmd(route_type: str, destination: str, mask: str, next_hop: str) -> str | None:
    """Build a 'no ip/ipv6 route' command."""
    if route_type == 'ipv4':
        return 'no ip route {0} {1} {2}'.format(destination, mask, next_hop)
    elif route_type == 'ipv6':
        if mask.isdigit():
            dest_with_prefix = '{0}/{1}'.format(destination, mask)
        else:
            dest_with_prefix = '{0}/{1}'.format(destination, mask)
        return 'no ipv6 route {0} {1}'.format(dest_with_prefix, next_hop)
    return None


def build_replaced_commands(
    config: list[RouteConfig],
    existing_routes: list[RouteConfig],
) -> list[str]:
    """Build CLI commands for 'replaced' state.

    Removes all existing static routes and adds the desired ones.
    """
    commands: list[str] = []

    # First, delete all existing routes
    for route in existing_routes:
        route_type = route.get('route_type', 'ipv4')
        destination = route.get('destination', '')
        mask = route.get('mask', '')
        next_hop = route.get('next_hop', '')

        cmd = _build_no_route_cmd(route_type, destination, mask, next_hop)
        if cmd:
            commands.append(cmd)

    # Then add desired routes
    commands.extend(build_static_route_commands(config, []))

    return commands


def build_after_state(
    before: list[RouteConfig],
    desired: list[RouteConfig],
    state: str,
) -> list[RouteConfig]:
    """Build a normalized simulated after-state for static route lifecycle results."""
    after_by_key = {route_key(route): normalize_route(route) for route in before}

    if state == 'replaced':
        after_by_key = {}

    if state in ('merged', 'replaced'):
        for route in desired:
            normalized = normalize_route(route)
            after_by_key[route_key(normalized)] = normalized
    elif state == 'deleted':
        if desired:
            for route in desired:
                after_by_key.pop(route_key(route), None)
        else:
            after_by_key = {}

    return [after_by_key[key] for key in sorted(after_by_key)]


def prefix_to_ipv4_mask(prefix_len: int) -> str:
    """Convert CIDR prefix length to dotted-decimal mask."""
    if prefix_len == 0:
        return '0.0.0.0'
    if prefix_len >= 32:
        return '255.255.255.255'

    mask_bits = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return '.'.join(str((mask_bits >> (8 * i)) & 0xFF) for i in range(3, -1, -1))


def ipv4_mask_to_prefix(mask: str) -> int:
    """Convert dotted-decimal mask to CIDR prefix length. Returns -1 on failure."""
    try:
        parts = mask.split('.')
        if len(parts) != 4:
            return -1
        bits = sum(int(p).bit_length() for p in parts)
        # More accurate: convert to binary and count
        binary = 0
        for p in parts:
            binary = (binary << 8) | int(p)
        # Count leading 1s
        prefix = 0
        temp = binary
        while temp & 0x80000000:
            prefix += 1
            temp = (temp << 1) & 0xFFFFFFFF
        # Verify it's a valid mask
        expected = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        if binary == expected:
            return prefix
        return -1
    except (ValueError, AttributeError):
        return -1


def main() -> None:
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type='list',
            elements='dict',
            options=dict(
                destination=dict(
                    type='str',
                    required=True,
                ),
                mask=dict(
                    type='str',
                    required=True,
                ),
                next_hop=dict(
                    type='str',
                    required=True,
                ),
                distance=dict(
                    type='int',
                    default=1,
                    choices=list(range(MIN_DISTANCE, MAX_DISTANCE + 1)),
                ),
                route_type=dict(
                    type='str',
                    choices=['ipv4', 'ipv6'],
                    default='ipv4',
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

    # Validate distance range
    for route in config:
        distance = route.get('distance', 1)
        if distance < MIN_DISTANCE or distance > MAX_DISTANCE:
            module.fail_json(
                msg="Distance must be between {0} and {1}, got {2}".format(
                    MIN_DISTANCE, MAX_DISTANCE, distance
                )
            )

    result = {
        'changed': False,
        'commands': [],
        'before': [],
        'after': [],
    }

    if not HAS_FACTS:
        module.fail_json(msg='static route facts support is required for diffing')
        return

    try:
        facts = StaticRoutesFacts(module)
        existing_routes = facts.facts.get('static_routes', [])
    except Exception as exc:
        module.fail_json(msg='failed to gather static route facts: {0}'.format(exc))
        return

    result['before'] = existing_routes

    # Generate commands based on state
    if state == 'merged':
        commands = build_static_route_commands(config, existing_routes)
    elif state == 'replaced':
        commands = build_replaced_commands(config, existing_routes)
    elif state == 'deleted':
        commands = build_delete_commands(config, existing_routes)
    else:
        commands = []

    result['commands'] = commands
    result['changed'] = bool(commands)
    result['after'] = build_after_state(existing_routes, config, state) if commands else existing_routes

    if module.check_mode:
        module.exit_json(**result)

    if commands:
        load_config(module, commands)
        try:
            facts_after = StaticRoutesFacts(module)
            result['after'] = facts_after.facts.get('static_routes', [])
        except Exception as exc:
            module.fail_json(msg='failed to gather static route facts after apply: {0}'.format(exc))
            return

    module.exit_json(**result)


if __name__ == '__main__':
    main()
