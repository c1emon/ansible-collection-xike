## Purpose
Define the internal TTP-backed parsing behavior for converting Xike OS command output into existing facts and resource module return contracts using collection-bundled templates.

## Requirements

### Requirement: Bundled TTP templates parse internal command output
The collection SHALL support internal facts parsers that parse Xike OS command output using collection-bundled TTP templates.

#### Scenario: VLAN brief output is parsed with a bundled template
- **WHEN** the VLAN facts parser receives `show vlan brief` command output
- **THEN** it MUST parse the output using a bundled TTP template owned by the collection.

#### Scenario: Parser handles empty command output
- **WHEN** the VLAN facts parser receives empty command output
- **THEN** it MUST return an empty VLAN list without raising an error.

### Requirement: TTP parser results preserve existing facts contracts
Internal TTP-based parsers SHALL normalize parsed template results into the same return contracts that existing facts and resource modules consume.

#### Scenario: VLAN fields are normalized after template parsing
- **WHEN** `show vlan brief` output contains VLAN ID, name, status, and ports fields
- **THEN** the VLAN parser MUST return dictionaries with integer `vlan_id`, string `name`, string `state`, string `status`, and list-valued `ports` fields.

#### Scenario: VLAN without ports remains compatible
- **WHEN** `show vlan brief` output contains a VLAN row without a ports column value
- **THEN** the VLAN parser MUST return that VLAN with `ports` set to an empty list.

### Requirement: TTP execution is safe for Ansible module contexts
Internal TTP parsing SHALL execute in single-process mode suitable for Ansible module and unit-test execution.

#### Scenario: Template helper parses without worker processes
- **WHEN** an internal parser invokes the shared TTP parsing helper
- **THEN** the helper MUST invoke TTP parsing in single-process mode.

### Requirement: Bundled parser templates are packaged with the collection
The collection SHALL include internal `.ttp` template files in the built Ansible collection artifact.

#### Scenario: Collection artifact contains VLAN template
- **WHEN** the collection is built for distribution
- **THEN** the artifact MUST include the bundled template used to parse `show vlan brief` output.
