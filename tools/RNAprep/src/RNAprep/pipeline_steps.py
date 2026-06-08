from pdbfixer import PDBFixer
from Bio.PDB.Residue import Residue
from openmm.app import PDBFile
from pathlib import Path
import subprocess
from pdb_io import load_pdb, save_pdb


def run_tleap(basename, output_pdb):
    """
    Run AmberTools tleap to generate protonated termini and AMBER topology/coordinates.

    This function writes a temporary tleap input script, executes tleap via subprocess,
    and captures stdout/stderr into a log file.

    Parameters
    ----------
    basename : str or Path
        Base filename used for all input/output files. Expected inputs/outputs:
        - {basename}_protein.pdb : input structure for tleap
        - {basename}_tleap.in    : generated tleap input script
        - {basename}_tleap.log   : tleap stdout/stderr log
        - {basename}_protein_tleap.pdb : output PDB from tleap
        - {basename}.prmtop      : AMBER topology file
        - {basename}.rst7        : AMBER restart file

    Raises
    ------
    subprocess.CalledProcessError
        If tleap execution fails (non-zero exit code).
    """

    tleap_in = Path(f"{basename}_tleap.in")
    tleap_log = Path(f"{basename}_tleap.log")

    tleap_in.write_text(f"""
source leaprc.protein.ff14SB
source leaprc.RNA.OL3
source leaprc.DNA.OL21

loadoff terminal_monophosphate.lib

rna = loadpdb {basename}_protein.pdb
check rna

savepdb rna {output_pdb}
saveamberparm rna {basename}.prmtop {basename}.rst7

quit
""")

    with tleap_log.open("w") as log:
        subprocess.run(
            ["tleap", "-f", str(tleap_in)],
            stdout=log,
            stderr=subprocess.STDOUT,
            check=True,
        )


def run_pdbfixer(input_pdb, output_pdb):
    """
    Run PDBFixer to identify missing residues/atoms and write a fixed PDB.

    Parameters
    ----------
    input_pdb : str
        Input PDB filename.
    output_pdb : str, optional
        Output PDB filename. If None, appends '_fixed' to the input name.

    Returns
    -------
    None
    """
    input_pdb = Path(input_pdb)

    fixer = PDBFixer(str(input_pdb))
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()

    with open(output_pdb, "w") as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)


def reorder_pdb(structure, targets, new_resname="OHE"):
    """
    Splits atoms matching `targets` out of their original residues and places them
    into newly created residues inserted at the start of each chain.

    For each chain, residues containing atoms whose names match `targets` are processed.
    Those atoms are removed from the original residue and copied into a new residue
    with name `new_resname`. The new residues are then inserted at the beginning of
    the chain to preserve ordering in the resulting structure.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        Input structure containing chains, residues, and atoms.
    targets : iterable of str
        Atom names to extract and move into new residues.
    new_resname : str, optional
        Residue name assigned to newly created residues (default is "OHE").

    Returns
    -------
    structure
        Reordered structure; structure is modified in place.
    """

    for chain in structure.get_chains():
        inserts = []

        for res in list(chain):
            move = [atom for atom in list(res) if atom.name in targets]
            if not move:
                continue

            res_copy = Residue((" ", res.id[1] - 1, " "), new_resname, res.segid)

            for atom in move:
                res_copy.add(atom.copy())
                res.detach_child(atom.id)

            inserts.append(res_copy)

        for res in reversed(inserts):
            chain.child_list.insert(0, res)
    return structure


def write_reorderd_pdb(input_pdb, output_pdb, targets):
    """
    Write the modified structure to a PDB file.

    Parameters
    ----------
    input_pdb : str
        Input PDB filename.
    output_pdb : str or Path
        Output PDB filename.

    Returns
    -------
    None
    """

    structure = load_pdb(input_pdb)
    structure = reorder_pdb(structure, targets, new_resname="OHE")

    save_pdb(structure, output_pdb)
    return structure


def get_op_and_p_indices(structure, targets):
    """
    Extract atom serial numbers for target atoms ("op_idx") and corresponding
    phosphate ("P") atoms in the next residue ("p_idx").

    For each residue in each chain, if the residue contains any atom whose
    name matches `targets`, all matching atom serial numbers are collected.


    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        Parsed structure containing chains, residues, and atoms.
    targets : iterable of str
        Atom names to search for within each residue.

    Returns
    -------
    op_idx : list of int
        Serial numbers of atoms in residues containing target atom types.
    p_idx : list of int
        Serial numbers of "P" atoms in the subsequent residues.
    """
    op_idx = []
    p_idx = []

    for chain in structure.get_chains():
        residues = list(chain)

        for i, res in enumerate(residues):
            if any(atom.name in targets for atom in res):
                op_idx.extend(
                    [atom.get_serial_number() for atom in res if atom.name in targets]
                )

                nxt = residues[i + 1]

                p_idx.append(
                    next(atom.get_serial_number() for atom in nxt if atom.name == "P")
                )

    return op_idx, p_idx


def write_pdb_with_connect(pdb_file, output_pdb, targets):
    """
    Write a PDB file with additional CONECT records linking terminal phosphate atoms.

    Atom serial numbers are obtained from the provided structure using
    `get_op_and_p_indices()`. For each target residue, two CONECT records are
    inserted immediately before the END record:
        OP3 -- HOP3
        OP3 -- P

    Parameters
    ----------
    fixed_file : str or Path
        Input PDB file to copy and augment.
    output_pdb : str or Path
        Output PDB file containing the added CONECT records.
    structure : Bio.PDB.Structure.Structure
        Structure corresponding to `fixed_file`, used to determine atom
        serial numbers.
    targets : iterable
        Residue identifiers passed to `get_op_and_p_indices()`.

    Returns
    -------
    None
    """
    structure = load_pdb(pdb_file)

    op_idx, p_idx = get_op_and_p_indices(structure, targets)

    with open(pdb_file) as fin, open(output_pdb, "w") as fout:
        for line in fin:
            if line.startswith("END"):
                for p, op3, hop3 in zip(p_idx, op_idx[::2], op_idx[1::2]):
                    fout.write(f"CONECT{op3:5d}{hop3:5d}\n")
                    fout.write(f"CONECT{op3:5d}{p:5d}\n")
            fout.write(line)
