import json
from pathlib import Path

from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent

SRC = REPO_ROOT / "references" / "docking" / "ligands" / "HIV_ligands.csv"
DST = REPO_ROOT / "notebooks" / "HIV_ligands.csv"

NB_INPUT = REPO_ROOT / "notebooks" / "Docking.ipynb"


def test_prepare_results():
    """Ensure reference MD inputs are copied for analysis notebook."""
    prepare_file(SRC, DST)

    assert DST.exists()


def rename_vina_path_in_notebook(notebook_path: Path):
    """Rename the path to vina in the notebook."""

    old = "/mnt/sds-hd/sd25g005/docking/bin/vina"
    nb = json.loads(NB_INPUT.read_text(encoding="utf-8"))

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            for i, line in enumerate(cell["source"]):
                if old in line:
                    cell["source"][i] = line.replace(old, "vina")
