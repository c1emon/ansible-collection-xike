"""Conftest for xike-xikeos unit tests.

Sets up Python path so that ``ansible_collections.c1emon.xikeos`` imports
resolve to the local collection root without requiring a full Ansible
installation.
"""

import atexit
import os
import shutil
import sys
import tempfile
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

_TEST_PATH = Path(tempfile.mkdtemp(prefix="xikeos-collection-"))
_COLLECTION_PARENT = _TEST_PATH / "ansible_collections" / "c1emon"
_COLLECTION_LINK = _COLLECTION_PARENT / "xikeos"


def _ensure_collection_path():
    """Create a process-owned namespace directory for local collection imports."""
    _COLLECTION_PARENT.mkdir(parents=True, exist_ok=True)
    os.symlink(str(COLLECTION_ROOT), str(_COLLECTION_LINK))

    # Add the parent of ansible_collections to sys.path
    test_path_parent = str(_TEST_PATH)
    if test_path_parent not in sys.path:
        sys.path.insert(0, test_path_parent)
    for collection_path in os.environ.get("ANSIBLE_COLLECTIONS_PATH", "").split(os.pathsep):
        if collection_path and collection_path not in sys.path:
            sys.path.append(collection_path)


_ensure_collection_path()
atexit.register(shutil.rmtree, _TEST_PATH, ignore_errors=True)
