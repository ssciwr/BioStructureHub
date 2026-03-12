from pathlib import Path
import json
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/afold_test"

output_json = OUTPUT_DIR / "input.json"
reference_json = REPO_ROOT / "references/afold/input.json"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references/afold/run.sh"


MARKERS = ["afold_test", "af3models"]


def normalize_paths(text: str) -> str:
    for marker in MARKERS:
        # Match everything up to the marker, remove it, keep the rest
        text = re.sub(rf"/[^ \n]*?({marker}/?)", r"\1", text)
    return text


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced = normalize_paths(output_sh.read_text())
    expected = normalize_paths(reference_sh.read_text())
    assert produced == expected, f"Produced {output_sh} differs from reference"


def test_input_json_exists():
    assert output_json.exists(), f"{output_json} was not created by the notebook"


def test_input_json_content():
    produced = json.loads(output_json.read_text())
    expected = json.loads(reference_json.read_text())

    assert produced == expected, f"Produced {output_json} differs from reference"
