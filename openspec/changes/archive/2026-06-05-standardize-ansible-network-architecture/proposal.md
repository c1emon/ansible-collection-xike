## Why

The collection currently documents itself as an Ansible network collection, but its implementation does not follow the standard `ansible.netcommon.network_cli` + `cliconf` + `terminal` architecture used by Cisco IOS-like collections. Most modules generate CLI commands without sending them to the device, so command/config modules and resource modules are not functionally usable against switches.

## What Changes

- **BREAKING**: Standardize inventory examples and runtime behavior on `ansible_connection: ansible.netcommon.network_cli` and `ansible_network_os: xike.xikeos.xikeos`; remove `netconf` and direct Netmiko-as-backend assumptions from the primary architecture.
- Add standard Ansible network platform plumbing for Xike OS:
  - `plugins/terminal/xikeos.py` for prompt/error detection, paging control, and privilege-mode behavior.
  - `plugins/cliconf/xikeos.py` for `get`, `get_config`, `edit_config`, device info, and capabilities.
  - collection runtime metadata needed for the platform.
- Make `xikeos_command` execute show/operational commands through the network connection and return real stdout.
- Make `xikeos_config` push configuration through the network connection, support check mode, save, and command reporting.
- Convert `xikeos_vlans` into the reference resource module pattern: gather facts, compute idempotent diffs, support check mode, execute commands, and return before/after state.
- Fix documentation to match the chosen architecture and isolate Netmiko Raisecom as an external reference for CLI behavior, not the primary Ansible backend.
- Replace the damaged generated `docs/manual_zh.md` with a corrected structure for at least the sections exercised by the reference implementation.
- Establish testing patterns for terminal/cliconf behavior, command/config modules, parser fixtures, and idempotent resource-module diffs.

## Capabilities

### New Capabilities
- `ansible-network-platform`: Defines Xike OS as a standard Ansible `network_cli` platform with terminal and cliconf plugins.
- `device-command-execution`: Defines how modules execute operational and configuration commands on Xike switches.
- `idempotent-resource-modules`: Defines the reference behavior for facts gathering, diffing, check mode, and before/after state in resource modules.
- `validated-command-manual`: Defines the documentation quality bar for command manual content used by implemented modules.

### Modified Capabilities

- None. No existing OpenSpec capabilities are present.

## Impact

- Affected code:
  - `plugins/connection/xikeos.py`
  - `plugins/cliconf/xikeos.py` (new)
  - `plugins/terminal/xikeos.py` (new)
  - `plugins/modules/xikeos_command.py`
  - `plugins/modules/xikeos_config.py`
  - `plugins/modules/xikeos_vlans.py`
  - `plugins/module_utils/facts/vlans.py`
  - shared module utilities and tests
- Affected documentation:
  - `README.md`
  - `docs/architecture.md`
  - `docs/development.md`
  - `docs/faq.md`
  - `docs/manual_zh.md`
- Dependencies and runtime:
  - Requires `ansible.netcommon` as a collection dependency.
  - Netmiko remains optional/reference-only unless a later proposal explicitly chooses a Netmiko-based custom backend.
- User impact:
  - Inventory examples change from `netconf` or custom connection assumptions to `ansible.netcommon.network_cli`.
  - Existing playbooks relying on the documented `netconf` examples must be updated.
