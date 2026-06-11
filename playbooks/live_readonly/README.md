# Live read-only test playbooks

These playbooks exercise the current lifecycle coverage without applying device
configuration. Run them against `playbooks/inventory.yml` or a compatible
inventory that defines the `xike_switches` group.

## Test list

1. `00_read_commands.yml`
   - Runs read-only operational commands through `xikeos_command`.
   - Covers the command execution path and basic device reachability.
2. `01_gather_lifecycle_state.yml`
   - Runs `xikeos_vlans state=gathered`.
   - Exercises the lifecycle-complete gathered path.
3. `02_check_mode_lifecycle_modules.yml`
   - Runs lifecycle-complete resource modules in check mode with empty configs.
   - Covers read-only gather/no-op paths for interfaces, L2, L3, LAG, static
     routes, and ACLs.
4. `03_render_specialty_modules.yml`
   - Runs specialty modules with `state=rendered`.
   - Covers non-mutating command rendering for STP, ERPS, EAPS, QinQ, mirror,
     port-isolate, flex/monitor link, and OSPFv2.

## Run commands

When running directly from this source checkout, expose it as a local Ansible
collection under `.test_path` first:

```bash
mkdir -p .test_path/ansible_collections/xike
ln -sfn "$PWD" .test_path/ansible_collections/xike/xikeos
export ANSIBLE_COLLECTIONS_PATH=.test_path
export XIKEOS_PASSWORD='your-login-password'
export XIKEOS_ENABLE_PASSWORD='your-enable-password'  # optional; defaults to XIKEOS_PASSWORD
```

```bash
uv run ansible-playbook -i playbooks/inventory.yml playbooks/live_readonly/00_read_commands.yml
uv run ansible-playbook -i playbooks/inventory.yml playbooks/live_readonly/01_gather_lifecycle_state.yml
uv run ansible-playbook -i playbooks/inventory.yml playbooks/live_readonly/02_check_mode_lifecycle_modules.yml
uv run ansible-playbook -i playbooks/inventory.yml playbooks/live_readonly/03_render_specialty_modules.yml
```

Run all playbooks from a shell loop:

```bash
for playbook in playbooks/live_readonly/*.yml; do
  uv run ansible-playbook -i playbooks/inventory.yml "$playbook"
done
```
