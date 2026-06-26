from pathlib import Path
from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent


SRC_cif = REPO_ROOT / "references" / "afold" / "mapping" / "1BT0_A.cif"
DST_cif = REPO_ROOT / "notebooks" / "1BT0_A.cif"


def test_prepare_cif():
    """Ensure reference Boltz input files are copied for prediction notebook."""
    prepare_file(SRC_cif, DST_cif)

    assert DST_cif.exists()
