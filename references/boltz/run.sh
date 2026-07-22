
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz

boltz predict  /home/hd/hd_hd/hd_aq354/boltz_test/insulin.yaml  \
    --write_full_pae \
    --out_dir /home/hd/hd_hd/hd_aq354/boltz_test
