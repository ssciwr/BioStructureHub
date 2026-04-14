from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

DIRS = {
    "ALPHAFOLD_MODEL_DIR": NOTEBOOKS_DIR / "af3models",
    "ALPHAFOLD_WORKING_DIR": NOTEBOOKS_DIR / "afold_test",
    "ALPHAFOLD_RESULTS_DIR": NOTEBOOKS_DIR / "afold_test" / "output",
    "BOLTZ_WORKING_DIR": NOTEBOOKS_DIR / "boltz_test",
    "BOLTZGEN_WORKING_DIR": NOTEBOOKS_DIR / "protein_design_w_Boltzgen",
    "RFDIFFUSION_WORKING_DIR": NOTEBOOKS_DIR / "protein_design_w_RFDiffusion",
    "BINDCRAFT_WORKING_DIR": NOTEBOOKS_DIR / "protein_design_w_Bindcraft",
    "MD_WORKING_DIR": NOTEBOOKS_DIR / "md_inputs",
}


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # delete all the created dirs
    for path in DIRS.values():
        if path.exists():
            shutil.rmtree(path)
