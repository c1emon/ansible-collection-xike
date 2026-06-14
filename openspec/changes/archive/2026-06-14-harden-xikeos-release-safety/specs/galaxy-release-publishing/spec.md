## ADDED Requirements

### Requirement: Release workflow publishes the declared-version tarball
The Galaxy release workflow SHALL publish the collection tarball that exactly matches the version declared in `galaxy.yml`.

#### Scenario: Exact tarball is selected
- **WHEN** the release workflow builds the collection
- **THEN** it MUST select the tarball whose filename matches the namespace, collection name, and declared `galaxy.yml` version
- **AND** it MUST NOT select a tarball through a broad glob plus first-result ordering

#### Scenario: Expected tarball missing fails release
- **WHEN** the expected declared-version tarball does not exist after build
- **THEN** the workflow MUST fail before attempting to publish to Galaxy

### Requirement: Collection build ignores local artifacts and tooling state
The collection build configuration SHALL exclude local build artifacts, virtual environments, caches, test path scaffolding, and agent/tooling directories from published Galaxy packages.

#### Scenario: Local artifacts are excluded from package
- **WHEN** the collection is built for publication
- **THEN** tarballs, Python caches, test path scaffolding, virtualenv directories, lint/test caches, and local agent/tooling directories MUST NOT be included in the published package

### Requirement: Documentation uses project execution conventions
User and contributor documentation SHALL use project-standard command forms for playbook execution and GitNexus analysis.

#### Scenario: Playbook examples use uv
- **WHEN** documentation shows how to run an Ansible playbook from this project
- **THEN** it MUST use `uv run ansible-playbook` unless explicitly documenting an external user environment

#### Scenario: GitNexus guidance uses global command
- **WHEN** project guidance instructs contributors or agents to refresh GitNexus analysis
- **THEN** it MUST use `gitnexus analyze`
- **AND** it MUST NOT instruct them to use `npx gitnexus analyze`
