#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Xike OS Static Routes resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type
# pylint: disable=unsupported-binary-operation

DOCUMENTATION = """
module: xikeos_static_routes
short_description: Manage static routes on Xike OS devices
version_added: "0.1.0"
description:
  - This module provides declarative management of static routes on Xike (兮克) OS devices.
  - Manages evidence-admitted IPv4 static routes.
  - IPv6 mutation is rejected until matching command and gather evidence is recorded.
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
          - "For IPv4: dotted-decimal format (e.g., '192.168.1.0')."
        type: str
        required: true
      mask:
        description:
          - Subnet mask or prefix length.
          - "For IPv4: dotted-decimal mask (e.g., '255.255.255.0') or CIDR prefix (e.g., '24')."
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
          - "Valid range: 1-255."
          - Default is 1 for static routes.
        type: int
        default: 1
      route_type:
        description:
          - Type of static route.
          - C(ipv4) for IPv4 static routes.
          - C(ipv6) is accepted only for gathered data; mutation and rendered planning fail closed.
          - If omitted, the module infers the type from C(destination) or C(next_hop).
        type: str
        choices: ['ipv4', 'ipv6']
  state:
    description:
      - State of the static route configuration.
      - C(merged) - Adds or updates static routes as specified.
      - C(replaced) - Replaces existing static routes with specified config.
      - C(deleted) - Deletes static routes specified in config.
      - C(gathered) - Gathers static route state without changing the device.
      - C(rendered) - Renders CLI commands without connecting to the device.
    type: str
    choices: ['merged', 'replaced', 'deleted', 'gathered', 'rendered']
    default: merged
author: "clemon (@c1emon)"
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

- name: Synchronize listed static routes while preserving unlisted routes
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
    - destination: 0.0.0.0
      mask: 0.0.0.0
      next_hop: 10.0.0.1
      distance: 1
      route_type: ipv4
after:
  description: The configuration after the module execution.
  returned: when I(state) is C(merged), C(replaced), or C(deleted)
  type: list
  sample:
    - destination: 0.0.0.0
      mask: 0.0.0.0
      next_hop: 10.0.0.1
      distance: 1
      route_type: ipv4
commands:
  description: The set of commands pushed to the device.
  returned: when I(state) is C(merged), C(replaced), C(deleted), or C(rendered)
  type: list
  sample:
    - ip route 0.0.0.0 0.0.0.0 10.0.0.1
    - ip route 192.168.100.0 255.255.255.0 10.0.0.2 10
gathered:
  description: Static route state gathered from the device when I(state) is C(gathered).
  returned: when I(state) is C(gathered)
  type: list
rendered:
  description: Rendered CLI commands when I(state) is C(rendered).
  returned: when I(state) is C(rendered)
  type: list
"""

import ipaddress

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.static_routes import StaticRoutesFacts
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import gather_with_error_boundary, run_resource_module_lifecycle
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.reconcile import (
    FieldPolicy,
    Operation,
    ReconciliationInputError,
    ResourcePlan,
    ResourcePolicy,
    seal_resource_plan,
)
from typing import Any

RouteConfig = dict[str, Any]
RouteKey = tuple[Any, Any, Any, Any]

# Valid distance range
MIN_DISTANCE = 1
MAX_DISTANCE = 255

STATIC_ROUTE_POLICY = ResourcePolicy(
    identity=('route_type', 'destination', 'mask', 'next_hop'),
    fields={
        # ``distance`` is the admitted IPv4 add form. A changed distance must
        # fail closed because the available delete form cannot scope it.
        'distance': FieldPolicy(kind='scalar', removal_supported=False),
        # Used only by ``deleted`` planning so the sealed plan can model an
        # exact resource deletion without global route removal semantics.
        'present': FieldPolicy(kind='scalar', removal_supported=False),
    },
)


def infer_route_type(route: RouteConfig) -> str:
    """Infer route type from explicit option or IP address fields."""
    explicit = route.get('route_type')
    if explicit:
        return explicit
    for field in ('destination', 'next_hop'):
        value = str(route.get(field) or '').split('/', 1)[0]
        if not value:
            continue
        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            continue
        return 'ipv6' if address.version == 6 else 'ipv4'
    return 'ipv4'


