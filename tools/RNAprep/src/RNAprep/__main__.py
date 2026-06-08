# __main__.py

import argparse

from .RNAprep import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run the PDB preparation pipeline.")
    parser.add_argument("basename", help="Base name of the input structure.")

    args = parser.parse_args()

    run_pipeline(args.basename)


if __name__ == "__main__":
    main()
