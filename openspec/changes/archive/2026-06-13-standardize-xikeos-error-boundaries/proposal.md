## Why

Lower-level transport and facts helpers currently call `module.fail_json` directly, which prevents module entrypoints from adding operation-specific failure context. This is especially problematic when configuration apply succeeds but save or post-apply gather fails, because the top-level module must preserve accurate `changed`, `saved`, and result semantics.

## What Changes

- **BREAKING**: Change collection-owned internal helper APIs so transport and facts layers raise typed Xike OS exceptions instead of calling `module.fail_json` directly.
- Add a standard exception boundary between transport/facts helpers and Ansible module orchestration code.
- Update `xikeos_command`, `xikeos_config`, `xikeos_facts`, and resource module lifecycle paths to catch lower-level exceptions and fail with user-facing context.
- Standardize partial-failure reporting:
  - Apply-start failures report `changed: true` because a non-transactional network CLI may have partially changed the device.
  - Post-apply gather failures fail the task with `changed: true` because the module cannot prove final state.
  - Config save failures after successful apply fail with `changed: true` and `saved: false`.
- Preserve external optional dependency handling for parser libraries such as TextFSM and TTP.
- Preserve Galaxy and ansible-doc import compatibility.

## Capabilities

### New Capabilities
- `xikeos-error-boundaries`: Defines the collection-wide boundary where lower layers raise typed errors and Ansible orchestration layers convert them into module failures.

### Modified Capabilities
- `device-command-execution`: Command and config execution failure behavior gains explicit top-level module context, including save-failure semantics.
- `resource-module-lifecycle`: Resource lifecycle failure behavior gains explicit partial-apply and post-gather failure semantics.

## Impact

- Affected code:
  - `plugins/module_utils/network/xikeos/xikeos.py`
  - new `plugins/module_utils/network/xikeos/errors.py`
  - `plugins/modules/xikeos_command.py`
  - `plugins/modules/xikeos_config.py`
  - `plugins/modules/xikeos_facts.py`
  - resource module lifecycle helpers
  - facts providers under `plugins/module_utils/facts/`
  - resource module `gather_*` wrappers
- Affected APIs:
  - Internal collection helper behavior changes from direct `fail_json` to raised typed exceptions.
  - Public Ansible module options should remain unchanged.
- Tests must cover command failure, config apply failure, save-after-apply failure, facts gather failure, resource apply failure, and post-gather failure results.
