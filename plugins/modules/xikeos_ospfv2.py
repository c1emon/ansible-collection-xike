#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS OSPFv2 resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_ospfv2
short_description: Manage OSPFv2 routing protocol on Xike switches
version_added: "0.1.0"
description:
  - This module provides declarative management of OSPFv2 routing protocol
    configurations on Xike (兮克) switches.
  - Xike uses Cisco IOS-like OSPF commands (router ospf, network, etc.).
options:
  config:
    description: OSPFv2 configuration for a single process
    type: dict
    suboptions:
      process_id:
        description: OSPF process ID
        type: int
        required: true
      router_id:
        description: OSPF router ID (e.g., '1.1.1.1')
        type: str
      networks:
        description: List of network statements to enable OSPF on
        type: list
        elements: dict
        suboptions:
          network:
            description: Network IP address (e.g., '10.0.0.0')
            type: str
            required: true
          wildcard:
            description: Wildcard mask (e.g., '0.0.255.255')
            type: str
            required: true
          area:
            description: OSPF area ID
            type: str
            required: true
      redistribute:
        description: List of redistribution entries
        type: list
        elements: dict
        suboptions:
          protocol:
            description: Protocol to redistribute (static, connected, bgp)
            type: str
            choices: ['static', 'connected', 'bgp']
            required: true
          metric:
            description: Metric for redistributed routes
            type: int
          route_map:
            description: Route-map name to filter redistributed routes
            type: str
      default_info_originate:
        description: Enable default-information originate
        type: bool
        default: false
      default_info_originate_always:
        description: Always advertise default route (requires default_info_originate=true)
        type: bool
        default: false
      default_info_originate_metric:
        description: Metric for default route advertisement
        type: int
      default_info_originate_metric_type:
        description: Metric type (1 for E1, 2 for E2)
        type: int
        choices: [1, 2]
      passive_interfaces:
        description: List of interfaces to make passive (suppress hello packets)
        type: list
        elements: str
        description: Interface names (e.g., 'vlan-interface 10') or 'default' for all
  state:
    description: Desired state of the configuration
    type: str
    default: merged
    choices: ['merged', 'replaced']
author: Andy
"""

EXAMPLES = """
- name: Configure OSPFv2 with network statements
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - network: 10.0.0.0
          wildcard: 0.0.255.255
          area: "0"
        - network: 192.168.1.0
          wildcard: 0.0.0.255
          area: "1"
    state: merged

- name: Configure OSPFv2 with redistribution
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - network: 10.0.0.0
          wildcard: 0.0.255.255
          area: "0"
      redistribute:
        - protocol: static
          metric: 10
        - protocol: connected
          route_map: REDIST-CONNECTED
    state: merged

- name: Configure OSPFv2 with default-information originate
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      default_info_originate: true
      default_info_originate_always: true
      default_info_originate_metric: 100
      default_info_originate_metric_type: 2
    state: merged

- name: Configure OSPFv2 with passive interfaces
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - network: 10.0.0.0
          wildcard: 0.0.255.255
          area: "0"
      passive_interfaces:
        - vlan-interface 10
        - vlan-interface 20
    state: merged

- name: Replace entire OSPFv2 configuration
  xike.xikeos.xikeos_ospfv2:
    config:
      process_id: 1
      router_id: 2.2.2.2
      networks:
        - network: 172.16.0.0
          wildcard: 0.0.255.255
          area: "0"
    state: replaced
"""

RETURN = """
before:
  description: The OSPFv2 configuration prior to the module execution
  returned: when I(state) is C(merged) or C(replaced)
  type: dict
  sample:
    processes:
      '1':
        process_id: 1
        router_id: 1.1.1.1
        networks:
          - network: 10.0.0.0
            wildcard: 0.0.255.255
            area: "0"
after:
  description: The OSPFv2 configuration after the module execution
  returned: when I(state) is C(merged) or C(replaced)
  type: dict
  sample:
    processes:
      '1':
        process_id: 1
        router_id: 1.1.1.1
        networks:
          - network: 10.0.0.0
            wildcard: 0.0.255.255
            area: "0"
