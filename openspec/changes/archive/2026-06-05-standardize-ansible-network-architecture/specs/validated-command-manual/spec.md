## ADDED Requirements

### Requirement: Manual sections used by modules are structurally valid
Documentation used as command authority for implemented modules SHALL have valid headings, command blocks, and tables for the relevant sections.

#### Scenario: Implemented command references manual section
- **WHEN** a module implementation relies on a command from `docs/manual_zh.md`
- **THEN** the corresponding manual section MUST have readable structure and MUST be checked against the source manual or observed device behavior.

### Requirement: Damaged generated manual content is not treated as authoritative
The collection SHALL NOT treat malformed generated Markdown as authoritative for command syntax, prompts, or save behavior.

#### Scenario: Manual Markdown is malformed
- **WHEN** a generated manual section has broken headings, shifted tables, or command examples inside incorrect code blocks
- **THEN** implementation MUST validate the needed command against the source PDF or real device output before using it.

### Requirement: Architecture documentation distinguishes references from dependencies
The documentation SHALL distinguish external references such as Netmiko Raisecom and Genie/pyATS from required runtime dependencies.

#### Scenario: User reads parser or connection guidance
- **WHEN** documentation mentions Netmiko, TextFSM, Genie, or pyATS
- **THEN** it MUST state whether the item is a required dependency, optional tool, or architectural reference.
