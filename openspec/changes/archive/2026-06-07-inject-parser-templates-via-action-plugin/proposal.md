## Why

Ansible module runtime packages Python `module_utils` into an AnsiballZ payload that may omit non-Python parser template files. VLAN gathering currently depends on bundled TextFSM template files being present at module runtime, which can fail even when the collection source or built artifact contains the template.

## What Changes

- Add a controller-side action plugin path for `xikeos_vlans` that loads collection-owned parser template files before module execution.
- Inject required parser template content into hidden module arguments so the module does not need to read `.textfsm` or `.ttp` files from the AnsiballZ payload.
- Update parser helpers to accept injected template content and use local files only as a development/test fallback.
- Remove embedded/builtin template fallbacks so missing templates fail explicitly instead of silently drifting from file templates.
- Keep public module arguments and returned VLAN facts unchanged.

## Capabilities

### New Capabilities

- `controller-injected-parser-templates`: Controller-side parser template injection for modules that need bundled parser templates at runtime.

### Modified Capabilities

- `ttp-return-template-parsing`: Template-backed parser execution supports controller-injected TTP/TextFSM template content and explicit missing-template failures.
- `idempotent-resource-modules`: VLAN current-state gathering continues to use normalized `show vlan` parser output while obtaining parser templates through action-plugin injection.

## Impact

- Affected code:
  - New `plugins/action/xikeos_vlans.py` action plugin.
  - `plugins/modules/xikeos_vlans.py` hidden template argument handling.
  - `plugins/module_utils/facts/vlans.py` parser call signatures.
  - `plugins/module_utils/facts/textfsm_parser.py` and `ttp_parser.py` template-loading behavior.
  - Unit tests for parser helpers, VLAN gathering, and action plugin injection.
- Dependencies:
  - No new Python dependencies beyond current `ttp` and `textfsm` packages.
- Compatibility:
  - No breaking changes to public module arguments, facts keys, resource module states, or return structures.
- Runtime behavior:
  - Missing controller-side template files should fail with an actionable error before or during module invocation instead of falling back to duplicated builtin strings.
