# tests/utils.py
import re
import yaml
from typing import Any, Dict
import shutil
from pathlib import Path


# -------------------------------
# Text-based normalization
# -------------------------------
def normalize_text_paths(text: str, markers: list[str]) -> str:
    """
    Normalize absolute paths in text files:
    - Strips everything before the full marker
    - Handles multiple markers and multiple occurrences per line
    - Handles Linux absolute paths (/home/...) and Windows absolute paths (C:\...)
    """
    for marker in markers:
        # does not work on windows due to drive letters in github runner
        # text = re.sub(rf"/[^ \n]*?\b({re.escape(marker)})\b(/?)", r"\1\2", text)
        # try
        text = re.sub(
            rf"(?:[A-Za-z]:)?[\\/][^ \n]*?\b({re.escape(marker)})\b([\\/][^\s]*)?",
            r"\1\2",
            text,
        )
    return text.replace("\\", "/")


# -------------------------------
# YAML normalization
# -------------------------------
def normalize_msa_paths(yaml_dict: Dict[str, Any], marker: str) -> Dict[str, Any]:
    """
    Strip absolute prefixes from msa fields only.
    """
    for seq in yaml_dict.get("sequences", []):
        protein = seq.get("protein", {})
        msa = protein.get("msa")
        if msa and marker in msa:
            protein["msa"] = marker + msa.split(marker, 1)[-1]
    return yaml_dict


# -------------------------------
# Helper functions for loading files
# -------------------------------
def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -------------------------------
# Helper functions for copying files
# -------------------------------
def prepare_results(src: Path, dst: Path) -> None:
    """
    Copy reference Boltz results to the destination directory.
    Creates or overwrites the destination so that analysis notebooks can read it.
    """
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)

    if not dst.exists():
        raise RuntimeError(f"Failed to create {dst}")
