# xike.xikeos FAQ

Frequently asked questions about the `xike.xikeos` Ansible Collection.

## General

### Why `ansible.netcommon.network_cli` instead of a custom Netmiko backend?

The supported architecture uses **`ansible.netcommon.network_cli`** with this collection's terminal and cliconf plugins:

1. **Standard Ansible Network Pattern**: `network_cli` is the supported connection path for CLI network collections.

2. **Collection-owned Platform Behavior**: `terminal/xikeos.py` and `cliconf/xikeos.py` define Xike prompt, error, show, and config behavior.
   - Proper prompt detection
   - Command encoding/decoding
   - Session timeout handling
   - Pagination support

3. **Clear Dependencies**: `ansible.netcommon` is required. Netmiko Raisecom, TextFSM, Genie, and pyATS are optional references/tools only.

4. **Consistent Module API**: modules call Ansible connection helpers rather than returning generated commands without device execution.

**Alternative considered**: a custom Netmiko backend remains a reference option, but it duplicates `network_cli` behavior and is not the supported default.

---

### Difference from cisco.ios collection?

The `xike.xikeos` collection is specifically designed for **Xike (兮克) switches**, while `cisco.ios` targets **Cisco IOS/IOS-XE** devices. Key differences:

| Aspect | xike.xikeos | cisco.ios |
|--------|-------------|-----------|
| **Target** | Xike switches | Cisco IOS/IOS-XE |
| **CLI Syntax** | Xike-specific (IOS-like) | Cisco IOS |
| **Interface Naming** | `ethernet 0/0/1` | `GigabitEthernet0/1` |
| **VLAN Interface** | `vlan-interface 100` | `Vlan100` |
| **Port Modes** | access, trunk, **hybrid** | access, trunk |
| **STP Commands** | `stp` | `spanning-tree` |
| **LAG** | `eth-trunk` | `Port-channel` |
| **ACL Numbering** | 1-999, 1000-1999, 2000-2999 | 1-199, 1300-2699 |
| **Xike Features** | ERPS, EAPS, QinQ, Hybrid | Not supported |

**When to use which**:
- Use `cisco.ios` for Cisco IOS/IOS-XE devices
- Use `xike.xikeos` for Xike (兮克) switches
- Both cannot be used interchangeably

---

### How to handle hybrid port mode?

Hybrid port mode is a **Xike-specific feature** not found on Cisco switches. It allows flexible VLAN tagging where:

- **Untagged VLANs**: Traffic is sent without VLAN tags
- **Tagged VLANs**: Traffic is sent with VLAN tags
- **PVID**: The default VLAN for incoming untagged traffic

**Configuration Example**:
```yaml
- name: Configure hybrid port
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/3
        mode: hybrid
        pvid: 100
        hybrid_untagged_vlan: "10,20"
        hybrid_tagged_vlan: "30,40"
    state: merged
```

**Generated Commands**:
```
interface ethernet 0/0/3
switchport link-type hybrid
switchport pvid 100
switchport hybrid untagged vlan 10,20
switchport hybrid tagged vlan 30,40
```

**Key Points**:
- Hybrid mode must be set before configuring untagged/tagged VLANs
- PVID is the VLAN assigned to incoming untagged traffic
- VLAN ranges can be specified as comma-separated values (e.g., `10,20,30`) or ranges (e.g., `10-20`)

---

## Troubleshooting

### How to troubleshoot connection issues?

Follow these steps to diagnose connection problems:

#### 1. Verify SSH Connectivity
```bash
# Test basic SSH connection
ssh admin@192.168.1.100

# Test with verbose output
ssh -v admin@192.168.1.100
```

#### 2. Check Ansible Inventory
```yaml
# Verify these variables are set correctly
all:
  children:
    xike_switches:
      hosts:
        core-sw01:
          ansible_host: 192.168.1.100      # IP address
          ansible_port: 22                    # SSH port
          ansible_user: admin                 # Username
          ansible_password: "secret"          # Password
          ansible_network_os: xike.xikeos.xikeos
          ansible_connection: ansible.netcommon.network_cli
```

#### 3. Test with ansible ping
```bash
# Test connection
ansible xike_switches -m ping -i inventory.yml

# Test with verbose output
ansible xike_switches -m ping -i inventory.yml -vvv
```

