## 1. Audit Regressions and Validation Baseline

- [x] 1.1 Add a regression test that passes L3 `replaced` input through Ansible argument validation, omits IPv6, and proves no IPv6 removal is planned.
- [x] 1.2 Add a regression test that passes LAG `merged` input through Ansible argument validation with only members and proves omitted mode/LACP fields neither fail nor render removals.
- [x] 1.3 Add no-op `replaced` regressions for identical static routes and ACLs, asserting empty commands and `changed: false`.
- [x] 1.4 Add check-mode regressions proving base-interface and L2 `after` state preserves unlisted resources and matches the rendered operations.
- [x] 1.5 Add static-route parser regression coverage for Cisco-style `[administrative-distance/metric]` output and multiple next hops for the same prefix.
- [x] 1.6 Add synthetic-secret regressions for username privilege/password, radius/tacacs host keys, config responses, command lists, and failure details.
- [x] 1.7 Add command-safety regressions for newline/compound input, non-positive retries, and proof that invalid input never reaches `run_commands()`.
- [x] 1.8 Capture the complete current `ansible-test sanity` failure baseline without adding broad ignores.
- [x] 1.9 Inventory every positive, removal, reset, mode, ordering, and verification behavior that this change would introduce or semantically alter across the seven core resource families; classify current code/tests and unreviewed converted manual text as software baseline rather than device evidence.
- [x] 1.10 Create the mutation evidence register with reviewed source excerpts or model/firmware-scoped device transcripts, exact render forms, and bounded gather observations; record each uncovered transition as fail-closed or byte-for-byte legacy preservation before its migration wave begins.
- [x] 1.11 Resolve static-route distance removal/add scope and select the ACL sequenced or positional model from admitted evidence before implementing either policy.

## 2. Canonical Input and Resource Plan Foundation

- [x] 2.1 Add a shared desired-input normalizer that strips optional `None` values while preserving explicit empty collections and false/zero values.
- [x] 2.2 Add canonical current-state validators for resource identity, field shape, value type, and module-owned schema.
- [x] 2.3 Make duplicate resource identities and duplicate set/rule identities fail with safe resource/field context.
- [x] 2.4 Extend reconciliation policies for explicit resource existence and ordered collections required by VLANs and ACLs.
- [x] 2.5 Keep the reconciler pure by producing deterministic semantic operations and candidate simulated after-state without CLI strings or device access.
- [x] 2.6 Add atomic sealed `ResourcePlan` construction containing operations, renderer acknowledgements, deterministic commands, simulated after-state, and state-aware changed status.
- [x] 2.7 Ensure planning fails before CLI rendering for unknown fields, malformed identities, unsupported removals, and unsafe reset requests.
- [x] 2.8 Audit nested argument-spec defaults and remove or explicitly contract-test action-causing defaults such as base-interface `enabled: true`.
- [x] 2.9 Make plan sealing reject unconsumed operations, empty/ambiguous mutating render results, extra commands not attributable to operations, and partial renderer output.
- [x] 2.10 Add focused unit tests for omission, explicit empty, false/zero preservation, ordering, duplicates, resource operations, pure-plan determinism, complete renderer consumption, rendered-preview `changed: false`, and sealed-plan invariants.

## 3. Lifecycle Integration

- [x] 3.1 Refactor the shared lifecycle helper to consume only a sealed `ResourcePlan` instead of independently computing commands and simulated after-state.
- [x] 3.2 Make mutating/check-mode `commands`, `changed`, and `after` derive from acknowledged operations in the same sealed plan while preserving `changed: false` for non-mutating `rendered` previews.
- [x] 3.3 Preserve post-apply gather as the authoritative non-check-mode `after` state where supported.
- [x] 3.4 Preserve typed partial-change and post-apply verification failure semantics while routing payloads through shared sanitization.
- [x] 3.5 Add lifecycle tests for no-op, check mode, apply success, partial apply failure, and post-apply gather failure using a single plan.

## 4. L3 and LAG Repair

