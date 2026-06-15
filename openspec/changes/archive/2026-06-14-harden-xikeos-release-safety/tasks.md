## 1. Command Safety

- [x] 1.1 Add unit coverage proving `xikeos_command` check mode does not call the network command execution path for guarded mutating commands when `unsafe_allow_mutating_commands=true`.
- [x] 1.2 Update `xikeos_command` check-mode control flow so unsafe mutating commands are reported but not sent to the device.
- [x] 1.3 Verify read-only `show` commands keep existing check-mode/read-only behavior and report `changed: false`.

## 2. OSPF Facts Execution

- [x] 2.1 Add unit coverage proving `Ospfv2Facts` uses the collection network operational command utility instead of `module.run_command()`.
- [x] 2.2 Replace local `module.run_command()` calls in OSPFv2 facts gathering with `run_commands()` from the XikeOS network utility layer.
- [x] 2.3 Remove broad swallowed exceptions from OSPFv2 facts gathering and surface failures through the existing facts/module error boundary.
- [x] 2.4 Verify `xikeos_ospf_v2` before/after gathering still receives normalized OSPF facts or contextual failures.

## 3. Packaging and Release Workflow

- [x] 3.1 Update `galaxy.yml` build ignores to exclude `plugins/connection/xikeos.py`, collection tarballs, virtualenvs, caches, `.test_path`, and local agent/tooling directories.
- [x] 3.2 Update the Galaxy publish workflow to select the exact tarball matching the `galaxy.yml` version instead of using broad glob plus first-result ordering.
- [x] 3.3 Add or document a release validation check that fails if the expected declared-version tarball is missing after build.
- [x] 3.4 Verify a collection build does not include the legacy connection plugin or ignored local artifacts.

## 4. Documentation Alignment

- [x] 4.1 Replace project playbook execution examples with `uv run ansible-playbook` where the docs describe running from this repository.
- [x] 4.2 Replace project GitNexus refresh guidance with global `gitnexus analyze` and remove `npx gitnexus analyze` guidance.
- [x] 4.3 Remove or rewrite user-facing legacy connection examples so setup documentation uses `ansible_connection: ansible.netcommon.network_cli` and `ansible_network_os: c1emon.xikeos.xikeos`.
- [x] 4.4 Update stale version/module-count references discovered during review.

## 5. Verification

- [x] 5.1 Run targeted unit tests for command safety and OSPF facts changes.
- [x] 5.2 Run the full unit test suite with `uv run pytest tests/unit`.
- [x] 5.3 Run a collection build dry-run with `uv run ansible-galaxy collection build --force` and inspect the generated package contents for excluded files.
- [x] 5.4 Run OpenSpec validation/status checks for this change before applying or archiving.
