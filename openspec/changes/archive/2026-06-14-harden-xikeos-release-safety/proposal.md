## Why

Recent architecture review found several release-blocking safety and packaging risks: `xikeos_command` can still execute guarded mutating commands in check mode, OSPF facts use local command execution with swallowed errors, and Galaxy publishing can include legacy or stale artifacts. This change hardens the collection before the next release without introducing the larger resource reconciler refactor.

## What Changes

- Prevent `xikeos_command` from sending unsafe mutating commands while Ansible check mode is active, even when the unsafe override is enabled.
- Route OSPFv2 facts gathering through the collection network operational command path and surface failures instead of silently returning partial facts.
- Exclude the legacy custom connection plugin from the published collection package so the supported `ansible.netcommon.network_cli` platform path remains the only forward-facing connection model.
- Harden Galaxy release packaging so the workflow publishes the exact tarball for the declared collection version and ignores local caches, build artifacts, and tooling directories.
- Align user and contributor documentation with project conventions: `uv`-managed commands, global `gitnexus analyze`, current version/module counts, and no legacy connection examples.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `xikeos-command-safety`: check mode must never send guarded mutating commands to the device.
- `device-command-execution`: OSPF/resource facts gathering must use the Ansible network operational command path and must not use local controller process execution.
- `ansible-network-platform`: the legacy custom connection plugin must be excluded from the published collection and docs must continue to present `network_cli` as the supported path.
- `galaxy-release-publishing`: release packaging must publish the precise declared-version tarball and exclude stale/local artifacts from the build.

## Impact

- Affected modules/utilities: `plugins/modules/xikeos_command.py`, `plugins/module_utils/facts/ospfv2.py`, `plugins/modules/xikeos_ospf_v2.py` tests around facts behavior.
- Affected packaging/release files: `galaxy.yml`, `.github/workflows/publish-galaxy.yml`, and release validation tests or checks.
- Affected docs: README, development docs, FAQ, module docs, AGENTS guidance, and any examples that mention legacy connection usage or non-`uv` playbook execution.
- No new runtime dependencies are expected.
