## 1. Safety and Baseline

- [ ] 1.1 Run GitNexus impact analysis for each symbol before editing it, including transport helpers, module entrypoints, lifecycle helpers, and facts provider methods.
- [ ] 1.2 Run the current unit test baseline with `uv run pytest tests/unit -q` and note existing failures, if any.
- [ ] 1.3 Identify all current lower-layer `module.fail_json` call sites in transport helpers and facts providers.

## 2. Typed Error Foundation

- [ ] 2.1 Add `plugins/module_utils/network/xikeos/errors.py` with `XikeOSError` and typed command, config, facts, parse, and connection subclasses.
- [ ] 2.2 Include safe contextual fields on typed errors, such as commands and redacted detail where appropriate.
- [ ] 2.3 Add unit coverage for typed error string/detail behavior.

## 3. Transport Boundary

- [ ] 3.1 Update `get_capabilities`, `run_commands`, `get_config`, and `load_config` to raise typed Xike OS errors instead of calling `module.fail_json`.
- [ ] 3.2 Preserve Ansible network connection behavior and command/config execution semantics.
- [ ] 3.3 Update transport-related tests to expect raised typed errors from helpers.

## 4. Direct Module Error Handling

- [ ] 4.1 Update `xikeos_command` to catch typed command/connection errors and fail with command-module context.
- [ ] 4.2 Update `xikeos_config` to catch config apply errors, fail with apply context, and avoid save after failed apply.
- [ ] 4.3 Update `xikeos_config` save handling so apply-success/save-failure returns `failed: true`, `changed: true`, and `saved: false`.
- [ ] 4.4 Update `xikeos_facts` to catch typed lower-layer errors and fail with subset/resource gather context.
- [ ] 4.5 Ensure failure payloads use existing redaction behavior for sensitive output/config values.

## 5. Facts Provider Boundary

- [ ] 5.1 Update facts providers under `plugins/module_utils/facts/` so collection-owned parsing/gathering failures raise typed errors instead of calling `module.fail_json`.
- [ ] 5.2 Preserve friendly runtime failures for optional external parser dependencies such as TextFSM and TTP.
- [ ] 5.3 Add or update tests for facts command failures and parser failures.

## 6. Resource Lifecycle and Gather Wrappers

- [ ] 6.1 Update resource `gather_*` wrappers to catch typed facts/parse/command errors and fail with resource-specific gather context.
- [ ] 6.2 Update `run_resource_module_lifecycle` so apply-start failures fail with `changed: true`, attempted commands, and partial-change context.
- [ ] 6.3 Update `run_resource_module_lifecycle` so post-apply gather failures fail with `changed: true` and final-state-verification context.
- [ ] 6.4 Add or update tests for resource gather failure, apply failure, and post-gather failure semantics.

## 7. Validation

- [ ] 7.1 Run `uv run pytest tests/unit -q`.
- [ ] 7.2 Run the repository's lint command, including Ruff/ansible-lint paths used by the collection.
- [ ] 7.3 Run ansible-doc/Galaxy-style documentation checks for affected modules and plugins.
- [ ] 7.4 Run `gitnexus_detect_changes()` before any commit to confirm affected symbols and execution flows match the intended scope.
