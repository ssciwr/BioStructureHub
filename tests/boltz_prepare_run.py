from pathlib import Path
from tests.utils import prepare_file

REPO_ROOT = Path(__file__).resolve().parent.parent


SRC_fasta = REPO_ROOT / "references" / "boltz" / "insulin.fasta"
DST_fasta = REPO_ROOT / "notebooks" / "boltz_test" / "insulin.fasta"

SRC_a3m = (
    REPO_ROOT
    / "references"
    / "boltz"
    / "sp_P01308_INS_HUMAN_Insulin_OS_Homo_sapiens_OX_9606_GN_INS_PE_1_SV_1.a3m"
)
DST_a3m = (
    REPO_ROOT
    / "notebooks"
    / "boltz_test"
    / "sp_P01308_INS_HUMAN_Insulin_OS_Homo_sapiens_OX_9606_GN_INS_PE_1_SV_1.a3m"
)


def test_prepare_fasta():
    """Ensure reference Boltz input files are copied for prediction notebook."""
    prepare_file(SRC_fasta, DST_fasta)

    assert DST_fasta.exists()


def test_prepare_a3m():
    """Ensure reference Boltz input files are copied for prediction notebook."""
    prepare_file(SRC_a3m, DST_a3m)

    assert DST_a3m.exists()
