from .pipeline_steps import (
    fix_phosphate_pdb,
    remove_op3,
    run_pdbfixer,
    run_tleap,
    write_pdb_with_connect,
    write_reorderd_pdb,
)

targets = {"HOP3", "OP3"}


def run_pipeline(basename):
    """
    Run the complete PDB preparation pipeline.

    Parameters
    ----------
    basename : str or Path
        Base name used for all intermediate and output files.
    targets : iterable
        Residue identifiers required for CONECT generation.

    Note
    ----------
    Temporary PDB files need to be written to disk at each step. StringIO was tested.
    """

    # Step 0 - remove OP3
    remove_op3(f"{basename}_protein.pdb", f"{basename}_protein_00.pdb")

    # Step 1 - run tleap to add OP3
    run_tleap(basename, f"{basename}_protein_01.pdb")

    # Step2 - get standard pdb file format with chains via pdbfixer
    run_pdbfixer(f"{basename}_protein_01.pdb", f"{basename}_protein_02.pdb")

    # Step 3 - split residue containing termini to correct terminus and move termini to top of the chain
    write_reorderd_pdb(
        f"{basename}_protein_02.pdb", f"{basename}_protein_03.pdb", targets
    )

    # Step4 -  might not be needed, Fixer to start counting residue ids from 1
    run_pdbfixer(f"{basename}_protein_03.pdb", f"{basename}_protein_04.pdb")

    # Step 5 -  add CONECT for OP3/HOP3 and P
    write_pdb_with_connect(
        f"{basename}_protein_04.pdb", f"{basename}_protein_05.pdb", targets
    )

    fix_phosphate_pdb(
        f"{basename}_protein_05.pdb", f"{basename}_protein_fixed.pdb", thresh=1
    )

    return f"{basename}_protein_fixed.pdb"
