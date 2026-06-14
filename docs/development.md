# c1emon.xikeos Developer Guide

Guide for developers contributing to the `c1emon.xikeos` Ansible Collection.

## Table of Contents

- [Project Structure](#project-structure)
- [Adding a New Module](#adding-a-new-module)
- [Adding a New Facts Parser](#adding-a-new-facts-parser)
- [Resource Module Lifecycle Contract](#resource-module-lifecycle-contract)
- [Testing Changes](#testing-changes)
- [Code Style Conventions](#code-style-conventions)

---

## Project Structure

```
c1emon.xikeos/
├── galaxy.yml                    # Collection metadata
├── README.md                     # Main documentation
├── pyproject.toml                # Python project metadata and dependencies
├── uv.lock                       # Locked Python dependency graph
├── plugins/
│   ├── __init__.py
│   ├── terminal/
│   │   └── xikeos.py            # Prompt, paging, error handling
│   ├── cliconf/
│   │   └── xikeos.py            # Command/config API over network_cli
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── xikeos_interfaces.py
│   │   ├── xikeos_l2_interfaces.py
│   │   ├── xikeos_l3_interfaces.py
│   │   ├── xikeos_lag_interfaces.py
│   │   ├── xikeos_vlans.py
│   │   ├── xikeos_ospf_v2.py
│   │   ├── xikeos_static_routes.py
│   │   ├── xikeos_acls.py
│   │   ├── xikeos_stp.py
│   │   ├── xikeos_mirror.py
│   │   ├── xikeos_port_isolate.py
│   │   ├── xikeos_erps.py
│   │   ├── xikeos_eaps.py
│   │   ├── xikeos_qinq.py
│   │   ├── xikeos_flex_monitor_link.py
│   │   ├── xikeos_config.py
│   │   └── xikeos_command.py
│   ├── module_utils/
│   │   ├── __init__.py
│   │   ├── xikeos.py             # COMMAND_MAP and constants
│   │   └── facts/
│   │       ├── __init__.py
│   │       ├── interfaces.py
│   │       ├── l2_interfaces.py
│   │       ├── l3_interfaces.py
│   │       ├── lag_interfaces.py
│   │       ├── vlans.py
│   │       ├── ospfv2.py
│   │       ├── static_routes.py
│   │       ├── acls.py
│   │       ├── stp.py
│   │       ├── mirror.py
│   │       ├── port_isolate.py
│   │       ├── erps.py
│   │       ├── eaps.py
│   │       ├── qinq.py
│   │       └── flex_monitor_link.py
│   └── filter/
│       └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_*.py
│   └── integration/
│       └── targets/
│           └── xikeos_*/
├── docs/
│   ├── architecture.md
│   ├── modules.md
│   ├── faq.md
│   └── development.md
└── meta/
    └── runtime.yml
```

### Key Components

#### Platform Plugins (`plugins/terminal/xikeos.py`, `plugins/cliconf/xikeos.py`)
- Inventory must use `ansible_connection: ansible.netcommon.network_cli`.
- `ansible_network_os: c1emon.xikeos.xikeos` selects this collection's terminal and cliconf plugins.
- `terminal/xikeos.py` owns prompt matching, paging disablement, privilege-mode handling, and command error detection.
- `cliconf/xikeos.py` owns show command execution, running-config retrieval, configuration edits, device info, and capabilities.

#### Dependency guidance
- Required Ansible collection dependency: `ansible.netcommon`.
- Optional references only: Netmiko Raisecom prompt behavior, TextFSM templates, Genie/pyATS parser conventions. Do not make these mandatory runtime dependencies unless a later OpenSpec change explicitly chooses that architecture.

#### Modules (`plugins/modules/`)
- Each module implements a specific feature
- Modules gather current state where needed, generate minimal CLI commands, and execute through cliconf helpers.
- Support check mode and consistent `before`, `after`, `commands`, and `changed` results for reference resource modules.

---

## Resource Module Lifecycle Contract

Declarative resource modules that support mutating states (`merged`, `replaced`, `deleted`, `present`, or `absent`) must follow the standard lifecycle:

1. Validate module input.
2. Gather `before` state through network `run_commands()` or a facts provider that uses that helper.
3. Normalize desired and current state before diffing.
4. Compute minimal `commands` before honoring check mode.
5. In check mode, return `changed`, `commands`, `before`, and `after` without calling `load_config()`.
6. Outside check mode, apply configuration only through `load_config()`.
7. Report `after` from post-change facts or a clearly documented simulated transition.

Resource modules must not use `module.run_command()` for device configuration. Facts providers must fail explicitly when required show/config output cannot be gathered or parsed; they must not silently return empty current state.

Current lifecycle classification:

| Module | Lifecycle status | Notes |
|--------|------------------|-------|
| `xikeos_vlans` | lifecycle-complete | Reference implementation; supports `gathered` and mutating VLAN states. |
| `xikeos_static_routes` | lifecycle-complete | Uses facts, computes check-mode diffs, applies with `load_config()`. |
| `xikeos_acls` | lifecycle-complete | Uses facts, computes check-mode diffs, applies with `load_config()`. |
| `xikeos_interfaces` | lifecycle-complete | Uses interface facts and shared lifecycle helper. |
| `xikeos_l2_interfaces` | lifecycle-complete | Uses running-config facts and shared lifecycle helper. |
| `xikeos_l3_interfaces` | lifecycle-complete | Uses running-config facts and shared lifecycle helper. |
| `xikeos_lag_interfaces` | lifecycle-complete | Uses running-config facts and shared lifecycle helper. |
| `xikeos_stp`, `xikeos_erps`, `xikeos_eaps`, `xikeos_qinq`, `xikeos_mirror`, `xikeos_port_isolate`, `xikeos_flex_monitor_link`, `xikeos_ospf_v2` | rendered-only | `state=rendered` returns commands without changing the device; mutating states fail fast until full lifecycle support is implemented. |

Use `plugins/module_utils/network/xikeos/lifecycle.py` for shared lifecycle mechanics when adding or migrating modules.

#### Module Utils (`plugins/module_utils/`)
- **xikeos.py**: COMMAND_MAP and constants
- **facts/**: Parsers for "show" command output

---

## Adding a New Module

Follow these steps to add a new resource module.

### Step 1: Plan the Module

Before coding, define:
- **Purpose**: What feature does this module manage?
- **Parameters**: What configuration options are needed?
- **States**: What states should be supported? (merged, replaced, deleted, present, absent)
- **CLI Commands**: What Xike CLI commands are used?
- **Show Commands**: What show commands provide current state?

### Step 2: Create the Module File

Create `plugins/modules/xikeos_<feature>.py`:

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS <Feature> resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_<feature>
short_description: Manage <feature> on Xike OS devices
version_added: "0.2.0"
description:
  - This module provides declarative management of <feature>
    on Xike (兮克) OS devices.
options:
  config:
    description: <Feature> configuration
    type: dict
    suboptions:
      parameter_name:
        description: Description of parameter
        type: str
        required: true
  state:
    description:
      - State of the configuration.
      - C(present) - Creates or updates the configuration.
      - C(absent) - Removes the configuration.
    type: str
    choices: ['present', 'absent']
    default: present
author: clemon
"""

EXAMPLES = """
- name: Configure <feature>
  c1emon.xikeos.xikeos_<feature>:
    config:
      parameter_name: value
    state: present
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - command1
    - command2
"""

from ansible.module_utils.basic import AnsibleModule


def get_commands(config, state):
    """Generate CLI commands from configuration."""
    commands = []
    
    if state == "absent":
        # Generate removal commands
        commands.append("no <feature> config")
        return commands
    
    # Generate creation/update commands
    commands.append("<feature> config")
    commands.append("parameter-name {0}".format(config.get("parameter_name")))
    
    return commands


def main():
    """Main entry point for the module."""
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                parameter_name=dict(
                    type="str",
                    required=True,
                ),
            ),
        ),
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ("state", "present", ["config"]),
        ],
        supports_check_mode=True,
    )
    
    config = module.params.get("config") or {}
    state = module.params.get("state", "present")
    
    result = {
        "changed": False,
        "commands": [],
    }
    
    if not config and state == "present":
        module.exit_json(**result)
    
    # Generate commands
    commands = get_commands(config, state)
    result["commands"] = commands
    
    if module.check_mode:
        module.exit_json(**result)
    
    if commands:
        result["changed"] = True
    
    module.exit_json(**result)


if __name__ == "__main__":
    main()
```

### Step 3: Create Facts Parser (if needed)

If the module needs to gather current state, create `plugins/module_utils/facts/<feature>.py`:

```python
"""Facts parser for Xike OS <feature>."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re


def parse_show_output(output):
    """
    Parse 'show <feature>' output.
    
    Args:
        output: Raw CLI output string
    
    Returns:
        dict: Parsed configuration data
    """
    result = {}
    
    if not output:
        return result
    
    # Parse output using regex
    # Example:
    # for line in output.splitlines():
    #     match = re.match(r'pattern', line)
    #     if match:
    #         result['key'] = match.group(1)
    
    return result
```

### Step 4: Add Constants (if needed)

If the module uses new show commands, update `plugins/module_utils/xikeos.py`:

```python
# Add to COMMAND_MAP
COMMAND_MAP = {
    # ... existing commands
    'show_<feature>': 'show <feature>',
}
```

### Step 5: Write Tests

Create unit tests in `tests/unit/test_xikeos_<feature>.py`:

```python
"""Unit tests for xikeos_<feature> module."""

import pytest
from ansible_collections.c1emon.xikeos.plugins.modules.xikeos_<feature> import (
    get_commands,
)


class TestGetCommands:
    """Tests for get_commands function."""
    
    def test_present_state(self):
        """Test command generation for present state."""
        config = {"parameter_name": "value"}
        state = "present"
        
        commands = get_commands(config, state)
        
        assert "command1" in commands
        assert "command2" in commands
    
    def test_absent_state(self):
        """Test command generation for absent state."""
        config = {}
        state = "absent"
        
        commands = get_commands(config, state)
        
        assert "no <feature> config" in commands
```

### Step 6: Update Documentation

1. Add module to `docs/modules.md`
2. Update `README.md` if it's a major feature
3. Add examples to the module's DOCUMENTATION string

### Step 7: Test the Module

```bash
# Run unit tests
uv run pytest tests/unit/test_xikeos_<feature>.py -v

# Run all tests
uv run pytest tests/unit -v

# Test with Ansible
uv run ansible-playbook tests/integration/targets/xikeos_<feature>/tests/main.yml -i tests/integration/inventory.ini
```

---

## Adding a New Facts Parser

Facts parsers extract structured data from CLI output.

### Step 1: Understand the CLI Output

Capture sample output from the Xike switch:

```bash
ssh admin@switch
show <command>
```

Example output:
```
Feature    Status    Mode
----------------------------------
feature1   enabled   active
feature2   disabled  inactive
```

### Step 2: Create the Parser File

Create `plugins/module_utils/facts/<feature>.py`:

```python
"""Facts parser for Xike OS <feature>."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re


def parse_<feature>_output(output):
    """
    Parse 'show <feature>' output.
    
    Expected output format:
        Feature    Status    Mode
        ----------------------------------
        feature1   enabled   active
        feature2   disabled  inactive
    
    Returns:
        dict: Parsed configuration data
    """
    result = {
        'features': []
    }
    
    if not output:
        return result
    
    lines = output.strip().splitlines()
    
    # Skip header lines
    data_started = False
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines and separators
        if not stripped or re.match(r'^[-=]+$', stripped):
            data_started = True
            continue
        
        # Parse data lines
        if data_started:
            # Regex pattern matching the column layout
            pattern = re.compile(
                r'^(\S+)\s+'           # Feature name
                r'(\S+)\s+'            # Status
                r'(\S+)$'              # Mode
            )
            
            match = pattern.match(stripped)
            if match:
                feature = {
                    'name': match.group(1),
                    'status': match.group(2),
                    'mode': match.group(3),
                }
                result['features'].append(feature)
    
    return result


class <Feature>Facts:
    """Facts class for <feature>."""
    
    def __init__(self, module):
        self.module = module
        self._facts = None
    
    @property
    def facts(self):
        """Get facts from device."""
        if self._facts is None:
            self._facts = self._get_facts()
        return self._facts
    
    def _get_facts(self):
        """Gather facts from device."""
        # Get show command output
        show_cmd = self.module.params.get('show_command', 'show <feature>')
        
        try:
            rc, out, err = self.module.run_command(show_cmd)
            if rc == 0:
                return parse_<feature>_output(out)
        except Exception:
            pass
        
        return {'features': []}
    
    def get_facts(self):
        """Get facts as dict."""
        return self.facts
```

### Step 3: Integrate with Module

Update the module to use the facts parser:

```python
try:
    from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.<feature> import (
        <Feature>Facts,
    )
    HAS_FACTS = True
except ImportError:
    HAS_FACTS = False


def main():
    # ... argument spec ...
    
    # Gather existing facts
    if HAS_FACTS:
        facts = <Feature>Facts(module)
        existing_config = facts.get_facts()
    else:
        existing_config = {}
    
    # ... rest of module ...
```

### Step 4: Test the Parser

```python
"""Unit tests for <feature> facts parser."""

import pytest
from ansible_collections.c1emon.xikeos.plugins.module_utils.facts.<feature> import (
    parse_<feature>_output,
)


class TestParseOutput:
    """Tests for parse_<feature>_output function."""
    
    def test_parse_valid_output(self):
        """Test parsing valid CLI output."""
        output = """
Feature    Status    Mode
----------------------------------
feature1   enabled   active
feature2   disabled  inactive
"""
        result = parse_<feature>_output(output)
        
        assert len(result['features']) == 2
        assert result['features'][0]['name'] == 'feature1'
        assert result['features'][0]['status'] == 'enabled'
    
    def test_parse_empty_output(self):
        """Test parsing empty output."""
        result = parse_<feature>_output("")
        
        assert result['features'] == []
    
    def test_parse_no_match(self):
        """Test parsing output with no matching lines."""
        output = """
Some other output
that doesn't match
"""
        result = parse_<feature>_output(output)
        
        assert result['features'] == []
```

---

## Testing Changes

### Unit Tests

Unit tests validate individual functions without device access:

```bash
# Run all unit tests
uv run pytest tests/unit/ -v

# Run specific test file
uv run pytest tests/unit/test_xikeos_vlans.py -v

# Run with coverage
uv run pytest tests/unit/ --cov=plugins/modules --cov-report=html
```

### Integration Tests

Integration tests require a live Xike switch:

```bash
# Run integration tests
ansible-test integration xikeos_vlans -i tests/integration/inventory.ini

# Run specific test case
ansible-test integration xikeos_vlans -i tests/integration/inventory.ini --testcase test_create_vlan
```

### Manual Testing

1. **Set up test environment**:
```bash
# Create inventory file
cat > inventory.yml << EOF
all:
  hosts:
    test-switch:
      ansible_host: 192.168.1.100
      ansible_user: admin
      ansible_password: secret
      ansible_network_os: c1emon.xikeos.xikeos
      ansible_connection: ansible.netcommon.network_cli
EOF
```

2. **Create test playbook**:
```yaml
---
- name: Test module
  hosts: test-switch
  gather_facts: no
  tasks:
    - name: Test task
      c1emon.xikeos.xikeos_<feature>:
        config:
          # ... test configuration
        state: present
      register: result
    
    - name: Show result
      debug:
        var: result
```

3. **Run test**:
```bash
uv run ansible-playbook test_playbook.yml -i inventory.yml -vvv
```

### Test Checklist

Before submitting a pull request:

- [ ] Unit tests pass: `uv run pytest tests/unit/ -v`
- [ ] No syntax errors: `python -m py_compile plugins/modules/xikeos_<feature>.py`
- [ ] Documentation is complete (DOCUMENTATION, EXAMPLES, RETURN)
- [ ] Module supports check mode
- [ ] Module handles errors gracefully
- [ ] Code follows style conventions

---

## Code Style Conventions

### Python Style

Follow PEP 8 with these additions:

```python
# File header
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module docstring."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

# Imports
import re
from ansible.module_utils.basic import AnsibleModule

# Constants
CONSTANT_VALUE = 'value'

# Functions
def function_name(param1, param2):
    """Function docstring.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        type: Description
    """
    pass

# Classes
class ClassName:
    """Class docstring."""
    
    def __init__(self, param):
        """Initialize."""
        self.param = param
```

### Module Structure

Every module should follow this structure:

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Xike OS <Feature> resource module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: xikeos_<feature>
short_description: ...
version_added: "0.2.0"
description:
  - ...
options:
  config:
    description: ...
    type: dict
    suboptions:
      param:
        description: ...
        type: str
  state:
    description: ...
    type: str
    choices: ['present', 'absent']
    default: present
author: clemon
"""

EXAMPLES = """
- name: Example
  c1emon.xikeos.xikeos_<feature>:
    config:
      param: value
    state: present
"""

RETURN = """
commands:
  description: List of commands sent to the device
  returned: always
  type: list
  sample:
    - command1
"""

from ansible.module_utils.basic import AnsibleModule


def get_commands(config, state):
    """Generate CLI commands."""
    commands = []
    # ... command generation logic
    return commands


def main():
    """Main entry point."""
    module_args = dict(
        config=dict(type="dict", options=dict(...)),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    
    config = module.params.get("config") or {}
    state = module.params.get("state", "present")
    
    result = {"changed": False, "commands": []}
    
    commands = get_commands(config, state)
    result["commands"] = commands
    
    if module.check_mode:
        module.exit_json(**result)
    
    if commands:
        result["changed"] = True
    
    module.exit_json(**result)


if __name__ == "__main__":
    main()
```

### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Module file | `xikeos_<feature>.py` | `xikeos_vlans.py` |
| Facts file | `<feature>.py` | `vlans.py` |
| Module name | `xikeos_<feature>` | `xikeos_vlans` |
| Function | `snake_case` | `get_commands` |
| Variable | `snake_case` | `existing_config` |
| Constant | `UPPER_SNAKE_CASE` | `COMMAND_MAP` |
| Class | `PascalCase` | `VlansFacts` |

### Documentation Strings

Use Ansible documentation format:

```python
DOCUMENTATION = """
module: xikeos_<feature>
short_description: Brief description
version_added: "0.2.0"
description:
  - Detailed description
  - Can span multiple lines
options:
  config:
    description:
      - Configuration description
      - Can span multiple lines
    type: dict
    suboptions:
      param:
        description: Parameter description
        type: str
        required: true
        choices: ['option1', 'option2']
        default: option1
  state:
    description:
      - State description
      - C(present) - Creates or updates
      - C(absent) - Removes configuration
    type: str
    choices: ['present', 'absent']
    default: present
author: clemon
"""
```

### Error Handling

Always handle errors gracefully:

```python
def main():
    module = AnsibleModule(...)
    
    try:
        # ... module logic
        commands = get_commands(config, state)
    except ValueError as e:
        module.fail_json(msg="Invalid configuration: {0}".format(str(e)))
    except Exception as e:
        module.fail_json(msg="Unexpected error: {0}".format(str(e)))
    
    # ... rest of module
```

### Check Mode

Always support check mode:

```python
def main():
    module = AnsibleModule(..., supports_check_mode=True)
    
    # ... gather state and build commands
    
    result = {"changed": False, "commands": commands}
    
    if module.check_mode:
        module.exit_json(**result)
    
    # ... apply changes through cliconf/network_cli
```

---

## Git Workflow

### Branch Naming

- `feature/<feature-name>` - New features
- `fix/<bug-description>` - Bug fixes
- `docs/<documentation-update>` - Documentation changes

### Commit Messages

Use conventional commits:

```
feat: Add xikeos_<feature> module

- Implement <feature> management
- Add facts parser for show command
- Include unit tests

Closes #123
```

### Pull Request Checklist

- [ ] Code follows style conventions
- [ ] Unit tests added/updated
- [ ] Documentation updated
- [ ] No syntax errors
- [ ] All tests pass
- [ ] PR description explains changes

---

## Resources

- [Ansible Module Development Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- [ansible.netcommon network_cli documentation](https://docs.ansible.com/ansible/latest/collections/ansible/netcommon/network_cli_connection.html)
- [Netmiko Documentation](https://ktbyers.github.io/netmiko/) — optional CLI behavior reference only
- [Xike Switch CLI Reference](https://www.xike.com/support/cli-reference)

---

## Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Code Review**: Submit a pull request for review
