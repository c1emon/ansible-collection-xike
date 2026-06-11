## Context

The project currently has a valid Ansible collection structure and a
`galaxy.yml`, but publishing to Galaxy is a manual process. The repository has
also moved to `https://github.com/c1emon/ansible-collection-xike`, while
`galaxy.yml` still references the old `andy/xike-xikeos` URLs and the
collection namespace remains `xike`.

Galaxy publication is immutable at the version level: once a version in
`galaxy.yml` is published, the same version cannot be replaced. That makes the
release trigger and version checks important. The project also standardizes on
`uv` for local commands and should use the same execution model in CI.

## Goals / Non-Goals

**Goals:**

- Publish the collection to Ansible Galaxy from GitHub Release publication.
- Use `c1emon.xikeos` consistently as the collection FQCN.
- Keep the release workflow deterministic with `uv` managed commands.
- Fail releases early when the GitHub Release tag does not match
  `galaxy.yml` version.
- Document the required `ANSIBLE_GALAXY_API_KEY` GitHub secret and release
  procedure.

**Non-Goals:**

- Publishing to Automation Hub or Private Automation Hub.
- Running `ansible-test sanity` as a release gate.
- Automating version bumps or changelog generation.
- Supporting both `xike.xikeos` and `c1emon.xikeos` FQCNs at the same time.

## Decisions

### Decision 1: Use GitHub Release publication as the release trigger

The workflow will run on `release` events with `types: [published]`.

Alternatives considered:

- `push.tags`: simpler, but a pushed tag immediately attempts publication and
  is easier to trigger accidentally.
- `workflow_dispatch`: useful for manual retries, but not as naturally tied to
  public release records.

GitHub Release publication gives maintainers a deliberate final confirmation
before an immutable Galaxy version is published.

### Decision 2: Use `uv` for release validation and publishing commands

The workflow will install dependencies with `uv sync --group dev` and run
commands through `uv run`, including tests, collection build, and publish.

This matches the project's local command convention and avoids a separate CI
dependency path based on raw `pip` or globally installed Ansible.

### Decision 3: Require release tag and `galaxy.yml` version to match

The workflow will strip a leading `v` from `GITHUB_REF_NAME` and compare it to
the `version:` field in `galaxy.yml`. A mismatch fails before build or publish.

This prevents publishing a release named `v0.1.1` that actually uploads
`version: 0.1.0`.

### Decision 4: Publish with explicit API key argument

The workflow will pass `${{ secrets.ANSIBLE_GALAXY_API_KEY }}` explicitly to
`ansible-galaxy collection publish --api-key`. The CLI does not rely on implicit
environment-variable discovery for the Galaxy API key.

### Decision 5: Change the collection namespace globally

The implementation will change the collection namespace to `c1emon` in
`galaxy.yml` and update all user-facing FQCNs and test imports from
`xike.xikeos` to `c1emon.xikeos`.

This is a breaking change but avoids a worse publication mismatch where Galaxy
installs `c1emon.xikeos` while examples and tests still instruct users to call
`xike.xikeos`.

## Risks / Trade-offs

- [Risk] Namespace change breaks existing users of `xike.xikeos`. → Mitigation:
  document the breaking FQCN change and update all examples, playbooks, tests,
  and inventory values consistently.
- [Risk] A release can fail after GitHub Release publication if the version was
  already uploaded to Galaxy. → Mitigation: document version immutability and
  require version bumps before each release.
- [Risk] Skipping `ansible-test sanity` allows packaging issues that unit tests
  do not catch. → Mitigation: still run unit tests and collection build; leave
  sanity enablement for a future change after existing sanity debt is resolved.
- [Risk] Secret misconfiguration causes publish failure. → Mitigation: document
  the required `ANSIBLE_GALAXY_API_KEY` secret and make the publish step fail
  clearly.

## Migration Plan

1. Add the release workflow and documentation.
2. Update `galaxy.yml` namespace and repository metadata.
3. Replace `xike.xikeos` references with `c1emon.xikeos` in docs, playbooks,
   tests, and Python imports.
4. Run unit tests and build the collection with `uv`.
5. Configure `ANSIBLE_GALAXY_API_KEY` in GitHub repository secrets.
6. Publish by creating a GitHub Release whose tag matches `galaxy.yml` version.

Rollback for the workflow is removing or disabling the release workflow before
publishing another release. Published Galaxy versions themselves cannot be
modified or removed as part of normal rollback.

## Open Questions

- Should release publication also upload the built tarball as a GitHub Release
  asset, or is Galaxy publication sufficient for now?
