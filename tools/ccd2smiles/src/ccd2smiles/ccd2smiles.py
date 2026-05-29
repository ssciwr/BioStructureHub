#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ccd2smiles.py

A tiny helper for converting RCSB CCD identifiers (e.g. "BNZ", "ATP", "HEM")
to their canonical SMILES strings.

Example
-------
>>> from ccd2smiles import ccd_to_smiles
>>> ccd_to_smiles("BNZ")
'c1ccccc1'

Command line example
--------------------
$ ccd2smiles BNZ
c1ccccc1

"""

from __future__ import annotations
import sys
from functools import lru_cache
from typing import Optional

import requests


# ----------------------------------------------------------------------
# Low‑level fetch – memoised with an LRU cache (default size 1024)
# ----------------------------------------------------------------------
@lru_cache(maxsize=1024)
def _fetch_smiles(ccd_id: str) -> Optional[str]:
    """
    Query the RCSB REST API for *ccd_id* and return the canonical SMILES.

    Returns ``None`` if the request fails, the entry has no SMILES,
    or the identifier does not exist.
    """
    url = f"https://data.rcsb.org/rest/v1/core/chemcomp/{ccd_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        _fetch_smiles.cache_clear()
        return None

    # The SMILES field is stored under:
    # payload["rcsb_chem_comp_descriptor"]["SMILES_stereo"]
    # Do not confuse with ["pdbx_chem_comp_desciptor"]
    desc = payload.get("rcsb_chem_comp_descriptor", {})
    smiles = desc.get("SMILES_stereo") or desc.get("SMILES")
    if smiles:
        smiles = smiles.strip()
    else:
        _fetch_smiles.cache_clear()
    return smiles


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def ccd_to_smiles(
    ccd_id: str,
    *,
    refresh: bool = False,
) -> Optional[str]:
    """
    Translate a CCD identifier into SMILES strings.

    Parameters
    ----------
    ccd_id  : str
        Three‑letter CCD codes (e.g. "ATP").
    refresh : bool, default=False
        If True, force a fresh download from the RCSB server even for
        identifiers already cached in the current Python session.

    Returns
    -------
    Optional[str]
        Mapping ``ccd_id -> smiles``.  If a component has no SMILES entry
        the value will be ``None``.
    """
    # Normalise input (upper‑case, strip whitespace)
    ccd = ccd_id.strip().upper()

    if refresh:
        _fetch_smiles.cache_clear()

    return _fetch_smiles(ccd)


def main():
    if len(sys.argv) != 2:
        print("Usage: ccd2smiles <CCD_ID>")
        sys.exit(1)

    print(ccd_to_smiles(sys.argv[1]))


if __name__ == "__main__":
    main()