commands:
  description: The set of commands pushed to the device
  returned: always
  type: list
  sample:
    - router ospf 1
    - ospf router-id 1.1.1.1
    - network 10.0.0.0 0.0.255.255 area 0
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.xike.xikeos.plugins.module_utils.facts.ospfv2 import (
        Ospfv2Facts,
        parse_running_config,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def _normalize_config(config):
    """Normalize config dict, converting string area IDs to strings consistently."""
    if config is None:
        return {}
    normalized = dict(config)
    if 'networks' in normalized and normalized['networks']:
        normalized['networks'] = [
            {
                'network': n['network'],
                'wildcard': n['wildcard'],
                'area': str(n['area']),
            }
            for n in normalized['networks']
        ]
    return normalized


def _get_existing_process(existing_facts, process_id):
    """Extract the config for a specific OSPF process from facts."""
    processes = existing_facts.get('processes', {})
    proc = processes.get(process_id)
    if proc is None:
        return {}
    return proc


def build_commands(config, existing_config):
    """Build CLI commands to achieve the desired OSPF state.

    Args:
        config: dict with OSPF process configuration
        existing_config: dict of current OSPF configs keyed by process_id

    Returns:
        list: CLI commands to apply
    """
    process_id = config.get('process_id')
    if process_id is None:
        return []

    commands = []
    existing = _get_existing_process(existing_config, process_id)

    # Check if the process already exists
    process_exists = bool(existing)

    # --- Router ospf entry command ---
    commands.append('router ospf {0}'.format(process_id))

    # --- Router ID ---
    desired_rid = config.get('router_id')
    existing_rid = existing.get('router_id')
    if desired_rid and desired_rid != existing_rid:
        commands.append('ospf router-id {0}'.format(desired_rid))

    # --- Networks ---
    desired_networks = config.get('networks') or []
    existing_networks = existing.get('networks') or []
    desired_net_set = {(n['network'], n['wildcard'], str(n['area'])) for n in desired_networks}
    existing_net_set = {(n['network'], n['wildcard'], str(n['area'])) for n in existing_networks}

    for net in desired_net_set - existing_net_set:
        commands.append('network {0} {1} area {2}'.format(*net))

    for net in existing_net_set - desired_net_set:
        commands.append('no network {0} {1} area {2}'.format(*net))

    # --- Redistribute ---
    desired_redist = config.get('redistribute') or []
    existing_redist = existing.get('redistribute') or []
    desired_redist_set = set()
    for r in desired_redist:
        key = (r['protocol'], r.get('metric'), r.get('route_map'))
        desired_redist_set.add(key)
    existing_redist_set = set()
    for r in existing_redist:
        key = (r['protocol'], r.get('metric'), r.get('route_map'))
        existing_redist_set.add(key)

    for r_key in desired_redist_set - existing_redist_set:
        cmd = 'redistribute {0}'.format(r_key[0])
        if r_key[1] is not None:
            cmd += ' metric {0}'.format(r_key[1])
        if r_key[2] is not None:
            cmd += ' route-map {0}'.format(r_key[2])
        commands.append(cmd)

    for r_key in existing_redist_set - desired_redist_set:
        cmd = 'no redistribute {0}'.format(r_key[0])
        commands.append(cmd)

    # --- Default information originate ---
    want_default = config.get('default_info_originate', False)

    # Build desired default-information command string
    desired_default_cmd = None
    if want_default:
        desired_default_cmd = 'default-information originate'
        if config.get('default_info_originate_always', False):
            desired_default_cmd += ' always'
        if config.get('default_info_originate_metric') is not None:
            desired_default_cmd += ' metric {0}'.format(config['default_info_originate_metric'])
        if config.get('default_info_originate_metric_type') is not None:
            desired_default_cmd += ' metric-type {0}'.format(config['default_info_originate_metric_type'])

    # Build existing default-information command string
    existing_default_cmd = None
    if existing.get('default_info_originate', False):
        existing_default_cmd = 'default-information originate'
        if existing.get('default_info_originate_always', False):
            existing_default_cmd += ' always'
        if existing.get('default_info_originate_metric') is not None:
            existing_default_cmd += ' metric {0}'.format(existing['default_info_originate_metric'])
        if existing.get('default_info_originate_metric_type') is not None:
            existing_default_cmd += ' metric-type {0}'.format(existing['default_info_originate_metric_type'])

    if desired_default_cmd and desired_default_cmd != existing_default_cmd:
        commands.append(desired_default_cmd)
    elif existing_default_cmd and not desired_default_cmd:
        commands.append('no default-information originate')

    # --- Passive interfaces ---
    desired_passive = set(config.get('passive_interfaces') or [])
    existing_passive = set(existing.get('passive_interfaces') or [])

    for iface in desired_passive - existing_passive:
        if iface == 'default':
            commands.append('passive-interface default')
        else:
            commands.append('passive-interface {0}'.format(iface))

    for iface in existing_passive - desired_passive:
        if iface == 'default':
            commands.append('no passive-interface default')
        else:
            commands.append('no passive-interface {0}'.format(iface))

    # Remove the 'router ospf <id>' command if no actual changes
    if len(commands) == 1:
        # Only the header, no actual changes
        commands = []

    return commands


def build_delete_commands(config, existing_config):
    """Build CLI commands to remove an OSPF process.

    Args:
        config: dict with process_id
        existing_config: dict of current OSPF configs

    Returns:
        list: CLI commands to apply
    """
    process_id = config.get('process_id')
    if process_id is None:
        return []

    existing = _get_existing_process(existing_config, process_id)
    if not existing:
        return []

    commands = []
    commands.append('router ospf {0}'.format(process_id))

    # Remove all existing networks
    for net in existing.get('networks', []):
        commands.append('no network {0} {1} area {2}'.format(
            net['network'], net['wildcard'], str(net['area']),
        ))

    # Remove redistribute
    for r in existing.get('redistribute', []):
        commands.append('no redistribute {0}'.format(r['protocol']))

    # Remove default-information originate
    if existing.get('default_info_originate', False):
        commands.append('no default-information originate')

    # Remove passive interfaces
    for iface in existing.get('passive_interfaces', []):
        if iface == 'default':
            commands.append('no passive-interface default')
        else:
            commands.append('no passive-interface {0}'.format(iface))

    # Remove router-id
    if existing.get('router_id'):
        commands.append('no ospf router-id')

    # Exit OSPF mode
    commands.append('exit')

    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(
                type='dict',
                options=dict(
                    process_id=dict(type='int', required=True),
                    router_id=dict(type='str'),
                    networks=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            network=dict(type='str', required=True),
                            wildcard=dict(type='str', required=True),
                            area=dict(type='str', required=True),
                        ),
                    ),
                    redistribute=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            protocol=dict(
                                type='str',
                                required=True,
                                choices=['static', 'connected', 'bgp'],
                            ),
                            metric=dict(type='int'),
                            route_map=dict(type='str'),
                        ),
                    ),
                    default_info_originate=dict(
                        type='bool',
                        default=False,
                    ),
                    default_info_originate_always=dict(
                        type='bool',
                        default=False,
                    ),
                    default_info_originate_metric=dict(type='int'),
                    default_info_originate_metric_type=dict(
                        type='int',
                        choices=[1, 2],
                    ),
                    passive_interfaces=dict(
                        type='list',
                        elements='str',
                    ),
                ),
            ),
            state=dict(
                type='str',
                default='merged',
                choices=['merged', 'replaced'],
            ),
        ),
        supports_check_mode=True,
    )

    config = module.params.get('config')
    state = module.params.get('state', 'merged')

    # Normalize area IDs
    if config:
        config = _normalize_config(config)

    # Gather existing facts
    if HAS_FACTS:
        facts = Ospfv2Facts(module)
        existing_config = facts.facts
    else:
        existing_config = {'processes': {}}

    result = {
        'changed': False,
        'commands': [],
        'before': existing_config,
    }

    all_commands = []

    if config is not None:
        if state == 'merged':
            commands = build_commands(config, existing_config)
            all_commands.extend(commands)
        elif state == 'replaced':
            # For replaced, build commands that achieve the desired state
            # This replaces the entire configuration for the given process
            commands = build_commands(config, existing_config)
            all_commands.extend(commands)

            # Additionally remove networks/ redistribution not in desired config
            process_id = config.get('process_id')
            existing = _get_existing_process(existing_config, process_id)
            if existing:
                desired_networks = config.get('networks') or []
                desired_net_set = {(n['network'], n['wildcard'], str(n['area'])) for n in desired_networks}
                existing_net_set = {
                    (n['network'], n['wildcard'], str(n['area']))
                    for n in existing.get('networks', [])
                }
                for net in existing_net_set - desired_net_set:
                    all_commands.append('router ospf {0}'.format(process_id))
                    all_commands.append('no network {0} {1} area {2}'.format(*net))

                desired_redist = config.get('redistribute') or []
                desired_redist_set = {(r['protocol'],) for r in desired_redist}
                existing_redist = existing.get('redistribute', [])
                for r in existing_redist:
                    if (r['protocol'],) not in desired_redist_set:
                        all_commands.append('router ospf {0}'.format(process_id))
                        all_commands.append('no redistribute {0}'.format(r['protocol']))

    # De-duplicate while preserving order (remove consecutive 'router ospf X' if followed by another)
    deduped = _deduplicate_commands(all_commands)

    result['commands'] = deduped

    if module.check_mode:
        module.exit_json(**result)

    result['changed'] = bool(deduped)

    # Refresh facts for 'after'
    if HAS_FACTS and deduped:
        facts_after = Ospfv2Facts(module)
        result['after'] = facts_after.facts
    else:
        result['after'] = existing_config

    module.exit_json(**result)


def _deduplicate_commands(commands):
    """Remove redundant consecutive 'router ospf <id>' lines."""
    if not commands:
        return commands

    deduped = []
    for cmd in commands:
        if deduped and cmd.startswith('router ospf ') and deduped[-1].startswith('router ospf '):
            continue
        deduped.append(cmd)
    return deduped


if __name__ == '__main__':
    main()
