from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks"

output_box = OUTPUT_DIR / "box_dimensions.txt"
reference_box = REPO_ROOT / "references/docking/box_dimensions.txt"


def test_box_exists():
    assert output_box.exists(), f"{output_box} was not created by the notebook"


def test_box_content():
    produced_text = output_box.read_text(encoding=None)
    expected_text = reference_box.read_text(encoding=None)

    assert produced_text == expected_text, (
        f"Produced {output_box} differs from reference"
    )
