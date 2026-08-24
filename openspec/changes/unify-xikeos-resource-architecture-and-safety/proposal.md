## Why

The collection has the right high-level Ansible Network layering, but the implementation is split between a shared reconciler and several module-local diff engines. A current implementation audit reproduced unsafe and non-idempotent behavior: Ansible-normalized omitted fields can be interpreted as removals, identical `replaced` route and ACL input is deleted and recreated, check-mode `after` state can claim resources disappeared without matching commands, common credentials escape redaction, static-route distance parsing drifts, the local test harness breaks after a checkout move, and the release workflow can publish while Ansible sanity validation fails.

This change finishes the architectural convergence before more mutating resource modules are added.

## What Changes

- Define one presence-aware input normalization boundary and one canonical resource planning pipeline for core lifecycle modules.
- Treat Ansible-normalized `None` values as omitted fields; use explicit empty collections for set clearing and require typed reset/delete semantics for scalar removal.
- Reconcile semantic operations, require the module renderer to consume every operation, and seal one immutable resource plan containing operations, rendered commands, simulated after-state, and truthful change status.
- Standardize `merged` as non-destructive and `replaced` as synchronization of explicitly declared fields on listed resources; preserve unlisted resources. Global removal remains reserved for future `overridden`/`purged` states.
- Migrate and repair the seven core lifecycle families: VLANs, interfaces, L2 interfaces, L3 interfaces, LAG interfaces, static routes, and ACLs.
- Correct static-route identity and administrative-distance parsing, and make route/ACL replacement minimal and idempotent.
- Gate every newly introduced or semantically changed mutating command transition on reviewed command/gather evidence; fail closed or retain non-mutating preview behavior when evidence is insufficient.
- Centralize result and failure redaction, cover common XikeOS credential syntax, and reject compound/multiline commands that could bypass the read-only command guard.
- Make unit tests exercise real Ansible argument normalization, make collection import scaffolding relocatable, add pre-release CI, and require Ansible sanity validation before Galaxy publication.
- Resolve the existing `validate-modules` failures and align module documentation with argument and return contracts.

## Capabilities

### New Capabilities

- `collection-implementation-validation`: relocatable test setup, real Ansible parameter-boundary tests, pre-release CI, and Ansible sanity gates.

### Modified Capabilities

- `resource-reconciliation-planning`: canonical normalized input, omission semantics, richer field/resource policies, one plan object, and deterministic after-state.
- `resource-module-lifecycle`: every core mutating module uses the shared planning pipeline and truthful state semantics.
- `idempotent-resource-modules`: module-specific regression contracts for L3/LAG omission, interface/L2 replacement, static routes, ACLs, and VLAN replacement compatibility.
- `xikeos-command-safety`: compound-command rejection and comprehensive result redaction.
- `xikeos-error-boundaries`: all returned failure context is sanitized at the orchestration boundary.
- `galaxy-release-publishing`: replace the prior explicit sanity exclusion with mandatory pre-publish sanity validation.
- `validated-command-manual`: evidence admission for changed resource mutation syntax, removal forms, command modes, and round-trip gathering.

## Impact

- Expected implementation areas: `plugins/module_utils/network/xikeos/reconcile.py`, `lifecycle.py`, `safety.py`, error helpers, facts parsers, and all core lifecycle modules.
- Expected validation areas: unit tests, Ansible parameter-boundary tests, `ansible-test sanity`, release/CI workflows, module documentation, and developer setup documentation.
- `replaced` behavior for modules that currently remove unlisted resources is intentionally standardized; migration notes and regression tests are required because this is an externally visible semantic correction.
- No new runtime dependency is planned.
- Specialty modules remain non-mutating `rendered-only` until separate changes define safe gather/diff/apply contracts.
- Software tests do not establish physical XikeOS command compatibility; live device validation remains separately evidenced.
- Public behavior corrections require a changelog fragment in this change; the exact new, never-published collection version remains a release-time decision and must match all release metadata and tags.
