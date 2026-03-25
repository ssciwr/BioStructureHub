from pathlib import Path
from tests.utils import normalize_text_paths

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/afold_test"


output_sh = OUTPUT_DIR / "run_gpu.sh"
reference_sh = REPO_ROOT / "references/afold/run_gpu.sh"


MARKERS = ["afold_test", "af3models"]


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_sh.read_text(), MARKERS)
    expected_text = normalize_text_paths(reference_sh.read_text(), MARKERS)

    assert produced_text == expected_text, (
        f"Produced {output_sh} differs from reference"
    )
