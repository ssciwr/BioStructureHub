from pathlib import Path
from tests.utils import normalize_text_paths

REPO_ROOT = Path(__file__).resolve().parent.parent

output_file = REPO_ROOT / "notebooks/protein_design_w_RFDiffusion/run.sh"
reference_file = REPO_ROOT / "references/rfdiffusion/run.sh"


MARKER = "protein_design_w_RFDiffusion"


def test_run_sh_exists():
    assert output_file.exists(), f"{output_file} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_file.read_text(), [MARKER])
    expected_text = normalize_text_paths(reference_file.read_text(), [MARKER])

    assert produced_text == expected_text, (
        f"Produced {output_file} differs from reference"
    )
