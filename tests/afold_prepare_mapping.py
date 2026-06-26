from pathlib import Path
from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent


SRC_fasta = REPO_ROOT / "references" / "mapping" / "1BT0_A_seqs.fasta"
DST_fasta = REPO_ROOT / "notebooks" / "1BT0_A_seqs.fasta"

SRC_json = REPO_ROOT / "references" / "mapping" / "1BT0_A_alignment.json"
DST_json = REPO_ROOT / "notebooks" / "1BT0_A_alignment.json"


def test_prepare_fasta():
    """Ensure reference Boltz input files are copied for prediction notebook."""
    prepare_file(SRC_fasta, DST_fasta)

    assert DST_fasta.exists()


def test_prepare_a3m():
    """Ensure reference Boltz input files are copied for prediction notebook."""
    prepare_file(SRC_json, DST_json)

    assert DST_json.exists()
