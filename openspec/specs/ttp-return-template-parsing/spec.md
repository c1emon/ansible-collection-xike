## Purpose
Define the internal template-backed parsing behavior for converting Xike OS command output into existing facts and resource module return contracts using collection-bundled TTP and TextFSM templates.

## Requirements

### Requirement: Bundled templates parse internal command output
The collection SHALL support internal facts parsers that parse Xike OS command output using collection-bundled templates. At module runtime, parser templates SHALL be supplied by controller-side injection when the module is executed through an action plugin, with local template files used only for local development and unit-test paths.

#### Scenario: VLAN output is parsed with a bundled template
- **WHEN** the VLAN facts parser receives `show vlan` command output
- **THEN** it MUST parse the output using a bundled TextFSM template owned by the collection.

#### Scenario: Parser handles empty command output
- **WHEN** the VLAN facts parser receives empty command output
- **THEN** it MUST return an empty VLAN list without raising an error.

#### Scenario: Injected template content is preferred
- **WHEN** injected template content is provided for a parser template name
- **THEN** the parser helper MUST use the injected template content instead of reading a template file from the module runtime filesystem.

### Requirement: Template parser results preserve existing facts contracts
Internal template-based parsers SHALL normalize parsed template results into the same return contracts that existing facts and resource modules consume.

#### Scenario: VLAN fields are normalized after template parsing
- **WHEN** `show vlan` output contains VLAN ID, name, type, media, and ports fields
- **THEN** the VLAN parser MUST return dictionaries with integer `vlan_id`, string `name`, string `type`, string `media`, string `state`, string `status`, and list-valued `ports` fields.

#### Scenario: VLAN without ports remains compatible
- **WHEN** `show vlan` output contains a VLAN row without a ports column value
- **THEN** the VLAN parser MUST return that VLAN with `ports` set to an empty list.

### Requirement: Template execution is safe for Ansible module contexts
Internal template parsing SHALL execute in single-process mode suitable for Ansible module and unit-test execution.

#### Scenario: Template helper parses without worker processes
- **WHEN** an internal parser invokes the shared TTP parsing helper
- **THEN** the helper MUST invoke TTP parsing in single-process mode.

#### Scenario: Complex table parser uses TextFSM in-process
- **WHEN** an internal parser invokes the shared TextFSM parsing helper
- **THEN** the helper MUST parse with the in-process TextFSM runtime.

### Requirement: Bundled parser templates are packaged with the collection
The collection SHALL include internal template files in the built Ansible collection artifact.

#### Scenario: Collection artifact contains VLAN template
- **WHEN** the collection is built for distribution
- **THEN** the artifact MUST include the bundled template used to parse `show vlan` output.
