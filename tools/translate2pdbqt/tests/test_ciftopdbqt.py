from translate2pdbqt import cif_to_pdbqt


def test_cif_to_pdbqt_existing_output(tmp_path):
    cif_file = tmp_path / "input.cif"
    pdbqt_file = tmp_path / "output.pdbqt"

    cif_file.write_text("dummy cif content")
    pdbqt_file.write_text("existing pdbqt content")

    result = cif_to_pdbqt(str(cif_file), str(pdbqt_file))

    assert result == str(pdbqt_file)
    assert pdbqt_file.read_text() == "existing pdbqt content"


def test_cif_to_pdbqt_conversion(tmp_path):
    cif_file = tmp_path / "input.cif"
    pdbqt_file = tmp_path / "output.pdbqt"

    cif_file.write_text(
        """\
data_water
_cell_length_a    10.0
_cell_length_b    10.0
_cell_length_c    10.0
_cell_angle_alpha 90
_cell_angle_beta  90
_cell_angle_gamma 90

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
O1 O  0.500 0.500 0.500
H1 H  0.550 0.500 0.500
H2 H  0.450 0.500 0.500
"""
    )

    result = cif_to_pdbqt(str(cif_file), str(pdbqt_file))

    assert result == str(pdbqt_file)
    assert pdbqt_file.exists()
    assert pdbqt_file.stat().st_size > 0

    content = pdbqt_file.read_text()

    assert "ROOT" not in content
    assert "ENDROOT" not in content
    assert "BRANCH" not in content
    assert "ENDBRANCH" not in content
    assert "TORSDOF" not in content
