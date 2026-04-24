# Environment Specifications

This directory contains the environment specifications used for the tutorials in this repository.
Each environment is defined by an environment.yml file that describes the intended software stack.

These environments are primarily for the bwForCluster Helix HPC system (accessed via bwVisu) and may include a mix of conda and pip packages.

## Creating an environment

Create an environment from a specification:

    conda env create -f boltz.environment.yml

Activate the environment:

    conda activate boltz

## Notes on reproducibility

These files describe the software requirements, but they are not lock files.
Exact package versions resolved by the solver may vary depending on:

- operating system

- HPC cluster configuration

- CUDA or system libraries

- available package builds

## Notes on Boltz

Note that Boltz requires [mmseqs2](https://github.com/soedinglab/MMseqs2) and [colabfold](https://github.com/YoshitakaMo/localcolabfold) to be installed. Helpful issues: 
-  [https://github.com/jwohlwend/boltz/issues/333#issuecomment-2963120545](https://github.com/jwohlwend/boltz/issues/333#issuecomment-2963120545)
-  [https://github.com/soedinglab/MMseqs2/issues/588](https://github.com/soedinglab/MMseqs2/issues/588)