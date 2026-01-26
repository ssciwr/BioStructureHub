from pathlib import Path
import shutil
# import os

# os.environ["HOME"] = os.getcwd()


ALPHAFOLD_MODEL_DIR = Path.home() / "af3models"
ALPHAFOLD_WORKING_DIR = Path.home() / "afold_test"  # must be created by user
ALPHAFOLD_RESULTS_DIR_PART1 = ALPHAFOLD_WORKING_DIR / "output"
BOLTZ_WORKING_DIR = Path.home() / "boltz_test"  # must be created by user
RFDIFFUSION_WORKING_DIR = Path.home() / "protein_design_RFDiffusion"
BINDCRAFT_WORKING_DIR = Path.home() / "protein_design_w_Bindcraft"


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    ALPHAFOLD_MODEL_DIR.mkdir(exist_ok=True)
    ALPHAFOLD_WORKING_DIR.mkdir(exist_ok=True)
    ALPHAFOLD_RESULTS_DIR_PART1.mkdir(exist_ok=True)

    BOLTZ_WORKING_DIR.mkdir(exist_ok=True)
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
    shutil.rmtree(BINDCRAFT_WORKING_DIR)
    # shutil.rmtree(ALPHAFOLD_WORKING_DIR)
    # shutil.rmtree(BOLTZ_WORKING_DIR)
