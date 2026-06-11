## Context

The collection currently parses Xike OS command output with parser-specific Python logic in `plugins/module_utils/facts/*.py`. Table-oriented commands such as `show vlan brief` are parsed with a mix of header skipping, regular expressions, and manual field splitting. This works for the current samples, but it duplicates parsing mechanics across files and makes future parser additions harder to review.

The first migration target is `parse_vlan_brief()` because it has a small return contract, existing unit coverage, and is used by both VLAN facts gathering and the `xikeos_vlans` resource module's current-state gathering path. Impact analysis found low risk for the parser symbol, with one direct indexed caller in VLAN facts flow.

TTP will be used only as an internal parser implementation detail. Module arguments, result keys, facts structures, and resource module behavior remain unchanged.

## Goals / Non-Goals

**Goals:**

- Introduce a reusable internal helper for parsing command output with bundled TTP templates.
- Store collection-owned TTP templates with the facts parser code so they are versioned and packaged with the collection.
- Migrate `parse_vlan_brief()` to use a bundled `show vlan brief` template.
- Preserve all existing VLAN parser semantics, including empty-output handling, integer VLAN IDs, `state` and `status` keys, and normalized `ports` lists.
- Keep parser execution safe in Ansible module contexts by using TTP single-process parsing.
- Verify bundled `.ttp` templates are included when the collection is built.

**Non-Goals:**

- Allow users to provide arbitrary TTP templates.
- Change `xikeos_command` to return structured parsed data.
- Migrate every facts parser in this change.
- Replace Python normalization with template-only transformations.
- Introduce `ansible.utils.cli_parse` as a runtime path.

## Decisions

### Use bundled templates instead of user-provided templates

The templates will be maintained by the collection and loaded from a package-relative template directory such as `plugins/module_utils/facts/ttp_templates/`.

Alternatives considered:

- User-provided templates: rejected because the goal is internal maintainability, not a new public parsing API.
- Inline template strings in parser functions: rejected because separate template files are easier to read, diff, and reuse.

### Add a small internal TTP helper

Create a facts parser utility that centralizes TTP import, template loading, `parse(one=True)`, result flattening, and error handling. Parser modules call this helper and then normalize the raw parsed rows.

Alternatives considered:

- Direct TTP calls in each parser: simpler initially, but it spreads import/error/result-shape details across modules.
- Use `ansible.utils.cli_parse`: rejected for this change because existing parsers are pure Python utilities and should remain simple to unit test without invoking Ansible parser plugins.

### Keep Python normalization as the compatibility boundary

TTP should extract fields from command output; Python should preserve existing return contracts by coercing types, applying defaults, splitting lists, and maintaining backwards-compatible keys.

For VLAN parsing this means the TTP result may contain string fields, while `parse_vlan_brief()` still returns normalized dictionaries with `vlan_id` as `int`, `ports` as `list[str]`, and both `state` and `status` populated.

Alternatives considered:

- Put conversions into the TTP template: rejected because it makes compatibility behavior harder to test and review.
- Return raw TTP output directly: rejected because consumers depend on the current normalized parser contract.

### Preserve `parse_vlan_line()` during the first migration

`parse_vlan_line()` is imported by existing tests and may be treated as a helper contract. The first migration should not remove or break it, even if `parse_vlan_brief()` no longer needs it internally.

Alternatives considered:

- Remove `parse_vlan_line()`: rejected as unnecessary compatibility risk for the initial TTP adoption.

## Risks / Trade-offs

- [Risk] TTP is a new runtime Python dependency and may be missing in some execution environments. → Mitigation: declare the dependency and make import failures explicit with an actionable error message.
- [Risk] TTP default result shape is nested and easy to misuse. → Mitigation: centralize result handling in the helper and use a flattened structure for parser callers.
- [Risk] Bundled `.ttp` files may be omitted from collection artifacts. → Mitigation: include collection-build verification in implementation tasks.
- [Risk] Template matching may be less permissive than the existing parser for unusual device output. → Mitigation: preserve existing parser tests and add focused cases for no ports and empty output; keep the first migration limited to VLAN parsing.
- [Trade-off] Python normalization remains necessary. → This keeps compatibility explicit, at the cost of not eliminating all parser-specific code.

## Migration Plan

1. Add the TTP dependency and internal parsing helper.
2. Add a bundled TTP template for `show vlan brief`.
3. Migrate `parse_vlan_brief()` to call the helper and normalize parsed rows into the existing return shape.
4. Keep `parse_vlan_line()` behavior intact.
5. Run unit tests for parser compatibility and VLAN resource behavior.
6. Build the collection and verify the `.ttp` template is included.

Rollback is straightforward: keep the old parser behavior available in version control and revert the VLAN parser to the previous regex/line-splitting implementation if the template path proves incompatible.

## Open Questions

- What minimum supported `ttp` version should be pinned after implementation validates the API in this environment?
- Should future parser migrations be handled one parser per change, or batched once the VLAN template pattern is proven?