#### 4. Check platform plugin selection
Ensure:
- `ansible.netcommon` is installed.
- `ansible_network_os` is exactly `xike.xikeos.xikeos`.
- The device responds to IOS-like commands and supports the prompt/error variants documented as open validation items.

#### 5. Debug Mode
```bash
# Run playbook with debug output
ansible-playbook playbook.yml -i inventory.yml -vvvv

# Check network_cli and platform plugin logs
ANSIBLE_DEBUG=1 ansible-playbook playbook.yml -i inventory.yml
```

#### 6. Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | SSH service not running | Check switch SSH config |
| `Authentication failed` | Wrong credentials | Verify username/password |
| `Timeout` | Network issue | Check firewall, increase timeout |
| `Could not find terminal/cliconf plugin` | Wrong `ansible_network_os` or missing collection | Use `xike.xikeos.xikeos` and install this collection |
| `Command timeout` | Long-running commands | Increase `ansible_timeout` |

---

### How to add new Xike firmware support?

When Xike releases new firmware with CLI changes, follow these steps:

#### 1. Capture CLI Output
```bash
# SSH to the switch and capture output of relevant commands
ssh admin@switch

# Capture output for each feature
show version
show vlan brief
show interface brief
show running-config
# ... capture all relevant commands
```

#### 2. Update Facts Parsers
If the CLI output format changed, update the corresponding facts parser:

```python
# Example: plugins/module_utils/facts/vlans.py

def parse_vlan_brief(output):
    """Parse 'show vlan brief' output."""
    # Check if output format matches expected pattern
    # Update regex patterns if needed
    # Handle new fields or changed formats
    pass
```

#### 3. Update Command Generation
If command syntax changed, update the module's command generation:

```python
# Example: plugins/modules/xikeos_vlans.py

def get_commands(config, state):
    """Generate CLI commands."""
    # Update command syntax if needed
    # Add new commands for new features
    pass
```

#### 4. Update COMMAND_MAP
If new show commands are available, add them to the command map:

```python
# plugins/module_utils/xikeos.py

COMMAND_MAP = {
    # ... existing commands
    'show_new_feature': 'show new-feature',
}
```

#### 5. Test Thoroughly
```bash
# Run existing tests
pytest tests/

# Test with new firmware
ansible-playbook test_playbook.yml -i inventory.yml
```

#### 6. Document Changes
Update documentation to reflect firmware compatibility:
- Add firmware version to README.md
- Update any version-specific notes

---

### How to compare with raw xikeos_config commands?

Use the `xikeos_config` module to push raw commands, or compare its output with resource modules:

#### Using xikeos_config
```yaml
# Raw command approach
- name: Push raw config
  xike.xikeos.xikeos_config:
    lines:
      - vlan 100
      - name DATA
      - interface ethernet 0/0/1
      - switchport pvid 100
    save: true
```

#### Using Resource Modules
```yaml
# Declarative approach
- name: Configure VLAN
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
    state: merged

- name: Configure interface
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/1
        mode: access
        access_vlan: 100
    state: merged
```

#### Comparison

| Aspect | xikeos_config | Resource Modules |
|--------|---------------|------------------|
| **Syntax** | Raw CLI commands | Declarative YAML |
| **Idempotency** | Not idempotent | Idempotent |
| **Error Handling** | Manual | Automatic |
| **Check Mode** | Limited | Full support |
| **Diff** | Raw text | Structured diff |
| **State Management** | None | merged/replaced/deleted |
| **Use Case** | One-off configs | Standardized automation |

#### Best Practices
1. **Use resource modules** for standard configurations (VLANs, interfaces, routing)
2. **Use xikeos_config** for:
   - One-off commands not covered by modules
   - Vendor-specific features not yet supported
   - Migration or temporary workarounds
3. **Document** any xikeos_config usage for future maintenance

---

## Configuration

### How to save configuration changes?

Most resource modules do not automatically save configuration. Use one of these methods:

#### Method 1: Use save parameter in xikeos_config
```yaml
- name: Apply and save config
  xike.xikeos.xikeos_config:
    lines:
      - vlan 100
      - name DATA
    save: true
```

