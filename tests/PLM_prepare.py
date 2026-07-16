from pathlib import Path
from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent


SRC_csv = REPO_ROOT / "references" / "PLM" / "test.csv"
DST_csv = REPO_ROOT / "notebooks" / "PLM_interact" / "test.csv"


def test_prepare_csv():
    """Ensure reference PLM input files are copied for prediction notebook."""
    prepare_file(SRC_csv, DST_csv)

    assert DST_csv.exists()
