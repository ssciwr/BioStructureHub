from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/boltz_test"

output_yaml = OUTPUT_DIR / "input_file.yaml"
reference_yaml = REPO_ROOT / "references/boltz/input_file.yaml"

output_sh = OUTPUT_DIR / "run.sh"
reference_sh = REPO_ROOT / "references/boltz/run.sh"


MARKER = "boltz_test"


def normalize_paths(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if MARKER in line:
            # Keep command intact, strip everything before the marker in paths
            line = (
                line[: line.find(MARKER)].split()[0] + " " + line[line.find(MARKER) :]
            )
        lines.append(line)
    return "\n".join(lines)


def normalize_msa_paths(yaml_dict):
    """Strip absolute prefix from msa fields only."""
    for seq in yaml_dict.get("sequences", []):
        protein = seq.get("protein", {})
        msa = protein.get("msa")
        if msa and MARKER in msa:
            protein["msa"] = MARKER + msa.split(MARKER, 1)[-1]
    return yaml_dict


def test_run_sh_exists():
    assert output_sh.exists(), f"{output_sh} was not created by the notebook"


def test_run_sh_content():
    produced = normalize_paths(output_sh.read_text())
    expected = normalize_paths(reference_sh.read_text())
    assert produced == expected, f"Produced {output_sh} differs from reference"


def test_yaml_exists():
    assert output_yaml.exists(), f"{output_yaml} was not created by the notebook"


def test_input_yaml_content():
    produced = yaml.safe_load(output_yaml.read_text())
    expected = yaml.safe_load(reference_yaml.read_text())

    produced = normalize_msa_paths(produced)
    expected = normalize_msa_paths(expected)

    assert produced == expected, f"Produced {output_yaml} differs from reference"
