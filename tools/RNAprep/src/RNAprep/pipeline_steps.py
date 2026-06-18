from pdbfixer import PDBFixer
from Bio.PDB.Residue import Residue
from openmm import unit
from openmm.app import PDBFile
from pathlib import Path
import subprocess
from .pdb_io import load_pdb, save_pdb
import numpy as np


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

rna = loadpdb {basename}_protein_00.pdb
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


def remove_op3(input_pdb, output_pdb):
    """
    Remove the terminal phosphate oxygen atom ("OP3") from the first residue
    of each chain in a PDB structure (if it contains OP3) and write the modified
    structure to a new PDB file.

    Parameters
    ----------
    input_pdb : str
        Path to the input PDB file.
    output_pdb : str
        Path where the modified PDB file will be written.

    Returns
    -------
    str
        The path to the output PDB file.

    Notes
    -----
    The OP3 atom is typically present on a 5'-terminal phosphate group in
    nucleic acid structures. Removing it is neccessary for AlphaFold structures
    that feature a distorted PO4 geometry.
    """
    structure = load_pdb(input_pdb)

    for chain in structure.get_chains():
        residues = list(chain.get_residues())
        first_residue = residues[0]

        if first_residue.has_id("OP3"):
            first_residue.detach_child("OP3")

    save_pdb(structure, output_pdb)


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

            for atom in reversed(move):
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
                for p, op3, hop3 in zip(p_idx, op_idx[1::2], op_idx[::2]):
                    fout.write(f"CONECT{op3:5d}{hop3:5d}\n")
                    fout.write(f"CONECT{op3:5d}{p:5d}\n")
            fout.write(line)


def fix_phosphate_pdb(infile, outfile, thresh=2):
    """
    Fix overlapping OP3/OP1(OP2) phosphate geometry for chains beginning with OHE.

    Parameters
    ----------
    infile : str
        Input PDB path.
    outfile : str
        Output PDB path.
    thresh : float
        Distance threshold in Å.
    keep_ids : bool
        Passed to PDBFile.writeFile().
    write_conects : bool
        If False, suppress CONECT records.
    """

    # keep connect records from original file
    with open(infile) as f:
        original_conect = [line for line in f if line.startswith("CONECT")]

    # read positions and topology with OpenMM
    pdb = PDBFile(infile)
    pos = pdb.positions

    # helper to get atom index by name in a residue
    def idx(res, name):
        for atom in res.atoms():
            if atom.name == name:
                return atom.index
        return None

    # helper to compute distance between two atoms by index
    def d(i, j):
        v = pos[j] - pos[i]
        return np.linalg.norm(v.value_in_unit(unit.nanometer)) * 10.0  # in Angstrom

    for chain in pdb.topology.chains():
        # find nucleotide chains that start with OHE
        residues = list(chain.residues())
        r1, r2 = residues[0], residues[1]

        if not (r1.name == "OHE"):
            continue

        # get atom indices for OHE and adjacent residue
        P = idx(r2, "P")
        OP1 = idx(r2, "OP1")
        OP2 = idx(r2, "OP2")
        OP3 = idx(r1, "OP3")
        O5 = idx(r2, "O5'")

        # find if there is something to fix
        if min(d(OP1, OP3), d(OP2, OP3)) >= thresh:
            continue

        p = pos[P]
        o5 = pos[O5]
        op3 = pos[OP3]

        u = o5 - p
        u /= np.linalg.norm(u)

        tmp = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(tmp, u)) > 0.9:
            tmp = np.array([0.0, 1.0, 0.0])

        e1 = np.cross(u, tmp)
        e1 /= np.linalg.norm(e1)

        e2 = np.cross(u, e1)
        e2 /= np.linalg.norm(e2)

        # do not move op3, to not move H
        op3_dir = op3 - p
        op3_dir /= np.linalg.norm(op3_dir)

        theta = np.arccos(-1.0 / 3.0)

        r = 0.15 * unit.nanometer

        oxygens = []
        for phi in (0.0, 2 * np.pi / 3, 4 * np.pi / 3):
            v = np.cos(theta) * u + np.sin(theta) * (
                np.cos(phi) * e1 + np.sin(phi) * e2
            )
            oxygens.append(v)

        oxygens.sort(key=lambda v: np.dot(v, op3_dir))

        pos[OP1] = p + r * oxygens[0]
        pos[OP2] = p + r * oxygens[1]

    with open(outfile, "w") as f:
        PDBFile.writeFile(pdb.topology, pos, f)

    # remove OpenMM-generated CONECT records and restore originals
    with open(outfile) as f:
        lines = [line for line in f if not line.startswith("CONECT")]

    with open(outfile, "w") as f:
        f.writelines(lines)
        f.writelines(original_conect)
