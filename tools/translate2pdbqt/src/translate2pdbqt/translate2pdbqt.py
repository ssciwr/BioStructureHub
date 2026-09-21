"""
translate2pdbqt.py

A tiny helper to convert PDB, CIF, and SMILES to PDBQT.

"""

from openbabel import pybel

# pybel.ob.obErrorLog.SetOutputLevel(0)


def pdb_to_pdbqt(pdb_file, pdbqt_file):
    """Convert a PDB file to PDBQT using Pybel and Gasteiger charges.

    Parameters
    ----------
    pdb_file : str
        Path to the input PDB file.
    pdbqt_file : str
        Path to the output PDBQT file.
    """

    ## TODO check if outputfile exists
    mol = next(pybel.readfile("pdb", pdb_file))
    mol.addh()
    mol.calccharges(model="gasteiger")
    mol.write("pdbqt", pdbqt_file, overwrite=True, opt={"rigid": None})

    with open(pdbqt_file) as f:
        lines = f.readlines()

    with open(pdbqt_file, "w") as f:
        f.writelines(
            line
            for line in lines
            if not line.startswith(
                ("ROOT", "ENDROOT", "BRANCH", "ENDBRANCH", "TORSDOF")
            )
        )

    return pdbqt_file


def cif_to_pdbqt(cif_file, pdbqt_file):
    """Convert a CIF file to PDBQT using Pybel and Gasteiger charges.

    Parameters
    ----------
    cif_file : str
        Path to the input CIF file.
    pdbqt_file : str
        Path to the output PDBQT file.
    """
    ## TODO check if outputfile exists
    mol = next(pybel.readfile("cif", cif_file))
    mol.addh()
    mol.calccharges(model="gasteiger")
    mol.write("pdbqt", pdbqt_file, overwrite=True, opt={"rigid": None})

    with open(pdbqt_file) as f:
        lines = f.readlines()

    with open(pdbqt_file, "w") as f:
        f.writelines(
            line
            for line in lines
            if not line.startswith(
                ("ROOT", "ENDROOT", "BRANCH", "ENDBRANCH", "TORSDOF")
            )
        )

    return pdbqt_file


def smiles_to_pdbqt(smiles, pdbqt_file, pH=7.4):
    """
    Convert a SMILES string to a PDBQT file using mmff94s.
    Note that it appends molecules into one PDBQT file if used in a list comprehension,
    but will overwrite the PDBQT file each time if used in a loop.
    https://projects.volkamerlab.org/teachopencadd/talktorials/T015_protein_ligand_docking.html

    Parameters
    ----------
    smiles: str
        SMILES string.
    pdbqt_path: str or pathlib.path
        Path to output PDBQT file.
    pH: float
        Protonation at given pH.
    """
    molecule = pybel.readstring("smi", smiles)
    # add hydrogens at given pH
    molecule.OBMol.CorrectForPH(pH)
    molecule.addh()
    # generate 3D coordinates
    molecule.make3D(forcefield="mmff94s", steps=10000)
    # add partial charges to each atom
    for atom in molecule.atoms:
        atom.OBAtom.GetPartialCharge()
    molecule.write("pdbqt", str(pdbqt_file), overwrite=True)
    return pdbqt_file
