import pytest
import requests

from ccd2smiles import ccd_to_smiles
from ccd2smiles.ccd2smiles import _fetch_smiles


@pytest.fixture(autouse=True)
def clear_cache():
    _fetch_smiles.cache_clear()


def test_fetch_smiles_success(monkeypatch):
    """
    Test that SMILES_stereo is correctly extracted from a valid RCSB response.
    """

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"rcsb_chem_comp_descriptor": {"SMILES_stereo": "c1ccccc1"}}

    monkeypatch.setattr(
        "ccd2smiles.ccd2smiles.requests.get", lambda *a, **k: FakeResponse()
    )

    assert _fetch_smiles("BNZ") == "c1ccccc1"


def test_fetch_smiles_fallback(monkeypatch):
    """
    Test that SMILES is used when SMILES_stereo is not present in the response.
    """

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"rcsb_chem_comp_descriptor": {"SMILES": "CCO"}}

    monkeypatch.setattr(
        "ccd2smiles.ccd2smiles.requests.get", lambda *a, **k: FakeResponse()
    )

    assert _fetch_smiles("ETH") == "CCO"


def test_fetch_smiles_missing(monkeypatch):
    """
    Test that None is returned when no SMILES data is available in the response.
    """

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {}

    monkeypatch.setattr(
        "ccd2smiles.ccd2smiles.requests.get", lambda *args, **kwargs: FakeResponse()
    )

    assert _fetch_smiles("XXX") is None


def test_fetch_smiles_request_error(monkeypatch):
    """
    Test that None is returned when the RCSB request raises a RequestException.
    """

    def raise_error(*args, **kwargs):
        raise requests.RequestException("network error")

    monkeypatch.setattr("ccd2smiles.ccd2smiles.requests.get", raise_error)

    assert _fetch_smiles("BNZ") is None


def test_ccd_to_smiles_integration(monkeypatch):
    """
    Test public API: verifies input normalization and correct delegation
    to the internal _fetch_smiles function.
    """

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"rcsb_chem_comp_descriptor": {"SMILES_stereo": "c1ccccc1"}}

    monkeypatch.setattr(
        "ccd2smiles.ccd2smiles.requests.get", lambda *a, **k: FakeResponse()
    )

    assert ccd_to_smiles(" bnz ") == "c1ccccc1"


def test_ccd_to_smiles_caching(monkeypatch):
    """
    Test that repeated calls to ccd_to_smiles with equivalent inputs
    only trigger a single underlying HTTP request due to LRU caching
    in _fetch_smiles.
    """
    calls = {"n": 0}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"rcsb_chem_comp_descriptor": {"SMILES_stereo": "c1ccccc1"}}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return FakeResponse()

    monkeypatch.setattr("ccd2smiles.ccd2smiles.requests.get", fake_get)

    ccd_to_smiles(" bnz ")
    ccd_to_smiles(" bnz ")

    assert calls["n"] == 1
