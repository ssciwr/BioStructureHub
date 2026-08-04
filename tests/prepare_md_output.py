from pathlib import Path
from tests.utils import prepare_results

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "molecular_dynamics" / "output"
DST = REPO_ROOT / "notebooks" / "output"


def test_prepare_results():
    """Ensure reference MD outputs are copied for analysis notebook."""
    prepare_results(SRC, DST)

    assert DST.exists()
