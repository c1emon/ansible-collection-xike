## ADDED Requirements

### Requirement: Controller injects bundled parser templates
Modules that need parser templates at runtime SHALL support receiving collection-owned template content from their action plugins through internal module arguments.

#### Scenario: VLAN action plugin injects TextFSM template
- **WHEN** `xikeos_vlans` runs through its action plugin
- **THEN** the action plugin MUST load the bundled `show_vlan.textfsm` template on the controller and pass its content to the module using an internal argument.

#### Scenario: Missing controller-side template fails explicitly
- **WHEN** the action plugin cannot find a required bundled parser template
- **THEN** execution MUST fail with an actionable error identifying the missing template.

### Requirement: Module runtime does not require template data files
Modules SHALL parse using injected template content when it is provided and MUST NOT require non-Python parser template files to exist inside the AnsiballZ payload.

#### Scenario: AnsiballZ payload omits template file
- **WHEN** a module runs from an AnsiballZ payload that does not contain `.textfsm` or `.ttp` data files
- **THEN** the parser MUST still parse successfully using the injected template content.

### Requirement: Parser helpers fail explicitly when templates are unavailable
Parser helpers SHALL fail explicitly if a requested template is neither injected nor available as a local file.

#### Scenario: No injected or local template exists
- **WHEN** a parser helper is invoked without injected template content and the local template file is missing
- **THEN** it MUST raise an actionable missing-template error rather than silently using a duplicated builtin fallback.
