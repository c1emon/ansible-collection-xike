## Context

The supported execution path is already well layered: playbooks select `ansible.netcommon.network_cli`, terminal/cliconf plugins own the network platform behavior, facts providers gather current state, resource modules render XikeOS commands, and the lifecycle helper owns check/apply/verify control flow. The architectural defect is inside the resource boundary: state semantics, omission handling, diffing, simulated after-state, and sanitization are not consistently centralized.

The existing reconciler proved the value of semantic operations, but it consumes ordinary dictionaries after Ansible has inserted `None` for missing nested options. At that point an omitted scalar and an explicit YAML null are indistinguishable. Other core modules still use independent builders, so `replaced` ranges from listed-resource synchronization to unconditional delete-and-recreate.

## Goals / Non-Goals

**Goals:**

- Establish one canonical pipeline from validated Ansible parameters to normalized desired/current state, semantic plan, CLI rendering, lifecycle execution, and sanitized result.
- Make omission, empty collection, reset, replacement scope, and resource identity explicit and testable.
- Make all seven core resource families idempotent under real Ansible parameter normalization.
- Ensure planned commands and simulated `after` state are produced from the same plan.
- Make security redaction and command classification collection-wide boundaries rather than optional caller behavior.
- Prevent release publication unless unit, OpenSpec, collection build, and Ansible sanity gates pass.

**Non-Goals:**

- Do not add mutating support to OSPF, STP, ERPS, EAPS, QinQ, mirror, port-isolate, or flex-monitor-link modules.
- Do not add `overridden` or `purged` until each resource family defines safe global removal semantics.
- Do not replace module-specific CLI renderers with a universal CLI generator.
- Do not access private Ansible raw-argument internals to recover whether YAML null was explicitly written.
- Do not treat simulator, parser golden, or unit evidence as physical-device validation.

## Decisions

### Use a single canonical resource pipeline

Core resource execution will follow:

`Ansible params -> desired normalizer -> canonical current/desired state -> pure reconciler -> semantic operations -> module renderer -> sealed ResourcePlan -> lifecycle apply/verify -> sanitized result`.

Facts providers remain module-specific, but their output must pass the same canonical-state validator used for desired input. CLI rendering remains resource-specific because interface context, route syntax, and ordered ACL rules are device semantics.

### Treat None as omitted at the public module boundary

After Ansible validation, missing nested fields are populated with `None`. The collection will therefore strip `None` from optional resource fields before planning. It will not interpret null as a removal request.

- Omitted or normalized-`None` field: no ownership request and no operation.
- Explicit empty set/list in `replaced`: clear that listed resource field when removal is supported.
- Explicit non-empty value: converge that field.
- Scalar removal: available only through an explicit typed reset/delete contract defined by that resource module; otherwise fail closed or remain unsupported.

This intentionally supersedes the earlier LAG decision that `lacp_mode: null` removes LACP mode. Depending on private Ansible raw input to distinguish null from omission was rejected as unstable.

### Seal one immutable ResourcePlan after complete rendering

The pure reconciler produces deterministic semantic operations and a candidate simulated after-state without device access or CLI knowledge. The module-owned pure renderer must then acknowledge every operation and atomically seal one `ResourcePlan` containing at least:

- canonical semantic operations;
- deterministic rendered commands;
- deterministic simulated after-state;
- mutating/check-mode changed status derived from the rendered command list;
- safe resource/field context for planning errors.

Every operation must be acknowledged by the renderer. If any operation is unsupported, silently dropped, or produces an empty/ambiguous mutation, plan sealing fails and no partial plan is returned. For mutating and check-mode execution, non-empty operations, non-empty commands, `changed: true`, and the simulated transition must agree. `state=rendered` may return preview commands while keeping Ansible result `changed: false`, because it never applies configuration. The lifecycle helper consumes only the sealed plan and must not independently call separate command or after-state diff functions.

