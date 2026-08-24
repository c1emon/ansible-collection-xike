# Ansible sanity baseline

This baseline was captured from the pre-change source commit `c99827e`
(the parent of the change-spec commit) in an isolated canonical collection
namespace. It used Python 3.12 and ansible-core 2.21 with the declared
`ansible.netcommon` and `ansible.utils` dependencies.

```sh
ansible-test sanity --python 3.12
```

The run exercised 24 sanity checks and failed these seven categories, without
adding a broad sanity exclusion:

| Check | Baseline failure scope |
| --- | --- |
| `import` | `xikeos_facts` imported a module from an invalid collection context. |
| `no-smart-quotes` | Three converted-manual Unicode quotes. |
| `pep8` | 27 style violations across plugins and tests. |
| `pylint` | 46 findings, including Python-version type-analysis false positives. |
| `runtime-metadata` | Unsupported dependency metadata key. |
| `shebang` | Eight non-module shebangs. |
| `validate-modules` | 61 module-header, author, argument-documentation, and return-schema issues. |

The current support matrix is validated separately after remediation; its
success must not be read as device/HIL evidence.
