# __main__.py

import argparse
from pathlib import Path

from .RNAprep import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run the PDB preparation pipeline.")
    parser.add_argument("basename", help="Base name of the input structure.")

    args = parser.parse_args()

    basename = Path(args.basename)
    if basename.name != args.basename:
        parser.error("basename must not contain path separators")

    run_pipeline(basename.name)


if __name__ == "__main__":
    main()
