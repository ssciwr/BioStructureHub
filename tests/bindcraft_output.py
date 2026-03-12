from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent

output_file = REPO_ROOT / "notebooks/protein_design_w_Bindcraft/input.json"
reference_file = REPO_ROOT / "references/bindcraft/input.json"


def normalize_paths(data):
    data["design_path"] = "<ROOT>/protein_design_w_Bindcraft"
    data["starting_pdb"] = "<ROOT>/protein_design_w_Bindcraft/PDL1.pdb"
    return data


def test_input_json_exists():
    assert output_file.exists(), f"{output_file} was not created by the notebook"


def test_input_json_content():
    produced = json.loads(output_file.read_text())
    expected = json.loads(reference_file.read_text())

    produced = normalize_paths(produced)
    expected = normalize_paths(expected)

    assert produced == expected, f"Produced {output_file} differs from reference"
