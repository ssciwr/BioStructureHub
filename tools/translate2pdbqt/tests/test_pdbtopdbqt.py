from translate2pdbqt import pdb_to_pdbqt


def test_pdb_to_pdbqt_returns_existing_output(tmp_path):
    pdb_file = tmp_path / "input.pdb"
    pdbqt_file = tmp_path / "output.pdbqt"

    pdb_file.write_text("dummy pdb content")
    pdbqt_file.write_text("existing pdbqt content")

    result = pdb_to_pdbqt(str(pdb_file), str(pdbqt_file))

    assert result == str(pdbqt_file)
    assert pdbqt_file.read_text() == "existing pdbqt content"


def test_pdb_to_pdbqt_converts_file(tmp_path):
    pdb_file = tmp_path / "input.pdb"
    pdbqt_file = tmp_path / "output.pdbqt"

    pdb_file.write_text(
        """\
ATOM      1  O   HOH A   1      10.000  10.000  10.000  1.00 20.00           O
ATOM      2  H1  HOH A   1      10.500  10.000  10.000  1.00 20.00           H
ATOM      3  H2  HOH A   1       9.500  10.000  10.000  1.00 20.00           H
END
"""
    )

    result = pdb_to_pdbqt(str(pdb_file), str(pdbqt_file))

    assert result == str(pdbqt_file)
    assert pdbqt_file.exists()
    assert pdbqt_file.stat().st_size > 0

    content = pdbqt_file.read_text()

    assert "ROOT" not in content
    assert "ENDROOT" not in content
    assert "BRANCH" not in content
    assert "ENDBRANCH" not in content
    assert "TORSDOF" not in content
