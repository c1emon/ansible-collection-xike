## Why

Xike OS facts parsers currently rely on hand-written regular expressions and line-splitting logic spread across individual parser modules. This makes table-style command parsing harder to maintain as device output formats evolve and as more facts parsers are added.

Using bundled TTP templates internally gives parser authors a declarative way to describe CLI output structure while preserving the existing Python return contracts consumed by facts and resource modules.

## What Changes

- Add an internal TTP-based parsing path for bundled facts parser templates.
- Introduce a reusable helper for loading bundled TTP templates and parsing command output in Ansible-safe single-process mode.
- Add an initial bundled template for `show vlan brief` and migrate `parse_vlan_brief()` to use it.
- Preserve the existing `parse_vlan_brief()` return shape, including integer VLAN IDs, `state`/`status` fields, and list-valued `ports`.
- Keep the scope internal to collection parsers; users will not provide arbitrary templates or receive a new structured `xikeos_command` API as part of this change.
- Add tests that lock in compatibility for empty output, rows without ports, and existing VLAN parser behavior.

## Capabilities

### New Capabilities
- `ttp-return-template-parsing`: Internal parser capability for converting Xike OS command output into existing facts return values using bundled TTP templates.

### Modified Capabilities
- `idempotent-resource-modules`: VLAN resource modules continue to gather current state through the existing parser contract while the parser implementation changes internally.

## Impact

- Affected code:
  - `plugins/module_utils/facts/vlans.py`
  - New internal facts parser helper under `plugins/module_utils/facts/`
  - New bundled TTP template directory under `plugins/module_utils/facts/`
  - VLAN parser unit tests under `tests/unit/`
- Dependencies:
  - Add the Python `ttp` package as a runtime dependency.
- Compatibility:
  - No breaking changes to public module arguments, facts keys, resource module behavior, or parser return shapes.
- Packaging:
  - Bundled `.ttp` template files must be included in the built Ansible collection artifact.
