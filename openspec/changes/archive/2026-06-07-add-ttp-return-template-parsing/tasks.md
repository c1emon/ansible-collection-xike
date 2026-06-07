## 1. Dependency and Template Infrastructure

- [x] 1.1 Add the Python `ttp` runtime dependency to project metadata with a validated minimum version.
- [x] 1.2 Create an internal facts parser helper for loading bundled `.ttp` templates and invoking TTP with `parse(one=True)`.
- [x] 1.3 Ensure the helper returns a predictable flattened Python structure for parser modules.
- [x] 1.4 Add explicit, actionable handling for missing TTP imports or missing bundled template files.

## 2. VLAN Template Parser

- [x] 2.1 Add a bundled TTP template for `show vlan brief` under the facts parser template directory.
- [x] 2.2 Migrate `parse_vlan_brief()` to parse rows through the internal TTP helper.
- [x] 2.3 Preserve VLAN normalization semantics: integer `vlan_id`, `name`, `state`, `status`, and list-valued `ports`.
- [x] 2.4 Preserve empty-output behavior and VLAN rows without ports.
- [x] 2.5 Keep `parse_vlan_line()` behavior compatible with existing tests and callers.

## 3. Tests and Compatibility

- [x] 3.1 Update or add unit tests for the TTP-backed VLAN parser while preserving existing parser expectations.
- [x] 3.2 Add test coverage for empty output and VLAN rows with no ports through the TTP-backed path.
- [x] 3.3 Verify `xikeos_vlans` current-state gathering continues to receive normalized VLAN fields for idempotent diffing.
- [x] 3.4 Run the relevant unit test suite for facts parsers and VLAN resource behavior.

## 4. Packaging Verification

- [x] 4.1 Build the Ansible collection artifact.
- [x] 4.2 Verify the bundled `show vlan brief` `.ttp` template is included in the built artifact.
- [x] 4.3 Document any required installation note for the new `ttp` Python dependency if collection packaging does not install it automatically.

## 5. Change Safety

- [x] 5.1 Run GitNexus impact analysis before editing `parse_vlan_brief()` and any new or modified parser helper symbols.
- [x] 5.2 Run `gitnexus_detect_changes()` before commit or final handoff to confirm affected flows match the intended VLAN parser scope.
