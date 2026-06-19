from Bio.PDB import PDBParser, PDBIO


def load_pdb(input_pdb):
    parser = PDBParser(QUIET=True)
    return parser.get_structure("x", input_pdb)


def save_pdb(structure, output_pdb):
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb)
