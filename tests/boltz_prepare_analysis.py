from pathlib import Path
from tests.utils import prepare_results

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "boltz" / "boltz_results_insulin"
DST = REPO_ROOT / "notebooks" / "boltz_test" / "boltz_results_insulin"


def test_prepare_results():
    """Ensure reference Boltz results are copied for analysis notebook."""
    prepare_results(SRC, DST)

    assert DST.exists()
