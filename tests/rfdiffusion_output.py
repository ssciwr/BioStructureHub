from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

output_file = REPO_ROOT / "notebooks/protein_design_w_RFDiffusion/run.sh"
reference_file = REPO_ROOT / "references/rfdiffusion/run.sh"


def normalize_paths(text):
    MARKER = "protein_design_w_RFDiffusion"
    lines = []

    for line in text.splitlines():
        if MARKER in line:
            prefix = line.split(MARKER)[0]
            line = line.replace(prefix, "")
        lines.append(line)

    return "\n".join(lines)


def test_run_sh_exists():
    assert output_file.exists(), f"{output_file} was not created by the notebook"


def test_run_sh_content():
    produced = normalize_paths(output_file.read_text())
    expected = normalize_paths(reference_file.read_text())

    assert produced == expected, f"Produced {output_file} differs from reference"
