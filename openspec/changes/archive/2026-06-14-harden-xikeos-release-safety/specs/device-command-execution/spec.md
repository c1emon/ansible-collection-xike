## ADDED Requirements

### Requirement: OSPF facts use network operational execution
The OSPFv2 facts provider SHALL gather device output through the collection network operational command utility and SHALL NOT use local controller process execution APIs for device show commands.

#### Scenario: OSPF facts gather show commands through network utility
- **WHEN** `Ospfv2Facts` gathers current OSPF state
- **THEN** it MUST execute `show ip ospf` and related show commands through the collection network operational command path
- **AND** it MUST NOT call `module.run_command()` for device show commands

#### Scenario: OSPF facts failure is surfaced
- **WHEN** OSPF show command execution or parsing fails
- **THEN** the facts provider MUST surface the failure through the module error boundary
- **AND** it MUST NOT silently return partial or empty facts by swallowing the exception
