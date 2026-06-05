## 1. Platform Plumbing

- [ ] 1.1 Add or update collection runtime metadata so `ansible_network_os: xike.xikeos.xikeos` resolves to the Xike OS platform plugins.
- [ ] 1.2 Implement `plugins/terminal/xikeos.py` with prompt recognition for user, privileged, global config, interface config, and known sub-mode prompts.
- [ ] 1.3 Implement terminal paging disablement and command error detection for invalid, incomplete, ambiguous, and permission-denied responses.
- [ ] 1.4 Implement `plugins/cliconf/xikeos.py` with operational `get`, running-config retrieval, configuration edit, device info, and capability methods.
- [ ] 1.5 Add unit tests or mocked connection tests for terminal prompt matching, command error matching, and cliconf command/config behavior.

## 2. Command and Config Modules

- [ ] 2.1 Refactor `plugins/modules/xikeos_command.py` to execute commands through the Ansible network connection instead of returning empty output.
- [ ] 2.2 Ensure `xikeos_command` returns `stdout` and `stdout_lines` aligned with the requested command order.
- [ ] 2.3 Ensure `xikeos_command` fails with useful context when the device reports a command error.
- [ ] 2.4 Refactor `plugins/modules/xikeos_config.py` to send configuration commands through cliconf.
- [ ] 2.5 Implement `xikeos_config` check-mode behavior that reports planned commands without modifying the device.
- [ ] 2.6 Validate the save command for the supported Xike OS scope and implement or guard explicit save behavior accordingly.
- [ ] 2.7 Add tests for command execution, config execution, check mode, failure handling, and save behavior.

## 3. Reference VLAN Resource Module

- [ ] 3.1 Define normalized VLAN state fields for `xikeos_vlans` results and parser output.
- [ ] 3.2 Implement or fix VLAN show-output parser using text fixtures and expected structured output.
- [ ] 3.3 Refactor `xikeos_vlans` to gather current state from the device and return `before`.
- [ ] 3.4 Implement idempotent desired-vs-current diff logic for VLAN create/update/delete operations.
- [ ] 3.5 Ensure `xikeos_vlans` sends configuration commands only when changes are required.
- [ ] 3.6 Ensure `xikeos_vlans` supports check mode and returns planned commands without modifying the device.
- [ ] 3.7 Ensure `xikeos_vlans` returns consistent `before`, `after`, `commands`, and `changed` fields.
- [ ] 3.8 Add unit tests for unchanged state, changed state, absent state, parser fixtures, and check mode.

## 4. Documentation and Manual Validation

- [ ] 4.1 Update `README.md` inventory and usage examples to use `ansible.netcommon.network_cli` and `xike.xikeos.xikeos`.
- [ ] 4.2 Update `docs/architecture.md` to describe the standard terminal/cliconf/network_cli architecture.
- [ ] 4.3 Update `docs/development.md` and `docs/faq.md` to distinguish required dependencies from optional references such as Netmiko, TextFSM, Genie, and pyATS.
- [ ] 4.4 Correct or replace the `docs/manual_zh.md` sections used by command/config/VLAN implementation.
- [ ] 4.5 Document open real-device validation items: prompt variants, error strings, and save command behavior.

## 5. Verification

- [ ] 5.1 Run the existing unit test suite and fix regressions.
- [ ] 5.2 Run targeted tests for terminal, cliconf, command, config, VLAN parser, and VLAN idempotency behavior.
- [ ] 5.3 Run OpenSpec validation for `standardize-ansible-network-architecture`.
- [ ] 5.4 Run GitNexus change detection before any commit to confirm affected symbols and execution flows match the intended scope.
