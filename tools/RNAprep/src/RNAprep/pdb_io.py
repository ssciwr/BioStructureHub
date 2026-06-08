from Bio.PDB import PDBParser, PDBIO


def load_pdb(pdb_file):
    parser = PDBParser(QUIET=True)
    return parser.get_structure("x", pdb_file)


def save_pdb(structure, file_name):
    io = PDBIO()
    io.set_structure(structure)
    io.save(file_name)