- [x] 4.1 Update L3 normalization so Ansible-inserted `ipv4=None` or `ipv6=None` is omitted and explicit empty lists remain clear requests in `replaced`.
- [x] 4.2 Verify L3 `merged`, `replaced`, `rendered`, simulated after-state, unlisted-interface preservation, and duplicate-address rejection through the new plan.
- [x] 4.3 Update LAG normalization so omitted mode, LACP mode, and members are no-ops; remove null-as-unset behavior.
- [x] 4.4 Define and test any supported explicit LAG scalar reset operation; otherwise reject it clearly without rendering commands.
- [x] 4.5 Verify additive members, listed-trunk replacement, member-order idempotency, and unlisted-trunk preservation.
- [x] 4.6 Remove legacy L3/LAG command/after planning paths after the plan-backed paths pass the full regression suite.

## 5. Base Interface and L2 Migration

- [x] 5.1 Define canonical scalar policies and safe reset capabilities for base interface description, speed, duplex, enabled, and MTU fields.
- [x] 5.2 Migrate base-interface command rendering and after-state to the shared plan.
- [x] 5.3 Define canonical L2 policies for mode, PVID, access, trunk, and hybrid VLAN fields, including device-safe reset limitations.
- [x] 5.4 Migrate L2 command rendering and after-state to the shared plan.
- [x] 5.5 Add regressions proving `merged` and `replaced` preserve unlisted interfaces, omitted fields are no-ops, and check-mode after-state exactly applies planned operations.
- [x] 5.6 Remove module-local state branches that duplicate reconciler semantics.

## 6. Static Route Migration

- [x] 6.1 Correct Cisco-style route parsing to preserve administrative distance and distinguish it from metric.
- [x] 6.2 Canonicalize route masks/prefixes and use `(route_type, destination, mask, next_hop)` as route identity.
- [x] 6.3 Model administrative distance as a compared field and render a remove/add transition only when its exact positive, removal, and scope behavior is admitted; otherwise fail before rendering.
- [x] 6.4 Preserve multiple next hops for the same prefix in gathering, diffing, deletion, and after-state.
- [x] 6.5 Replace unconditional delete-all/re-add `replaced` behavior with minimal listed-resource reconciliation.
- [x] 6.6 Add identical-state, ECMP, distance-change, IPv4/IPv6, delete, rendered, and check-mode regressions.

## 7. VLAN Migration

- [x] 7.1 Define VLAN resource identity, configurable fields, resource create/delete operations, and VLAN 1 protection in policy-backed planning.
- [x] 7.2 Migrate VLAN merged/replaced/deleted/rendered command and after-state generation to the shared plan.
- [x] 7.3 Change VLAN `replaced` to listed-resource synchronization and preserve unlisted VLANs; document the compatibility correction.
- [x] 7.4 Preserve parser-template injection and fail-closed current-state gathering.
- [x] 7.5 Add name omission, explicit supported reset, suspended-state rejection, VLAN 1 protection, no-op, and check-mode regressions.

## 8. ACL Migration

- [x] 8.1 Implement the evidence-selected ACL model: sequence identity and numeric order only when sequence round-trips, otherwise positional comparison with non-empty sequence rejected.
- [x] 8.2 Implement ACL-level and rule-level remark ownership only when both render and gather syntax are admitted; otherwise remove action-causing empty defaults and reject non-empty remark input instead of silently ignoring it.
- [x] 8.3 Migrate ACL merged/replaced/deleted/rendered planning and after-state to the shared ordered policy.
- [x] 8.4 Replace unconditional ACL delete/recreate with no-op detection and the smallest evidence-admitted whole-ACL or granular transition supported by the selected ACL model.
- [x] 8.5 Preserve unlisted ACLs in `replaced` and require future `overridden` semantics for global removal.
- [x] 8.6 Add rule order, sequence, remark, identical-state, rule add/remove, protected failure, and check-mode regressions.

## 9. Result Redaction and Command Safety

- [x] 9.1 Extend redaction to username modifier/password forms, radius/tacacs host key forms, SNMP communities, key strings, pre-shared keys, and multiline values.
- [x] 9.2 Add shared sanitization helpers for success results, check-mode results, warnings, typed errors, generic exception details, and partial-change payloads.
- [x] 9.3 Apply sanitization to `xikeos_command`, `xikeos_config`, facts results, resource lifecycle results, and all matching failure paths.
- [x] 9.4 Preserve safe command/resource context while proving synthetic secret values never appear in returned nested payloads.
- [x] 9.5 Reject command entries containing newlines or unsupported compound separators before mutating-prefix classification.
- [x] 9.6 Validate `retries > 0` and `interval >= 0` before any device call, and add wait-condition edge-case coverage.
- [x] 9.7 Audit generic command/config inputs and any future credential-specific options for appropriate Ansible `no_log` handling in addition to returned-payload sanitization.

