## ADDED Requirements

### Requirement: Sanitization is centralized at orchestration exits
Module entrypoints and shared lifecycle helpers SHALL route all success and failure payloads that can contain device or command data through a shared recursive sanitizer immediately before the Ansible exit boundary.

#### Scenario: Typed error contains nested unsafe context
- **WHEN** a typed Xike OS error contains commands, detail, response, or nested resource context
- **THEN** the orchestration boundary MUST sanitize the complete payload before `fail_json`

#### Scenario: Generic exception contains sensitive text
- **WHEN** a caught generic exception string contains known sensitive syntax
- **THEN** the returned error and detail fields MUST be sanitized before `fail_json`

#### Scenario: Successful result contains device response
- **WHEN** a module success result contains a device response or raw configuration fragment
- **THEN** the orchestration boundary MUST sanitize it before `exit_json`

## MODIFIED Requirements

### Requirement: Failure payloads preserve redaction boundaries
Module failure payloads SHALL NOT expose sensitive command operands, device output, running configuration, response data, or exception text and SHALL preserve safe operational context after recursive sanitization.

#### Scenario: Failure includes command output or config text
- **WHEN** a failure payload includes device output, running configuration, command data, or exception text derived from those values
- **THEN** the complete nested payload MUST be sanitized before returning the module failure

#### Scenario: Apply may be partial
- **WHEN** sanitization is applied to a partial-change failure
- **THEN** changed status, partial-change status, safe resource identity, and redacted command structure MUST remain available
- **AND** raw credential values MUST not be returned
