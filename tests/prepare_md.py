from pathlib import Path
from tests.utils import prepare_results

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "molecular_dynamics" / "input"
DST = REPO_ROOT / "notebooks" / "md_inputs"


def test_prepare_results():
    """Ensure reference MD inputs are copied for analysis notebook."""
    prepare_results(SRC, DST)

    assert DST.exists()
