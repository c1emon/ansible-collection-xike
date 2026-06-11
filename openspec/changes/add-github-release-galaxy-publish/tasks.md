## 1. Collection Metadata and FQCN Migration

- [x] 1.1 Update `galaxy.yml` namespace to `c1emon` and repository, documentation, homepage, and issues URLs to `https://github.com/c1emon/ansible-collection-xike`.
- [x] 1.2 Replace user-facing `xike.xikeos` FQCN references with `c1emon.xikeos` in README, docs, playbooks, and inventory examples.
- [x] 1.3 Update Python test imports and local collection path setup from `ansible_collections/xike/xikeos` to `ansible_collections/c1emon/xikeos`.
- [x] 1.4 Verify no stale `xike.xikeos` references remain except historical archived OpenSpec content where preserving history is intentional.

## 2. GitHub Release Publishing Workflow

- [x] 2.1 Add a GitHub Actions workflow triggered by `release.published` only.
- [x] 2.2 Configure the workflow to install `uv`, set up Python, and run `uv sync --group dev`.
- [x] 2.3 Add a release tag check that strips an optional leading `v` and compares the result to `galaxy.yml` `version`.
- [x] 2.4 Run `uv run pytest tests/unit` before collection build.
- [x] 2.5 Build the collection with `uv run ansible-galaxy collection build --force`.
- [x] 2.6 Publish the built tarball with `uv run ansible-galaxy collection publish ... --api-key "${{ secrets.ANSIBLE_GALAXY_API_KEY }}"`.
- [x] 2.7 Ensure the release workflow does not run `ansible-test sanity`.

## 3. Documentation

- [x] 3.1 Document the Galaxy release process, including GitHub Release creation and immutable version constraints.
- [x] 3.2 Document the required repository secret `ANSIBLE_GALAXY_API_KEY`.
- [x] 3.3 Document the local `.test_path` setup using `.test_path/ansible_collections/c1emon/xikeos`.
- [x] 3.4 Document that Automation Hub publishing is out of scope for this workflow.

## 4. Validation

- [x] 4.1 Run `uv run pytest tests/unit` after FQCN migration.
- [x] 4.2 Run `uv run ansible-galaxy collection build --force` and verify the generated tarball uses the `c1emon-xikeos-<version>.tar.gz` naming pattern.
- [x] 4.3 Run live read-only playbook syntax checks using `ANSIBLE_COLLECTIONS_PATH=.test_path`.
- [x] 4.4 Run `openspec validate add-github-release-galaxy-publish --strict`.
- [x] 4.5 Run GitNexus change detection before committing implementation changes.
