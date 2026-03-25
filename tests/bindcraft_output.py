from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent

output_file = REPO_ROOT / "notebooks/protein_design_w_Bindcraft/input.json"
reference_file = REPO_ROOT / "references/bindcraft/input.json"

marker = "protein_design_w_Bindcraft"


def normalize_paths(data, marker, root_placeholder="<ROOT>"):
    """
    Normalize absolute paths in JSON data:
    - Replace absolute JSON paths with placeholder + marker and normalize separators
    - Ensures 'design_path' and 'starting_pdb' use Linux-style '/'  on Windows
    """
    data["design_path"] = f"{root_placeholder}/{marker}"
    data["starting_pdb"] = f"{root_placeholder}/{marker}/PDL1.pdb"

    # handle Windows paths
    data["design_path"] = data["design_path"].replace("\\", "/")
    data["starting_pdb"] = data["starting_pdb"].replace("\\", "/")

    return data


def test_input_json_exists():
    assert output_file.exists(), f"{output_file} was not created by the notebook"


def test_input_json_content():
    produced = json.loads(output_file.read_text())
    expected = json.loads(reference_file.read_text())

    produced = normalize_paths(produced, marker)
    expected = normalize_paths(expected, marker)

    assert produced == expected, f"Produced {output_file} differs from reference"
