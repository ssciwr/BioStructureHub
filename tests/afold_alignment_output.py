from pathlib import Path
import json
from tests.utils import normalize_text_paths

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/afold_test"

output_json = OUTPUT_DIR / "input.json"
reference_json = REPO_ROOT / "references/afold/input.json"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references/afold/run.sh"


MARKERS = ["afold_test", "af3models"]


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_sh.read_text(), MARKERS)
    expected_text = normalize_text_paths(reference_sh.read_text(), MARKERS)

    assert produced_text == expected_text, (
        f"Produced {output_sh} differs from reference"
    )


def test_input_json_exists():
    assert output_json.exists(), f"{output_json} was not created by the notebook"


def test_input_json_content():
    produced = json.loads(output_json.read_text())
    expected = json.loads(reference_json.read_text())

    assert produced == expected, f"Produced {output_json} differs from reference"
