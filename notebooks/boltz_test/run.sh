
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz


boltz predict  /home/christine/Sandbox/BioStructureHub/notebooks/boltz_test/input_file.yaml  \
    --write_full_pae \
    --out_dir /home/christine/Sandbox/BioStructureHub/notebooks/boltz_test
