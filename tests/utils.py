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
        text = re.sub(
            rf"(?:[A-Za-z]:)?[\\/][^ \n]*?\b({re.escape(marker)})\b([\\/][^\s]*)?",
            r"\1\2",
            text,
        )
    return text.replace("\\", "/")


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
    Copy reference results to the destination directory.
    Creates or overwrites the destination so that analysis notebooks can read it.
    """
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)

    if not dst.exists():
        raise RuntimeError(f"Failed to create {dst}")
