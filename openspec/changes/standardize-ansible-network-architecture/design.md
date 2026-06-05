## Context

`xike.xikeos` is intended to be an Ansible Network Collection for Xike switches. The current repository contains many resource-style modules and documentation, but the runtime path is incomplete: command/config modules mostly generate command lists, several facts modules use `module.run_command()` on the controller instead of the network device, and the collection lacks the standard `terminal` and `cliconf` platform plugins used by `ansible.netcommon.network_cli`.

The target architecture should match the pattern used by established CLI-based Ansible network collections: inventory selects `ansible.netcommon.network_cli`, `ansible_network_os` resolves to this collection's platform plugins, modules call Ansible's network connection helpers, and resource modules gather state from the device before computing idempotent diffs.

Netmiko's Raisecom support and Cisco Genie/pyATS are useful references for prompt handling, parsing style, and fixture-based parser testing. They should not become mandatory runtime dependencies for the first implementation phase.

## Goals / Non-Goals

**Goals:**

- Provide a standard Ansible network platform entry point for Xike OS using `network_cli`, `terminal`, and `cliconf`.
- Make `xikeos_command` and `xikeos_config` execute against real devices through the network connection.
- Establish `xikeos_vlans` as the first reference idempotent resource module.
- Introduce parser and command-generation tests that are independent from physical devices.
- Correct documentation so users configure the collection with the supported architecture.
- Use the Chinese device manual as validation input only where its command structure is reliable or manually corrected.

**Non-Goals:**

- Refactor every existing resource module in this change.
- Add direct Netmiko as the primary Ansible connection backend.
- Add Genie/pyATS as a collection dependency.
- Guarantee full command coverage for the entire Xike OS manual.
- Replace later integration testing on real switches; mock/unit tests cannot fully validate prompts, privilege mode, paging, or save behavior.

## Decisions

### Use `ansible.netcommon.network_cli` as the primary transport

The collection will standardize inventory on:

```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: xike.xikeos.xikeos
```

Rationale: this is the standard architecture for CLI-based Ansible network platforms and lets modules use Ansible's network connection APIs instead of shelling out or executing commands locally.

Alternatives considered:

- Custom `plugins/connection/xikeos.py`: keeps more implementation inside the collection, but duplicates `network_cli` behavior and raises maintenance risk.
- Netmiko backend: useful externally, but creates an extra dependency path and diverges from Ansible network collection conventions.
- NETCONF: not supported by the current evidence and conflicts with the CLI-based modules in the repository.

### Add `terminal` and `cliconf` plugins before resource-module rewrites

The first implementation step is platform plumbing:

- `plugins/terminal/xikeos.py` handles prompts, terminal width/length, privilege mode, config mode prompts, and command error detection.
- `plugins/cliconf/xikeos.py` implements command execution and configuration editing via `network_cli`.
- Runtime metadata maps `xike.xikeos.xikeos` to those plugins.

Rationale: without this layer, every module has to invent its own device execution path.

### Make `xikeos_command` and `xikeos_config` the connection smoke tests

`xikeos_command` should execute operational commands and return stdout/stdout_lines. `xikeos_config` should enter configuration mode through cliconf, send config commands, support check mode, and optionally save running configuration.

Rationale: these modules are the simplest way to verify that the transport and plugin stack works before resource modules depend on it.

### Use `xikeos_vlans` as the first resource-module reference pattern

`xikeos_vlans` will demonstrate the intended pattern:

1. Gather current state with show commands.
2. Parse output into normalized facts.
3. Compare desired and current state.
4. Generate minimal commands.
5. Respect check mode.
6. Return `before`, `after`, `commands`, and `changed` consistently.

Rationale: VLANs are contained enough for a reference module and commonly used enough to validate the architecture.

### Prefer lightweight parsers and fixtures first

Implement parsers as small Python functions/classes in module utilities with text fixtures and expected structured output. TextFSM/TTP/Genie-style patterns may be referenced, but not required.

Rationale: parser correctness is critical, but adding heavy parser dependencies before the base architecture works increases risk and installation burden.

### Treat manual content as validated source material, not executable truth

The generated `docs/manual_zh.md` has malformed headings, code blocks, and tables. The implementation should only rely on manual sections that have been manually checked against the source PDF or real device output.

Rationale: generated manual damage can cause incorrect commands, especially around mode prompts, save commands, and command syntax.

## Risks / Trade-offs

- Device prompts may differ by model, hostname, privilege level, or sub-mode → Support known prompt variants and require real-device validation before broad release.
- Save command may be `copy running-config startup-config` rather than `write memory` → Implement save behavior behind tests and document as an open validation item until confirmed.
- Some modules may continue to be non-functional after the reference path is fixed → Scope this change to command/config/VLANs and document remaining modules as future work.
- Unit tests cannot prove real interactive behavior → Add mocked connection tests now and plan separate integration tests with real switches.
- Standard architecture may break users following current docs → Mark inventory change as breaking and update examples consistently.

## Migration Plan

1. Add runtime metadata, terminal plugin, and cliconf plugin.
2. Update `xikeos_command` and `xikeos_config` to use the network connection path.
3. Add tests for command execution, config execution, error detection, check mode, and save behavior.
4. Refactor `xikeos_vlans` as the reference resource module.
5. Update documentation and examples to the new inventory variables.
6. Leave existing non-reference resource modules in place, but document that broader refactors are follow-up work.

Rollback strategy: revert to the previous documentation and module behavior if `network_cli` plugin resolution fails, or temporarily keep the custom connection plugin as a compatibility path while the standard path is validated.

## Open Questions

- What exact prompts appear on supported Xike switch models in user, enable, global config, interface config, AAA config, VLAN config, and other sub-modes?
- Which command reliably saves running configuration to startup configuration: `write memory`, `copy running-config startup-config`, or both?
- What exact error strings should terminal plugin detect for invalid commands, incomplete commands, ambiguous commands, and permission failures?
- Which software versions and hardware models are in initial support scope?
