## Purpose
Define how GitHub Releases publish immutable Ansible Galaxy collection versions using uv-based validation and a Galaxy API token secret.

## Requirements

### Requirement: GitHub Releases publish the collection to Galaxy
The repository SHALL publish the Ansible collection to Ansible Galaxy when a
GitHub Release is published.

#### Scenario: Release publication triggers Galaxy publish
- **WHEN** a GitHub Release is published for the repository
- **THEN** the release workflow MUST build the collection and publish the built
  tarball to Ansible Galaxy.

#### Scenario: Non-release events do not publish
- **WHEN** a pull request or ordinary branch push runs repository validation
- **THEN** the workflow MUST NOT publish the collection to Ansible Galaxy.

### Requirement: Release workflow uses uv-managed validation
The release workflow SHALL run project validation and Ansible collection commands
through `uv`.

#### Scenario: Release validation runs before publish
- **WHEN** the release workflow starts
- **THEN** it MUST install dependencies with `uv` and run unit tests with
  `uv run pytest tests/unit` before publishing.

#### Scenario: Collection build uses uv
- **WHEN** the workflow builds the collection artifact
- **THEN** it MUST run `uv run ansible-galaxy collection build --force` from the
  collection root.

### Requirement: Release tag matches collection version
The release workflow SHALL verify that the GitHub Release tag version matches
the version declared in `galaxy.yml`.

#### Scenario: Matching version continues
- **WHEN** the GitHub Release tag is `v0.2.0` and `galaxy.yml` declares
  `version: 0.2.0`
- **THEN** the workflow MUST continue to build and publish.

#### Scenario: Mismatched version fails
- **WHEN** the GitHub Release tag version differs from `galaxy.yml` version
- **THEN** the workflow MUST fail before publishing to Ansible Galaxy.

### Requirement: Galaxy API key is provided through GitHub secrets
The release workflow SHALL use a GitHub secret named `ANSIBLE_GALAXY_API_KEY` to
authenticate publication to Ansible Galaxy.

#### Scenario: Publish passes explicit API key
- **WHEN** the workflow publishes the built tarball
- **THEN** it MUST pass `${{ secrets.ANSIBLE_GALAXY_API_KEY }}` explicitly to
  `ansible-galaxy collection publish --api-key`.

#### Scenario: Missing API key fails publishing
- **WHEN** `ANSIBLE_GALAXY_API_KEY` is not configured or is invalid
- **THEN** the publish step MUST fail without reporting a successful release.

### Requirement: Release workflow excludes ansible-test sanity
The release workflow SHALL NOT run `ansible-test sanity` as a required release
gate for this change.

#### Scenario: Release validation omits sanity
- **WHEN** the release workflow validates a release
- **THEN** it MUST run unit tests and collection build but MUST NOT require
  `ansible-test sanity` to pass.

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
