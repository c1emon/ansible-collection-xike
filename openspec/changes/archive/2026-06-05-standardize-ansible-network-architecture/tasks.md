## 1. Platform Plumbing

- [x] 1.1 Add or update collection runtime metadata so `ansible_network_os: xike.xikeos.xikeos` resolves to the Xike OS platform plugins.
- [x] 1.2 Implement `plugins/terminal/xikeos.py` with prompt recognition for user, privileged, global config, interface config, and known sub-mode prompts.
- [x] 1.3 Implement terminal paging disablement and command error detection for invalid, incomplete, ambiguous, and permission-denied responses.
- [x] 1.4 Implement `plugins/cliconf/xikeos.py` with operational `get`, running-config retrieval, configuration edit, device info, and capability methods.
- [x] 1.5 Add unit tests or mocked connection tests for terminal prompt matching, command error matching, and cliconf command/config behavior.

## 2. Command and Config Modules

- [x] 2.1 Refactor `plugins/modules/xikeos_command.py` to execute commands through the Ansible network connection instead of returning empty output.
- [x] 2.2 Ensure `xikeos_command` returns `stdout` and `stdout_lines` aligned with the requested command order.
- [x] 2.3 Ensure `xikeos_command` fails with useful context when the device reports a command error.
- [x] 2.4 Refactor `plugins/modules/xikeos_config.py` to send configuration commands through cliconf.
- [x] 2.5 Implement `xikeos_config` check-mode behavior that reports planned commands without modifying the device.
- [x] 2.6 Validate the save command for the supported Xike OS scope and implement or guard explicit save behavior accordingly.
- [x] 2.7 Add tests for command execution, config execution, check mode, failure handling, and save behavior.

## 3. Reference VLAN Resource Module

- [x] 3.1 Define normalized VLAN state fields for `xikeos_vlans` results and parser output.
- [x] 3.2 Implement or fix VLAN show-output parser using text fixtures and expected structured output.
- [x] 3.3 Refactor `xikeos_vlans` to gather current state from the device and return `before`.
- [x] 3.4 Implement idempotent desired-vs-current diff logic for VLAN create/update/delete operations.
- [x] 3.5 Ensure `xikeos_vlans` sends configuration commands only when changes are required.
- [x] 3.6 Ensure `xikeos_vlans` supports check mode and returns planned commands without modifying the device.
- [x] 3.7 Ensure `xikeos_vlans` returns consistent `before`, `after`, `commands`, and `changed` fields.
- [x] 3.8 Add unit tests for unchanged state, changed state, absent state, parser fixtures, and check mode.

## 4. Documentation and Manual Validation

- [x] 4.1 Update `README.md` inventory and usage examples to use `ansible.netcommon.network_cli` and `xike.xikeos.xikeos`.
- [x] 4.2 Update `docs/architecture.md` to describe the standard terminal/cliconf/network_cli architecture.
- [x] 4.3 Update `docs/development.md` and `docs/faq.md` to distinguish required dependencies from optional references such as Netmiko, TextFSM, Genie, and pyATS.
- [x] 4.4 Correct or replace the `docs/manual_zh.md` sections used by command/config/VLAN implementation.
- [x] 4.5 Document open real-device validation items: prompt variants, error strings, and save command behavior.

## 5. Verification

- [x] 5.1 Run the existing unit test suite and fix regressions.
- [x] 5.2 Run targeted tests for terminal, cliconf, command, config, VLAN parser, and VLAN idempotency behavior.
- [x] 5.3 Run OpenSpec validation for `standardize-ansible-network-architecture`.
- [x] 5.4 Run GitNexus change detection before any commit to confirm affected symbols and execution flows match the intended scope.
