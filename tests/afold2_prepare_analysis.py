from pathlib import Path
from tests.utils import prepare_results

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "afold2" / "output"
DST = REPO_ROOT / "notebooks" / "alphafold2" / "output" / "insulin"


def test_prepare_results():
    """Ensure reference Afold results are copied for analysis notebook."""
    prepare_results(SRC, DST)

    assert DST.exists()
