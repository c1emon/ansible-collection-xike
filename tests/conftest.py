"""Conftest for xike-xikeos unit tests.

Sets up Python path so that ``ansible_collections.c1emon.xikeos`` imports
resolve to the local collection root without requiring a full Ansible
installation.
"""

import os
import sys
from pathlib import Path

# Collection root: the directory that contains galaxy.yml
COLLECTION_ROOT = Path(__file__).resolve().parent.parent

# We need a directory structure like:
#   <temp>/
#     ansible_collections/
#       c1emon/
#         xikeos/   <-- symlink or actual dir -> COLLECTION_ROOT
#
# Create a wrapper so ``import ansible_collections.c1emon.xikeos`` works.

_COLLECTION_PARENT = COLLECTION_ROOT / ".test_path" / "ansible_collections" / "c1emon"
_COLLECTION_LINK = _COLLECTION_PARENT / "xikeos"


def _ensure_collection_path():
    """Create the namespace directory structure if it doesn't exist."""
    if not _COLLECTION_LINK.exists():
        _COLLECTION_PARENT.mkdir(parents=True, exist_ok=True)
        # Symlink xikeos -> collection root
        os.symlink(str(COLLECTION_ROOT), str(_COLLECTION_LINK))

    # Add the parent of ansible_collections to sys.path
    test_path_parent = str(COLLECTION_ROOT / ".test_path")
    if test_path_parent not in sys.path:
        sys.path.insert(0, test_path_parent)


_ensure_collection_path()
