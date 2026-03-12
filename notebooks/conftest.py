from pathlib import Path
import shutil

NOTEBOOKS_DIR = Path(__file__).resolve().parent

ALPHAFOLD_MODEL_DIR = NOTEBOOKS_DIR / "af3models"
ALPHAFOLD_WORKING_DIR = NOTEBOOKS_DIR / "afold_test"
ALPHAFOLD_RESULTS_DIR_PART1 = ALPHAFOLD_WORKING_DIR / "output"
BOLTZ_WORKING_DIR = NOTEBOOKS_DIR / "boltz_test"
BOLTZGEN_WORKING_DIR = NOTEBOOKS_DIR / "protein_design_w_Boltzgen"
RFDIFFUSION_WORKING_DIR = NOTEBOOKS_DIR / "protein_design_w_RFDiffusion"
BINDCRAFT_WORKING_DIR = NOTEBOOKS_DIR / "protein_design_w_Bindcraft"


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    ALPHAFOLD_MODEL_DIR.mkdir(exist_ok=True)
    ALPHAFOLD_WORKING_DIR.mkdir(exist_ok=True)
    ALPHAFOLD_RESULTS_DIR_PART1.mkdir(exist_ok=True)

    BOLTZ_WORKING_DIR.mkdir(exist_ok=True)
    BOLTZGEN_WORKING_DIR.mkdir(exist_ok=True)
    RFDIFFUSION_WORKING_DIR.mkdir(exist_ok=True)
    BINDCRAFT_WORKING_DIR.mkdir(exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # delete all the created dirs
    shutil.rmtree(ALPHAFOLD_MODEL_DIR)
    shutil.rmtree(RFDIFFUSION_WORKING_DIR)
    shutil.rmtree(BOLTZGEN_WORKING_DIR)
    shutil.rmtree(BINDCRAFT_WORKING_DIR)
    shutil.rmtree(ALPHAFOLD_WORKING_DIR)
    shutil.rmtree(BOLTZ_WORKING_DIR)