#### Method 2: Save separately after resource modules
```yaml
- name: Configure VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
    state: merged

- name: Save configuration
  xike.xikeos.xikeos_config:
    lines:
      - write memory
```

#### Method 3: Use xikeos_command
```yaml
- name: Save configuration
  xike.xikeos.xikeos_command:
    commands:
      - write memory
```

---

### How to use check mode?

All resource modules support check mode (`--check` or `--diff`):

```bash
# Check mode (dry run)
ansible-playbook playbook.yml --check

# Check mode with diff
ansible-playbook playbook.yml --check --diff
```

In check mode:
- Modules compute what commands would be sent
- No changes are made to the device
- Output shows `changed: false` and the commands that would be sent

---

### How to handle multiple VLANs in a range?

Use comma-separated values or ranges:

```yaml
# VLAN range syntax
- name: Configure trunk with VLAN range
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/24
        mode: trunk
        trunk_allowed_vlan: "10,20,30,40,50"
    state: merged

# Or use "all" for all VLANs
- name: Allow all VLANs on trunk
  xike.xikeos.xikeos_l2_interfaces:
    config:
      - name: ethernet 0/0/24
        mode: trunk
        trunk_allowed_vlan: "all"
    state: merged
```

---

## Advanced

### How to use with Ansible Vault?

Protect sensitive data with Ansible Vault:

```bash
# Create encrypted vault file
ansible-vault create group_vars/xike_switches/vault.yml

# Add credentials
ansible_vault:
  vault_switch_password: "your_password_here"

# Run playbook with vault
ansible-playbook playbook.yml --ask-vault-pass

# Or use vault ID
ansible-playbook playbook.yml --vault-id prod@prompt
```

In inventory:
```yaml
all:
  children:
    xike_switches:
      vars:
        ansible_password: "{{ vault_switch_password }}"
```

---

### How to use with AWX/Tower?

The `xike.xikeos` collection works with AWX/Tower:

1. **Install Collection**: Add to AWX/Tower collections path
2. **Configure Inventory**: Set network OS and connection variables
3. **Create Credentials**: Use Machine or Network credentials
4. **Run Playbooks**: Execute playbooks with collection modules

**AWX/Tower Variables**:
```yaml
ansible_network_os: xike.xikeos.xikeos
ansible_connection: ansible.netcommon.network_cli
```

---

### How to contribute to the project?

See [Development Guide](development.md) for:
- Project structure
- Adding new modules
- Testing guidelines
- Code style conventions

**Quick Start**:
```bash
# Fork and clone
git clone https://github.com/your-username/xike-xikeos.git
cd xike-xikeos

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/

# Submit pull request
```

---

## Performance

### How to optimize playbook execution?

1. **Use async for slow operations**:
```yaml
- name: Configure VLANs
  xike.xikeos.xikeos_vlans:
    config:
      - vlan_id: 100
        name: DATA
    state: merged
  async: 300
  poll: 0
```

2. **Use serial execution**:
```bash
ansible-playbook playbook.yml --serial 1
```

3. **Limit to specific hosts**:
```bash
ansible-playbook playbook.yml --limit core-sw01
```

4. **Use facts caching**:
```yaml
# ansible.cfg
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts_cache
fact_caching_timeout = 3600
```

---

### How to handle large-scale deployments?

For managing many switches:

1. **Use roles** for reusable configurations:
```yaml
# roles/switch_config/tasks/main.yml
- name: Configure VLANs
  xike.xikeos.xikeos_vlans:
    config: "{{ switch_vlans }}"
    state: merged

- name: Configure interfaces
  xike.xikeos.xikeos_l2_interfaces:
    config: "{{ switch_interfaces }}"
    state: merged
```

2. **Use inventory groups**:
```yaml
all:
  children:
    core_switches:
      hosts:
        core-sw01:
        core-sw02:
    access_switches:
      hosts:
        access-sw01:
        access-sw02:
```

3. **Use tags** for selective execution:
```bash
ansible-playbook playbook.yml --tags vlans
ansible-playbook playbook.yml --tags interfaces
```

4. **Use parallel execution** (with caution):
```bash
ansible-playbook playbook.yml --forks 10
```
