import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "afold" / "output_gpu"
DST = REPO_ROOT / "notebooks" / "afold_test" / "output_gpu"


def test_prepare_afold_results():
    """Copy reference Afold results so analysis notebook can read them."""

    if DST.exists():
        shutil.rmtree(DST)

    shutil.copytree(SRC, DST, dirs_exist_ok=True)

    assert DST.exists()
