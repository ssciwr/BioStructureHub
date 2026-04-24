
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz

export PATH="/mnt/sds-hd/sd25g005/boltz/localcolabfold/colabfold-conda/bin:$PATH"

colabfold_search  \
    --db-load-mode 2 \
    --threads 96 \
    --use-env 0 \
    --gpu 1 \
    "/home/hd/hd_hd/hd_aq354/boltz_test/insulin.fasta" \
    "/mnt/sds-hd/sd25g005/boltz/localcolabfold" \
    "/home/hd/hd_hd/hd_aq354/boltz_test" \
