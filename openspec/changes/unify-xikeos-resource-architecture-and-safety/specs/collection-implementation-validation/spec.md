## ADDED Requirements

### Requirement: Unit test collection layout is relocatable
The unit-test harness SHALL resolve the current checkout as `ansible_collections.c1emon.xikeos` without relying on a persistent absolute symlink to a previous checkout location.

#### Scenario: Checkout path changes
- **WHEN** the repository is moved or tested from a different absolute path
- **THEN** unit-test collection imports MUST resolve to the current checkout
- **AND** stale local test scaffolding MUST NOT cause collection-time `FileExistsError`

#### Scenario: Fresh checkout runs tests
- **WHEN** declared Python and Ansible collection dependencies are installed in a fresh uv-managed environment
- **THEN** the full unit suite MUST run without manual symlink repair

### Requirement: Runtime-sensitive tests use Ansible-normalized parameters
Tests for omitted fields, defaults, aliases, nested options, and secret options SHALL exercise the same Ansible argument validation behavior used by module execution.

#### Scenario: Nested option is omitted
- **WHEN** a test asserts behavior that depends on an omitted nested option
- **THEN** it MUST pass the input through Ansible argument validation before invoking normalization or lifecycle planning

#### Scenario: Pure planner test does not need Ansible
- **WHEN** a test covers only canonical reconciler behavior
- **THEN** it MAY use canonical state directly
- **AND** separate boundary coverage MUST prove raw module input normalizes to that canonical state

### Requirement: Ansible sanity findings are resolved explicitly
The collection SHALL pass the required `ansible-test sanity` suite without broad exclusions that conceal module contract failures.

#### Scenario: validate-modules checks documentation
- **WHEN** `validate-modules` compares module documentation, argument specifications, return schemas, authors, license headers, and import placement
- **THEN** the collection MUST have zero unapproved findings

#### Scenario: Internal injected argument is validated
- **WHEN** a controller-injected internal argument is intentionally absent from public documentation
- **THEN** the implementation MUST use an Ansible-supported internal pattern or a narrow documented validation mechanism
- **AND** it MUST NOT expose the argument as user-facing API merely to silence validation

### Requirement: Controller support matrix is finite and authoritative
The collection SHALL define one finite, machine-readable support matrix whose entries are the authoritative supported Python minor and compatible `ansible-core` series combinations.

#### Scenario: Metadata declares controller support
- **WHEN** `pyproject.toml`, `meta/runtime.yml`, README, architecture documentation, or release configuration declares Python or Ansible support
- **THEN** the declaration MUST describe no broader set than the authoritative matrix
- **AND** the uv lock MUST resolve every matrix entry

#### Scenario: Validation runs the support matrix
- **WHEN** pull-request, protected-branch, or release validation runs
- **THEN** every matrix entry MUST run the required unit and Ansible sanity gates
- **AND** an untested open-ended `>=` range MUST NOT be presented as fully supported

### Requirement: Validation evidence is capability honest
Software validation SHALL distinguish contract/unit/sanity/build evidence from physical XikeOS device evidence.

#### Scenario: Software-only validation passes
- **WHEN** unit, OpenSpec, sanity, and build checks pass without a physical device
- **THEN** the change MAY claim software validation
- **AND** it MUST NOT claim physical command compatibility or production approval

#### Scenario: Live read-only validation is available
- **WHEN** a supported SKS8300-class target is available
- **THEN** gather and check-mode evidence SHOULD be recorded separately with model and firmware context