## 10. Relocatable Tests and Ansible-Native Validation

- [x] 10.1 Replace the persistent absolute `.test_path` symlink setup with relocatable, stale-link-safe collection import scaffolding.
- [x] 10.2 Add tests that run from a checkout path different from the original creation path.
- [x] 10.3 Add reusable helpers that pass module input through Ansible argument validation before lifecycle assertions.
- [x] 10.4 Convert omission-sensitive module tests to the Ansible-normalized test path.
- [x] 10.5 Keep test and dependency setup uv-managed and update developer documentation to remove manual `python -m venv` guidance.

## 11. Sanity, CI, and Release Gates

- [x] 11.1 Establish one finite machine-readable matrix of supported Python minor and compatible `ansible-core` series combinations from currently resolvable upstream-supported combinations.
- [x] 11.2 Align `pyproject.toml`, `meta/runtime.yml`, the uv lock, README, architecture/support documentation, and workflow declarations so none claims controller combinations outside the matrix.
- [x] 11.3 Add a non-publishing validation workflow for pull requests and protected-branch pushes.
- [x] 11.4 Run uv-managed unit tests and required Ansible sanity gates for every support-matrix entry, plus strict OpenSpec validation and collection build checks in validation CI.
- [x] 11.5 Fix shared GPL-compatible module headers, import ordering, author metadata, and documentation schema errors reported by `validate-modules`.
- [x] 11.6 Fix module-specific argument/default/choice/return documentation mismatches without exposing internal injected parameters as public API.
- [x] 11.7 Make the release workflow require the same matrix and validation gates before Galaxy publication and remove the prior sanity exclusion.
- [x] 11.8 Verify the built tarball contains required plugins/templates and excludes legacy/local/test artifacts.

## 12. Documentation and Compatibility

- [x] 12.1 Update the architecture document with the canonical input/plan/render/lifecycle/sanitization pipeline.
- [x] 12.2 Update the module support matrix and state semantics for all core lifecycle modules.
- [x] 12.3 Add migration notes for standardized `replaced` behavior and removal of null-as-unset semantics.
- [x] 12.4 Document explicit reset/delete capabilities and unsupported removals for each core module.
- [x] 12.5 Keep specialty modules documented as `rendered-only` and separate software validation from physical-device evidence.
- [x] 12.6 Update `docs/validation_items.md` and the manually reviewed command reference with the mutation evidence register, including model/firmware scope and explicit unsupported transitions.
- [x] 12.7 Add a changelog fragment naming affected modules and explaining the `replaced` and null/reset compatibility corrections; document that publication requires a new version rather than reuse of an immutable Galaxy version.

## 13. Final Verification

- [x] 13.1 Run all focused regression suites after each migration wave.
- [x] 13.2 Run the full unit suite in a fresh relocatable checkout with declared collection dependencies.
- [x] 13.3 Run full unit and required `ansible-test sanity` gates for every authoritative support-matrix entry with zero unapproved findings.
- [x] 13.4 Run `ansible-lint`, strict OpenSpec validation, collection build, and artifact-content inspection.
- [x] 13.5 Verify every semantically changed mutating operation has admitted command/gather evidence or a tested fail-closed outcome, and verify every sealed plan accounts for every operation and command.
- [ ] 13.6 Run read-only live-device validation for admitted gather/check-mode paths when a supported SKS8300 target is available; record it separately from software evidence. (No supported target was supplied; this remains explicitly outside software-only validation.)
- [x] 13.7 Verify the changelog fragment is present and release automation rejects inconsistent or reused version, tag, artifact, and generated-changelog metadata.
- [x] 13.8 Reconcile every audit and spec-review finding to a passing regression, admitted evidence record, or explicit documented non-goal before requesting archive/release.
