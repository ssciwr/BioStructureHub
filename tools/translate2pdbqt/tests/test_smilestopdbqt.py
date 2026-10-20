from translate2pdbqt import smiles_to_pdbqt


def test_smiles_to_pdbqt_existing_output(tmp_path):
    pdbqt_file = tmp_path / "output.pdbqt"

    pdbqt_file.write_text("existing pdbqt content")

    result = smiles_to_pdbqt("CCO", pdbqt_file)

    assert result == pdbqt_file
    assert pdbqt_file.read_text() == "existing pdbqt content"


def test_smiles_to_pdbqt_conversion(tmp_path):
    pdbqt_file = tmp_path / "output.pdbqt"

    result = smiles_to_pdbqt("CCO", pdbqt_file)

    assert result == pdbqt_file
    assert pdbqt_file.exists()
    assert pdbqt_file.stat().st_size > 0

    content = pdbqt_file.read_text()

    assert "ATOM" in content or "HETATM" in content
