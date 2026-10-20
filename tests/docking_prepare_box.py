from pathlib import Path

from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "docking" / "protein" / "HIV1protease.pdb"
DST = REPO_ROOT / "notebooks" / "HIV1protease.pdb"


def test_prepare_results():
    """Ensure reference MD inputs are copied for analysis notebook."""
    prepare_file(SRC, DST)

    assert DST.exists()
