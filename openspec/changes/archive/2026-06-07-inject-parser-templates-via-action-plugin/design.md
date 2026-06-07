## Context

`xikeos_vlans` gathers current state by running `show vlan`, then parsing the output through the VLAN facts parser. The parser now relies on a bundled TextFSM template. During live execution, Ansible wraps modules in an AnsiballZ payload that includes Python module dependencies but can omit non-Python template files. This makes runtime file lookup under `plugins/module_utils/facts/*_templates/` unreliable even when collection build artifacts include those files.

The clean boundary is to load template files on the controller, where the full collection tree is available, and pass template content into the module as internal arguments. The module should not silently fall back to duplicated builtin template strings because that creates drift risk and hides packaging or controller-side loading problems.

## Goals / Non-Goals

**Goals:**

- Load VLAN parser templates on the controller before `xikeos_vlans` module execution.
- Inject template contents through hidden module arguments so AnsiballZ runtime does not need template data files.
- Keep template files as the source of truth for parser behavior.
- Preserve public module arguments, states, results, and normalized VLAN return structures.
- Make missing templates fail explicitly with actionable messages.
- Keep parser helpers reusable for both injected templates and local unit-test/development file loading.

**Non-Goals:**

- Expose parser templates as user-provided module arguments.
- Add a public parsed-output API to `xikeos_command`.
- Rewrite non-VLAN facts parsers as part of this change.
- Remove TTP or TextFSM dependencies.
- Depend on AnsiballZ packaging non-Python resource files.

## Decisions

### Use an action plugin for controller-side template loading

Add `plugins/action/xikeos_vlans.py` to load `show_vlan.textfsm` from the installed collection/source tree and inject its contents into the module invocation.

Alternatives considered:

- Keep builtin template strings in Python: rejected because it duplicates the source of truth and can drift from file templates.
- Rely on collection artifact packaging: insufficient because collection packaging and AnsiballZ module payload packaging are separate phases.
- Require a full installed collection path at module runtime: rejected because network modules execute from temporary AnsiballZ payloads.

### Use hidden internal module arguments

The action plugin will pass template content via internal parameters such as `_textfsm_templates` and, when needed, `_ttp_templates`. These parameters are accepted by the module arg spec but omitted from public documentation.

Alternatives considered:

- Public module options: rejected because parser template selection is not a user-facing API.
- Environment variables: rejected because they are harder to test and more implicit than module arguments.

### Parser helpers prefer injected templates, then local files, then explicit failure

Parser helpers should resolve templates in this order:

1. Template content injected through module args.
2. Local template file path for unit tests and direct local parser use.
3. Explicit `FileNotFoundError` with the template name and expected path.

Embedded builtin fallbacks should be removed.

### Keep Python normalization as the return-contract boundary

TextFSM extracts structured fields and raw port tokens from complex tables. Python remains responsible for final normalization: integer `vlan_id`, active state/status defaults, and `ports` as dictionaries with `name` and `tagged`.

## Risks / Trade-offs

- [Risk] Action plugin loading differs between source checkout and installed collection layouts. → Mitigation: use Ansible action plugin loader context where possible, and test with `ANSIBLE_COLLECTIONS_PATH=.test_path`.
- [Risk] Hidden module arguments might leak into public docs or examples. → Mitigation: keep them out of `DOCUMENTATION` and mark `no_log=True` if appropriate.
- [Risk] Other modules may later need parser template injection. → Mitigation: keep helper signatures generic and use dictionaries keyed by template name.
- [Trade-off] The module gains an action plugin coupling. → This is acceptable because it preserves file templates as source of truth and avoids unreliable runtime file lookup.

## Migration Plan

1. Add action plugin template loading for `xikeos_vlans`.
2. Add hidden `_textfsm_templates` module argument and pass it through `gather_vlans()` to `parse_vlan()`.
3. Update `parse_vlan()` and TextFSM helper to accept injected template content.
4. Update TTP helper with the same injected-template interface for future parser users.
5. Remove builtin template fallback dictionaries.
6. Add tests for action plugin injection, missing-template failure, and local file fallback.
7. Run unit tests and the live playbook path that originally failed.

Rollback: restore file-only template loading or the temporary builtin fallback if action plugin injection fails, while keeping public module behavior unchanged.

## Open Questions

- Should template injection helper logic be shared across future action plugins, or kept local to `xikeos_vlans` until a second module needs it?
- Should hidden template arguments be marked `no_log=True` even though parser templates are not secrets?