def normalize_route(route: RouteConfig) -> RouteConfig:
    """Normalize a route entry for comparison.

    Ensures consistent format for mask (CIDR for IPv6, dotted-decimal for IPv4).
    """
    normalized = dict(route)

    route_type = infer_route_type(route)
    normalized['route_type'] = route_type
    normalized['destination'] = route.get('destination', '')
    normalized['mask'] = str(route.get('mask', ''))
    normalized['next_hop'] = route.get('next_hop', '')
    normalized['distance'] = route.get('distance', 1)
    mask = str(normalized['mask'])

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
        r.get('route_type', 'ipv4'),
        r.get('destination', ''),
        r.get('mask', ''),
        r.get('next_hop', ''),
    )


def _normalized_route_map(routes: list[RouteConfig], label: str) -> dict[RouteKey, RouteConfig]:
    """Validate exact route identities before a command can be rendered."""
    normalized: dict[RouteKey, RouteConfig] = {}
    for route in routes:
        candidate = normalize_route(route)
        key = route_key(candidate)
        if key in normalized:
            raise ReconciliationInputError(
                'duplicate or ambiguous {0} static route identity: {1}'.format(label, key)
            )
        normalized[key] = candidate
    return normalized


def _reject_unadmitted_ipv6(routes: list[RouteConfig], state: str) -> None:
    if any(normalize_route(route).get('route_type') == 'ipv6' for route in routes):
        raise ReconciliationInputError(
            'IPv6 static-route {0} is not admitted by the command evidence register'.format(state)
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

    _reject_unadmitted_ipv6(config, 'configuration')
    existing_by_key = _normalized_route_map(existing_routes, 'current')
    desired_by_key = _normalized_route_map(config, 'desired')

    for key in sorted(desired_by_key):
        normalized_route = desired_by_key[key]
        existing = existing_by_key.get(key)
        if existing:
            if existing.get('distance', 1) == normalized_route.get('distance', 1):
                continue
            raise ReconciliationInputError(
                'cannot safely replace static-route distance without an exact delete form: {0}'.format(key)
            )
        route_type = normalized_route.get('route_type', 'ipv4')
        destination = normalized_route.get('destination', '')
        mask = normalized_route.get('mask', '')
        next_hop = normalized_route.get('next_hop', '')
        distance = normalized_route.get('distance', 1)

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
    if not config:
        raise ReconciliationInputError('empty static-route deletion is unsafe; specify exact routes')
    _reject_unadmitted_ipv6(config, 'deletion')
    commands: list[str] = []
    existing_by_key = _normalized_route_map(existing_routes, 'current')
    desired_by_key = _normalized_route_map(config, 'desired')

    for key in sorted(desired_by_key):
        existing = existing_by_key.get(key)
        if existing is None:
            continue
        desired = desired_by_key[key]
        if existing.get('distance', 1) != desired.get('distance', 1):
            raise ReconciliationInputError(
                'cannot safely delete static route with an ambiguous distance: {0}'.format(key)
            )
        cmd = _build_no_route_cmd(
            existing.get('route_type', 'ipv4'),
            existing.get('destination', ''),
            existing.get('mask', ''),
            existing.get('next_hop', ''),
        )
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

    Synchronizes only desired route identities and preserves unlisted routes.
    """
    return build_static_route_commands(config, existing_routes)


def _route_operation_resource(key: RouteKey) -> tuple[tuple[str, Any], ...]:
    return tuple(zip(STATIC_ROUTE_POLICY.identity, key))


def _route_state_for_plan(routes: list[RouteConfig], label: str) -> dict[RouteKey, RouteConfig]:
    """Return canonical planner state with an explicit resource-presence bit."""
    return {
        key: {**route, 'present': True}
        for key, route in _normalized_route_map(routes, label).items()
    }


def _public_route_state(state: dict[Any, RouteConfig]) -> list[RouteConfig]:
    """Remove internal planner fields and restore the module's list result."""
    routes = []
    for route in state.values():
        if route.get('present', True):
            public = dict(route)
            public.pop('present', None)
            routes.append(public)
    return [routes_by_key for _key, routes_by_key in sorted((route_key(route), route) for route in routes)]


def _render_static_route_operation(operation: Operation) -> list[str]:
    """Render one exact admitted static-route transition."""
    route = dict(operation.resource)
    route_type = route['route_type']
    if operation.field == 'distance':
        if route_type != 'ipv4':
            raise ReconciliationInputError(
                'IPv6 static-route configuration is not admitted by the command evidence register'
            )
        command = 'ip route {0} {1} {2}'.format(
            route['destination'], route['mask'], route['next_hop']
        )
        if operation.value != 1:
            command += ' {0}'.format(operation.value)
        return [command]
    if operation.field == 'present' and operation.value is False:
        command = _build_no_route_cmd(
            route_type, route['destination'], route['mask'], route['next_hop']
        )
        if not command:
            raise ReconciliationInputError('unsupported static-route type: {0}'.format(route_type))
        return [command]
    raise ReconciliationInputError('unsupported static-route operation: {0}'.format(operation))


def build_lifecycle_plan(
    config: list[RouteConfig], state: str, existing_routes: list[RouteConfig]
) -> ResourcePlan:
    """Build one sealed, minimal static-route transition.

    ``replaced`` deliberately has listed-resource semantics: routes absent from
    desired input are preserved. Distance replacements remain fail-closed until
    the device command/gather evidence can identify a safe deletion scope.
    """
    current = _route_state_for_plan(existing_routes, 'current')
    desired = _normalized_route_map(config, 'desired')
    operations: list[Operation] = []

    if state == 'deleted':
        if not config:
            raise ReconciliationInputError('empty static-route deletion is unsafe; specify exact routes')
        _reject_unadmitted_ipv6(config, 'deletion')
        for key in sorted(desired):
            existing = current.get(key)
            if existing is None:
                continue
            if existing.get('distance', 1) != desired[key].get('distance', 1):
                raise ReconciliationInputError(
                    'cannot safely delete static route with an ambiguous distance: {0}'.format(key)
                )
            operations.append(Operation('set_field', _route_operation_resource(key), 'present', False))
    elif state in ('merged', 'replaced', 'rendered'):
        _reject_unadmitted_ipv6(config, 'configuration')
        for key in sorted(desired):
            existing = current.get(key)
            if existing is not None:
                if existing.get('distance', 1) != desired[key].get('distance', 1):
                    raise ReconciliationInputError(
                        'cannot safely replace static-route distance without an exact delete form: {0}'.format(key)
                    )
                continue
            operations.append(
                Operation('set_field', _route_operation_resource(key), 'distance', desired[key].get('distance', 1))
            )
    else:
        raise ReconciliationInputError('unsupported static-route lifecycle state: {0}'.format(state))

    plan = seal_resource_plan(
        current, operations, STATIC_ROUTE_POLICY, _render_static_route_operation, state
    )
    return ResourcePlan(plan.operations, plan.commands, _public_route_state(plan.after), plan.changed)


def build_lifecycle_commands(
    config: list[RouteConfig],
    state: str,
    existing_routes: list[RouteConfig],
) -> list[str]:
    """Build commands for static route resource lifecycle states."""
    return list(build_lifecycle_plan(config, state, existing_routes).commands)


def build_after_state(
    before: list[RouteConfig],
    desired: list[RouteConfig],
    state: str,
) -> list[RouteConfig]:
    """Build a normalized simulated after-state for static route lifecycle results."""
    return list(build_lifecycle_plan(desired, state, before).after)


def gather_static_routes(module: Any) -> list[RouteConfig]:
    """Gather static route facts required for idempotent diffing."""
    def _gather() -> list[RouteConfig]:
        facts = StaticRoutesFacts(module)
        return facts.facts.get('static_routes', [])

    return gather_with_error_boundary(module, _gather, 'failed to gather static route facts', 'static_routes', [])


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
        # Convert to binary and count.
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
                ),
                route_type=dict(
                    type='str',
                    choices=['ipv4', 'ipv6'],
                    default=None,
                ),
            ),
        ),
        state=dict(
            type='str',
            choices=['merged', 'replaced', 'deleted', 'gathered', 'rendered'],
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

    if state == 'deleted' and not config:
        module.fail_json(msg='empty static-route deletion is unsafe; specify exact routes')

    run_resource_module_lifecycle(
        module=module,
        config=config,
        state=state,
        gather=gather_static_routes,
        build_commands=build_lifecycle_commands,
        build_after=build_after_state,
        mutating_states=('merged', 'replaced', 'deleted'),
        gathered_states=('gathered',),
        rendered_states=('rendered',),
        rendered_current=[],
        apply_config=load_config,
        gather_after_apply=True,
        build_plan=build_lifecycle_plan,
    )


if __name__ == '__main__':
    main()