### Extend policies only for proven core needs

The reconciler will support:

- scalar fields;
- identity-based unordered sets;
- ordered collections for ACL rules, with an explicit stable rule identity/order policy;
- resource create/delete operations where the module safely owns resource existence;
- explicit removal capability flags and typed reset renderers.

Unknown policy fields, missing identities, duplicate resource identities, and duplicate set/rule identities must fail before commands are rendered. Policies remain separate from CLI renderers and do not become a second copy of the Ansible argument schema.

### Standardize resource-state semantics

- `merged`: converge explicitly declared values and add desired set items; preserve current-only items and unlisted resources.
- `replaced`: synchronize explicitly declared owned fields for listed resources; preserve omitted fields and unlisted resources.
- `deleted`: delete only explicitly listed resource identities and fail closed for protected/default resources.
- `rendered`: plan from a defined empty/synthetic current state without device access.
- `overridden`/`purged`: reserved for future explicit global-removal contracts.

Any existing global behavior currently named `replaced` must be migrated to these semantics and documented as a compatibility correction. The change must not silently retain two meanings for the same state.

### Admit device mutation semantics before changing renderers

Existing source code, parser fixtures, and unit tests establish a software behavior baseline but do not prove XikeOS command compatibility. Before this change introduces or semantically alters a mutating transition, an evidence register must admit the exact positive/removal command forms, required CLI mode, ordering/atomicity constraints, and gather output needed to verify the result. Admission requires either a manually reviewed authoritative source excerpt or a captured device transcript with model and firmware context.

If evidence is insufficient, the mutating/check-mode transition must fail before commands are returned or applied. A module may retain explicitly documented non-mutating `rendered` preview behavior, but that preview remains software-only evidence and must not be described as device validated. A refactor may preserve a pre-existing command sequence byte-for-byte without expanding its compatibility claim; any changed command, order, removal scope, or reset behavior requires its own admission.

ACL migration uses one of two evidence-selected models:

- **Sequenced model:** sequence values round-trip through gather output, sequence is the rule identity, and numeric sequence defines order.
- **Positional model:** gathered device order is authoritative, rule values are compared positionally, unsupported sequence/remark inputs fail explicitly, and a changed ACL uses only an evidence-admitted whole-ACL or granular transition.

ACL-level and rule-level remarks are owned only if their render and gather syntax is independently admitted. Static-route distance changes likewise use remove/add only after both forms and their scope are admitted; otherwise the transition fails closed.

### Migrate core modules in dependency order

1. Establish the mutation evidence register and admission decisions for every changed core transition.
2. Fix the common normalizer, policy validation, renderer-completeness invariant, sealed `ResourcePlan`, and lifecycle integration.
3. Repair L3/LAG first because they already use the reconciler and contain the reproduced omission bug.
4. Migrate base interfaces and L2 interfaces to eliminate command/after divergence.
5. Migrate static routes with composite identity `(route_type, destination, mask, next_hop)` and distance as a compared field; preserve ECMP entries.
6. Migrate VLAN resource existence and protected VLAN 1 semantics.
7. Migrate ACLs last because ordered rules, sequence behavior, remarks, and replacement require the richest policy.

At each wave, contract tests must pass before the next module family is migrated.

### Make redaction an orchestration-boundary invariant

Introduce shared sanitization for successful results, check-mode results, warnings, and failure payloads. Modules may retain non-sensitive command context, but secret tokens in commands, responses, configuration text, exception details, and partially changed context must be replaced with the redaction marker.

Redaction coverage must include credential tokens that appear after optional modifiers, including username privilege/password forms and radius/tacacs host key forms. Tests must use synthetic secrets and assert they are absent from every returned payload.

`xikeos_command` must reject newline/compound command entries before prefix classification. Retry counts must be positive, and invalid wait parameters must fail before network execution.

### Separate pre-release validation from publication

