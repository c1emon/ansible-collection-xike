## Why

The collection is now merged to `main` but still requires manual, error-prone
publishing steps for Ansible Galaxy releases. A GitHub Release driven publishing
workflow gives maintainers a repeatable release path while preserving Galaxy's
immutable version guarantees.

## What Changes

- Add a GitHub Actions release workflow that publishes the collection to Ansible
  Galaxy when a GitHub Release is published.
- Use `uv` for dependency installation and release validation commands.
- Validate that the release tag version matches `galaxy.yml` before publishing.
- Publish with the GitHub secret `ANSIBLE_GALAXY_API_KEY` passed explicitly to
  `ansible-galaxy collection publish --api-key`.
- Do not run `ansible-test sanity` in the release workflow because the project
  currently has known collection-wide sanity debt.
- Update `galaxy.yml` for the public repository location and Galaxy namespace:
  `namespace: c1emon` and GitHub URLs under
  `https://github.com/c1emon/ansible-collection-xike`.
- **BREAKING**: Change the collection FQCN from `xike.xikeos` to
  `c1emon.xikeos` across documentation, examples, playbooks, tests, and local
  `.test_path` setup so the published namespace is consistent everywhere.

## Capabilities

### New Capabilities

- `galaxy-release-publishing`: Defines how GitHub Releases publish immutable
  Ansible Galaxy collection versions using uv-based validation and a Galaxy API
  token secret.

### Modified Capabilities

- `ansible-network-platform`: The collection namespace/FQCN changes from
  `xike.xikeos` to `c1emon.xikeos`, affecting inventory values, examples,
  playbooks, and import paths.

## Impact

- Adds `.github/workflows/` release automation.
- Updates `galaxy.yml` namespace and repository metadata.
- Updates docs, playbooks, tests, and Python imports that reference the old
  `xike.xikeos` FQCN.
- Requires a repository secret named `ANSIBLE_GALAXY_API_KEY` before release
  publishing can succeed.
- Requires GitHub Releases to use tags matching `galaxy.yml` version, for
  example `v0.1.0` for `version: 0.1.0`.
