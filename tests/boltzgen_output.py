from pathlib import Path
from tests.utils import normalize_text_paths, load_yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/protein_design_w_Boltzgen"

output_yaml = OUTPUT_DIR / "input.yaml"
reference_yaml = REPO_ROOT / "references/boltzgen/input.yaml"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references/boltzgen/run.sh"


MARKER = "protein_design_w_Boltzgen"


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_sh.read_text(encoding=None), [MARKER])
    expected_text = normalize_text_paths(
        reference_sh.read_text(encoding=None), [MARKER]
    )
    assert produced_text == expected_text, (
        f"Produced {output_sh} differs from reference"
    )


def test_yaml_exists():
    assert output_yaml.exists(), f"{output_yaml} was not created by the notebook"


def test_input_yaml_content():
    produced_yaml = load_yaml(output_yaml)
    expected_yaml = load_yaml(reference_yaml)

    assert produced_yaml == expected_yaml, (
        f"Produced {output_yaml} differs from reference"
    )
