## Context

The collection currently mixes transport, facts parsing, resource lifecycle, and Ansible module result handling. Helpers in `plugins/module_utils/network/xikeos/xikeos.py` and several facts providers call `module.fail_json` directly. That makes failures user-visible too early and prevents higher layers from adding business context such as `changed: true`, `saved: false`, `before`, `after`, and operation-specific messages.

The collection is still maturing, so internal helper API breakage is acceptable. Public module options and Galaxy/ansible-doc compatibility must remain stable.

## Goals / Non-Goals

**Goals:**
- Establish a clear boundary where lower layers raise typed Xike OS errors and Ansible orchestration layers call `module.fail_json`.
- Allow `xikeos_config` to report accurate partial outcomes, especially apply-success/save-failure.
- Ensure resource modules report uncertain device state honestly after apply starts or post-apply gather fails.
- Keep parser/facts failures contextual without silently treating missing facts as empty state.
- Preserve optional external parser dependency behavior for TextFSM and TTP.

**Non-Goals:**
- Do not add a compatibility `fail_on_error` flag.
- Do not redesign public module options.
- Do not replace the Ansible network connection architecture.
- Do not make facts providers completely independent from `AnsibleModule` in this change; they may still receive `module` where needed, but they must not own top-level failure semantics.

## Decisions

### Lower layers raise typed collection errors

Add `plugins/module_utils/network/xikeos/errors.py` with a small hierarchy rooted at `XikeOSError`, including command/config/facts/parse-oriented subclasses.

Rationale: typed errors let modules distinguish command execution, config application, save, facts, and parse failures without catching every `Exception` generically.

Alternative considered: raise raw `ConnectionError` or `ValueError`. This keeps less code but loses consistent context and makes module-level failure handling brittle.

### Transport helpers do not call `module.fail_json`

`run_commands`, `get_config`, `load_config`, and capability helpers should wrap Ansible connection exceptions in typed Xike OS errors and include useful context such as commands where safe.

Rationale: modules such as `xikeos_config` must decide what a transport failure means in the current operation.

Alternative considered: add `fail_on_error=False`. This would preserve compatibility but adds branching behavior to every caller and keeps the old boundary ambiguous.

### Ansible orchestration layers own user-facing failure payloads

Module entrypoints, resource `gather_*` wrappers, and lifecycle helpers may call `module.fail_json` because they know the Ansible task context.

Examples:
- `xikeos_command`: command failed while executing requested commands.
- `xikeos_config`: configuration apply failed, or apply succeeded but save failed.
- `gather_static_routes`: failed to gather static route facts.
- lifecycle helper: apply failed after command execution started, or post-apply gather failed.

Rationale: these layers can attach `changed`, `saved`, `before`, `after`, `commands`, and resource-specific messages.

Alternative considered: make only module `main()` call `fail_json`. That would force every resource module to duplicate lifecycle failure handling rather than centralizing it in the shared lifecycle helper.

### Apply-start failures report `changed: true`

Once a mutating command apply path is entered, resource modules must fail with `changed: true` because Xike OS CLI execution is not modeled as a transaction and the device may be partially changed.

Rationale: this is safer than falsely reporting no change when partial command execution may have occurred.

Alternative considered: `changed: false` for failed apply. This is cleaner for fully transactional systems but misleading for network CLI workflows.

### Post-apply gather failures fail with `changed: true`

If apply succeeds but the module cannot gather final state, the task must fail with `changed: true` because the device was changed but the module cannot satisfy the `after` state contract.

Rationale: returning success without final-state proof weakens idempotent resource module guarantees.

Alternative considered: return success with a warning. This hides an incomplete result contract from automation that depends on the final state.

### Preserve redaction in failure paths

Failure messages and context must avoid leaking sensitive running configuration or command output. Failure payloads should redact values before exposing raw output where applicable.

Rationale: moving failure construction upward can accidentally expose lower-level exception text. Redaction must be applied before `fail_json`.

## Risks / Trade-offs

- [Risk] Internal callers missed during migration may now raise uncaught exceptions. → Mitigation: update all known transport/facts/resource callers and add unit coverage around failure paths.
- [Risk] `changed: true` on apply failure may over-report changes when the first command failed before changing the device. → Mitigation: prefer safe, honest uncertainty for non-transactional CLI and include failure context.
- [Risk] Wrapping exceptions may drop original details. → Mitigation: preserve original message and safe context fields in typed errors.
- [Risk] Failure payloads may leak sensitive output. → Mitigation: route failure payload construction through module-level redaction helpers where output/config may be present.
- [Risk] Facts classes still accepting `module` can blur boundaries. → Mitigation: make `fail_json` ownership the enforceable boundary for this change; pure command-runner injection can be future cleanup.

## Migration Plan

1. Add typed Xike OS exceptions.
2. Change transport helpers to raise typed errors instead of calling `module.fail_json`.
3. Update direct modules (`xikeos_command`, `xikeos_config`, `xikeos_facts`) to catch typed errors and produce contextual failures.
4. Update facts providers to raise errors instead of failing the module directly.
5. Update resource `gather_*` wrappers and lifecycle helper to convert lower-layer errors into Ansible failures with consistent context.
6. Add unit tests for each failure boundary and partial-failure result.
7. Run unit, lint, and ansible-doc/Galaxy-style validation.

Rollback is straightforward before release: revert the internal helper API changes and associated tests. No public module option migration is required.

## Open Questions

- None for initial implementation. The selected semantics are: apply-start failures fail with `changed: true`, and post-apply gather failures fail with `changed: true`.
