## ADDED Requirements

### Requirement: Release workflow requires Ansible sanity
The Galaxy release workflow SHALL run Ansible sanity validation for the declared supported Python version or versions and SHALL require it to pass before building or publishing the collection.

#### Scenario: Sanity passes
- **WHEN** all required Ansible sanity tests pass in a fresh collection layout
- **THEN** the release workflow MAY continue to build and publish after its other gates pass

#### Scenario: Sanity fails
- **WHEN** any required Ansible sanity test reports an unapproved finding
- **THEN** the release workflow MUST fail before Galaxy publication

### Requirement: Validation runs before release publication
The repository SHALL run a non-publishing validation workflow for pull requests and protected-branch pushes using gates equivalent to the release validation path.

#### Scenario: Pull request changes collection implementation
- **WHEN** a pull request changes collection code, tests, contracts, documentation metadata, or release configuration
- **THEN** validation MUST run unit tests, strict OpenSpec validation, Ansible sanity, and collection build checks
- **AND** it MUST NOT publish to Galaxy

#### Scenario: Release starts after validated changes
- **WHEN** a GitHub Release is published
- **THEN** the release workflow MUST rerun or depend on equivalent immutable-revision validation before publishing

### Requirement: Compatibility corrections are release-noted and versioned
Externally visible resource-state compatibility corrections SHALL include a changelog fragment and SHALL be published only under a new, never-published collection version.

#### Scenario: Implementation changes replaced or null/reset semantics
- **WHEN** the change alters public `replaced`, omission, null, reset, or removal behavior
- **THEN** the implementation MUST add a changelog fragment that identifies the affected modules and migration behavior
- **AND** it MUST NOT silently ship the correction without operator-facing release notes

#### Scenario: Release version is selected
- **WHEN** maintainers prepare the implemented change for Galaxy publication
- **THEN** `galaxy.yml`, visible version documentation, generated changelog, artifact name, Git tag, and GitHub Release MUST reference the same new version
- **AND** the workflow MUST reject reuse of an already published version

## MODIFIED Requirements

### Requirement: Release workflow uses uv-managed validation
The release workflow SHALL run project validation and Ansible collection commands through an independent uv-managed environment.

#### Scenario: Release validation runs before publish
- **WHEN** the release workflow starts
- **THEN** it MUST install locked dependencies with uv
- **AND** it MUST run unit tests, strict OpenSpec validation, required Ansible sanity tests, and collection build verification before publishing

#### Scenario: Collection build uses uv
- **WHEN** the workflow builds the collection artifact
- **THEN** it MUST run the collection build command through `uv run` from a valid collection layout

## REMOVED Requirements

### Requirement: Release workflow excludes ansible-test sanity
**Reason:** The implementation audit found 61 `validate-modules` issues while the existing release contract explicitly prohibited sanity as a gate. The exclusion permits publication of structurally invalid collection content and is no longer acceptable.

**Migration:** Fix the current sanity baseline, add uv-managed sanity to validation CI, and require the same gate before Galaxy publication.
