import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "boltz" / "boltz_results_input_file"
DST = REPO_ROOT / "notebooks" / "boltz_test" / "boltz_results_input_file"


def test_prepare_boltz_results():
    """Copy reference Boltz results so analysis notebook can read them."""

    if DST.exists():
        shutil.rmtree(DST)

    shutil.copytree(SRC, DST, dirs_exist_ok=True)

    assert DST.exists()
