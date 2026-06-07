## 1. Action Plugin Template Injection

- [ ] 1.1 Add `plugins/action/xikeos_vlans.py` action plugin that delegates to the normal module action path.
- [ ] 1.2 Implement controller-side loading of `show_vlan.textfsm` from the collection template directory.
- [ ] 1.3 Inject loaded TextFSM content into an internal `_textfsm_templates` module argument keyed by template name.
- [ ] 1.4 Fail explicitly with an actionable message if the controller-side template file is missing.

## 2. Module and Parser Interfaces

- [ ] 2.1 Add hidden `_textfsm_templates` argument support to `xikeos_vlans` without documenting it as a public module option.
- [ ] 2.2 Pass injected templates from `xikeos_vlans.gather_vlans()` to `parse_vlan()`.
- [ ] 2.3 Update `parse_vlan()` to accept optional injected template mappings and preserve normalized VLAN return fields.
- [ ] 2.4 Update `parse_textfsm_template()` to prefer injected template content, fall back to local template files, and fail explicitly when neither exists.
- [ ] 2.5 Update `parse_ttp_template()` with the same injected-template interface for future TTP-backed parsers.
- [ ] 2.6 Remove embedded/builtin template fallback dictionaries from parser helpers.

## 3. Tests and Live Runtime Coverage

- [ ] 3.1 Add unit tests for action plugin template injection into `xikeos_vlans` module arguments.
- [ ] 3.2 Add parser helper tests proving injected templates work when local template directories are unavailable.
- [ ] 3.3 Add parser helper tests proving missing templates fail explicitly when neither injected nor local templates exist.
- [ ] 3.4 Keep real `show vlan` sample coverage for normalized VLANs, multi-line ports, tagged ports, and VLANs without ports.
- [ ] 3.5 Run the relevant unit test suite for facts parsers, VLAN resource behavior, and command generation.
- [ ] 3.6 Re-run the live playbook path that previously failed to confirm AnsiballZ runtime no longer requires template data files.

## 4. Documentation, Specs, and Packaging

- [ ] 4.1 Update docs/specs to describe controller-injected parser templates and explicit missing-template failures.
- [ ] 4.2 Build the collection artifact and verify parser template files remain packaged as source-of-truth files.
- [ ] 4.3 Verify hidden template arguments are not exposed in public module documentation examples.

## 5. Change Safety

- [ ] 5.1 Run GitNexus impact analysis before editing `xikeos_vlans`, `parse_vlan()`, and parser helper symbols.
- [ ] 5.2 Run `gitnexus_detect_changes()` before commit or final handoff to confirm affected flows match the intended VLAN parser/runtime scope.
