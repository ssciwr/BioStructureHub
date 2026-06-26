from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "notebooks/"

output_fasta = OUTPUT_DIR / "1BT0_A_seqs.fasta"
reference_fasta = REPO_ROOT / "references/mapping/1BT0_A_seqs.fasta"

output_json = OUTPUT_DIR / "1BT0_A_alignment.json"
reference_json = REPO_ROOT / "references/mapping/1BT0_A_alignment.json"


def test_output_fasta_exists():
    assert output_fasta.exists(), f"{output_fasta} was not created by the notebook"


def test_output_fasta_content():
    produced_text = output_fasta.read_text()
    expected_text = reference_fasta.read_text()

    assert produced_text == expected_text, (
        f"Produced {output_fasta} differs from reference"
    )


def test_output_json_exists():
    assert output_json.exists(), f"{output_json} was not created by the notebook"


def test_output_json_content():
    produced = json.loads(output_json.read_text())
    expected = json.loads(reference_json.read_text())

    assert produced == expected, f"Produced {output_json} differs from reference"
