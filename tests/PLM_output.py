from pathlib import Path

from tests.utils import normalize_text_paths

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks" / "PLM_interact"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references" / "PLM" / "run.sh"

MARKER = "PLM_interact"


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_sh.read_text(), [MARKER])
    expected_text = normalize_text_paths(reference_sh.read_text(), [MARKER])

    assert produced_text == expected_text, (
        f"Produced {output_sh} differs from reference"
    )