A non-publishing validation workflow will run for pull requests and protected-branch pushes. The release workflow will depend on equivalent gates before building/publishing:

- unit tests in a fresh checkout layout;
- real Ansible argument normalization regressions;
- strict OpenSpec validation;
- `ansible-test sanity` for the supported Python version(s);
- collection build and artifact-content checks.

The previous contract that explicitly excluded sanity from release validation is removed. Existing `validate-modules` findings must be fixed rather than skipped through broad ignore files. Narrow, documented exclusions are allowed only for intentional internal parameters when supported by Ansible conventions.

The collection will define one finite, machine-readable controller support matrix. Its entries, rather than open-ended `>=` prose alone, are the authoritative supported Python minor and compatible `ansible-core` series combinations. CI must test every matrix entry, and `pyproject.toml`, `meta/runtime.yml`, the uv lock, README/support documentation, validation CI, and release CI must not claim a broader range than that matrix.

This change must add a changelog fragment classifying the `replaced` and null/reset corrections as externally visible compatibility changes. It must not overwrite an already published collection version. The exact next version is selected at release time, when `galaxy.yml`, visible version documentation, generated changelog, artifact name, Git tag, and GitHub Release must be reconciled to the same new version.

## Risks / Trade-offs

- **Breaking state semantics:** Existing users may rely on global `replaced`. Mitigation: document the correction, add before/after examples, and reserve global removal for future `overridden`.
- **Planner scope growth:** Ordered ACLs and resource operations increase complexity. Mitigation: add only field kinds required by migrated modules and keep CLI rendering module-owned.
- **Parser uncertainty:** Current facts may not expose enough identity/order information. Mitigation: fail closed and keep a module rendered-only if canonical current state cannot be proven.
- **Command-evidence gaps:** Current code and converted manual chapters can appear more authoritative than they are. Mitigation: require operation-level admission and treat unreviewed converted text and software fixtures as non-device evidence.
- **Redaction overreach:** Broad patterns can hide harmless data. Mitigation: preserve command keywords/resource identities while redacting credential operands.
- **Sanity cleanup breadth:** Current validation has many failures. Mitigation: establish a baseline task, fix shared documentation/license patterns mechanically, then resolve remaining module-specific mismatches.

## Migration Plan

1. Add failing regression tests that reproduce every audit finding using real Ansible normalization where applicable.
2. Inventory changed mutating operations, admit their command/gather evidence, and record fail-closed decisions for unsupported transitions.
3. Implement canonical normalization, pure semantic reconciliation, complete renderer consumption, and sealed `ResourcePlan` construction.
4. Integrate the lifecycle helper with the sealed plan and sanitized result boundaries.
5. Migrate core module families in the dependency order above, preserving a passing full suite after each wave.
6. Harden command safety and redaction across command/config/facts/resource failures.
7. Replace persistent absolute test links, establish the finite support matrix, add CI, fix sanity findings, and enable release gates.
8. Add the changelog fragment and update support, state-migration, and operator documentation.

Rollback must be change-scoped by migration wave. Do not leave one module with partially mixed old/new planning paths. No persisted data migration is involved.

## Resolved Questions

- YAML/null does not mean scalar removal; normalized `None` is treated as omitted.
- `replaced` is listed-resource synchronization, not global removal.
- Static-route identity includes next hop so ECMP routes remain distinct; administrative distance is a compared value whose change renders remove/add only when the exact transition is evidence-admitted.
- ACLs use an evidence-selected sequenced or positional model; unsupported sequence or remark ownership fails explicitly rather than being ignored.
- A final `ResourcePlan` is sealed only after the renderer acknowledges every semantic operation; mutating changed status, commands, and simulated after-state cannot diverge.
- The release gate includes Ansible sanity validation and does not defer existing findings.
- Supported Python/Ansible combinations are exactly the finite CI matrix, and compatibility corrections ship with a changelog fragment under a new release version.
