## ADDED Requirements

### Requirement: Published package excludes legacy connection plugin
The published Galaxy collection package SHALL exclude the legacy custom XikeOS connection plugin so that the forward-facing platform path remains `ansible.netcommon.network_cli` with `ansible_network_os: c1emon.xikeos.xikeos`.

#### Scenario: Galaxy build omits legacy connection plugin
- **WHEN** the collection is built for publication
- **THEN** the resulting collection tarball MUST NOT contain `plugins/connection/xikeos.py`

#### Scenario: Documentation omits legacy connection examples
- **WHEN** users read inventory or connection setup documentation
- **THEN** examples MUST use `ansible_connection: ansible.netcommon.network_cli`
- **AND** examples MUST use `ansible_network_os: c1emon.xikeos.xikeos`
- **AND** examples MUST NOT present `connection: c1emon.xikeos.xikeos` as the supported setup
