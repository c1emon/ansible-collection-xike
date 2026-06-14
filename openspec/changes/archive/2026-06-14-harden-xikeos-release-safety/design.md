## Context

The collection already has a standard Ansible Network platform path based on `ansible.netcommon.network_cli` and collection-owned terminal/cliconf plugins. A strict review found release-safety gaps around four independent areas: command check-mode safety, OSPF facts execution, legacy connection packaging, and Galaxy artifact selection/ignore rules. These issues are release blockers but do not require the planned resource reconciler refactor.

Current constraints:

- Device interaction must go through the collection network connection utilities, not local controller process execution.
- Playbook and release commands should use `uv`-managed execution where applicable.
- `gitnexus` is assumed to be globally available; documentation should not instruct agents or contributors to run it through `npx`.
- The published collection should present `ansible.netcommon.network_cli` plus `ansible_network_os: c1emon.xikeos.xikeos` as the supported connection path.

## Goals / Non-Goals

**Goals:**

- Make `xikeos_command` check mode safe for guarded mutating commands.
- Make OSPFv2 facts gathering use the same network operational command path as other resource facts.
- Keep the legacy custom connection plugin out of the published collection package.
- Ensure the release workflow publishes the exact tarball for the `galaxy.yml` version and does not accidentally package stale artifacts or local tooling state.
- Align release/user/developer documentation with current conventions.

**Non-Goals:**

- Do not implement the reconciler/resource-state refactor in this change.
- Do not introduce `ansible-test sanity` as a required release gate here.
- Do not change the supported primary connection model away from `network_cli`.
- Do not add new runtime dependencies.

## Decisions

### Check mode blocks unsafe command execution

`xikeos_command` should continue rejecting unsafe mutating commands by default. When the unsafe override is enabled, normal execution may still send those commands, but check mode must not send them. The module should return the planned command context and report that a change would occur or that execution was skipped, without calling `run_commands()` for unsafe entries.

Alternative considered: allow unsafe override to bypass check mode. Rejected because check mode is an Ansible safety contract and users reasonably expect it not to mutate devices.

### OSPF facts use network operational execution and explicit errors

`Ospfv2Facts` should gather `show ip ospf` and related output through `run_commands()` from the XikeOS network utility layer. Generic `except Exception: pass` behavior should be removed so facts failures become typed/contextual module failures through existing error boundaries.

Alternative considered: leave OSPF as a best-effort parser that silently returns empty facts. Rejected because silent facts failure corrupts before/after calculations and hides network execution bugs.

### Exclude legacy connection plugin from release packaging

The source file can remain temporarily for compatibility analysis, but the Galaxy build should exclude `plugins/connection/xikeos.py`. User-facing documentation should not present `connection: c1emon.xikeos.xikeos`; examples should use `ansible_connection: ansible.netcommon.network_cli` and `ansible_network_os: c1emon.xikeos.xikeos`.

Alternative considered: delete the file immediately. This may be acceptable later, but excluding it from the published package is the lowest-risk release hardening step.

### Publish the exact declared-version tarball

The release workflow should remove old collection tarballs before build or select the exact expected filename derived from `galaxy.yml` version. It must not use a broad glob plus `head` to choose the artifact. `galaxy.yml` build ignores should exclude collection tarballs, virtualenvs, caches, local test path scaffolding, and agent/tooling directories.

Alternative considered: rely on `--force` and the current working directory being clean. Rejected because local or CI workspace residue can still cause stale artifact selection or package pollution.

### Documentation cleanup is part of release safety

Documentation changes are included because unsafe examples and wrong commands directly affect release usability. Docs should prefer `uv run ansible-playbook`, global `gitnexus analyze`, current version references, and supported connection examples.

## Risks / Trade-offs

- **Risk:** Excluding the legacy connection plugin could surprise users who depended on it from source checkouts. → **Mitigation:** Keep source temporarily if needed, document `network_cli` as the supported path, and verify published metadata/tests still resolve terminal/cliconf plugins.
- **Risk:** Check-mode behavior for unsafe commands could be ambiguous between `changed: true`, `skipped: true`, or failure. → **Mitigation:** Define tests around "no device command is sent" first; choose result fields consistently with existing module behavior.
- **Risk:** OSPF facts may begin failing where they previously returned empty facts. → **Mitigation:** This is intentional for correctness; failures should be contextual and test-covered.
- **Risk:** Release workflow version parsing may become brittle. → **Mitigation:** Use a simple deterministic extraction from `galaxy.yml` and verify the expected tarball exists before publishing.
- **Risk:** Documentation cleanup may be incomplete. → **Mitigation:** Add targeted grep-based verification for legacy connection examples, bare `ansible-playbook`, and `gitnexus analyze` guidance where appropriate.

## Migration Plan

1. Add/adjust unit tests that prove unsafe check-mode commands are not sent.
2. Update OSPF facts execution and tests to use mocked network command utilities.
3. Update packaging ignore rules and release artifact selection.
4. Clean documentation examples and project guidance.
5. Run unit tests and release packaging dry-run validation.

Rollback is straightforward: revert the code/docs/workflow changes. No data migration is involved.

## Open Questions

- Should `xikeos_command` in check mode with unsafe commands return `changed: true` with a warning, or fail fast? The safety requirement is that no command is sent; implementation can choose the clearest Ansible behavior.
- Should the legacy connection plugin also be deleted from source in a later cleanup change after one release cycle?
