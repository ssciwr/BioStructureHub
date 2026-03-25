from pathlib import Path
from tests.utils import normalize_text_paths, load_yaml
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/boltz_test"

output_yaml = OUTPUT_DIR / "input_file.yaml"
reference_yaml = REPO_ROOT / "references/boltz/input_file.yaml"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references/boltz/run.sh"


MARKER = "boltz_test"


def normalize_msa_paths(yaml_dict: Dict[str, Any], marker: str) -> Dict[str, Any]:
    """
    Strip absolute prefixes from msa fields only.
    This is very tailored to the structure of the input YAML produced in the Boltz notebook, but it is sufficient for our testing purposes.
    """
    for seq in yaml_dict.get("sequences", []):
        protein = seq.get("protein", {})
        msa = protein.get("msa")
        if msa and marker in msa:
            prefix, suffix = msa.split(marker, 1)
            # replace backslashes in the suffix only to please Windows
            protein["msa"] = marker + suffix.replace("\\", "/")
    return yaml_dict


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced_text = normalize_text_paths(output_sh.read_text(), [MARKER])
    expected_text = normalize_text_paths(reference_sh.read_text(), [MARKER])
    assert produced_text == expected_text, (
        f"Produced {output_sh} differs from reference"
    )


def test_yaml_exists():
    assert output_yaml.exists(), f"{output_yaml} was not created by the notebook"


def test_input_yaml_content():
    produced_yaml = normalize_msa_paths(load_yaml(output_yaml), MARKER)
    expected_yaml = normalize_msa_paths(load_yaml(reference_yaml), MARKER)

    assert produced_yaml == expected_yaml, (
        f"Produced {output_yaml} differs from reference"
    )
