
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltzgen


boltzgen run /home/hd/hd_hd/hd_aq354/protein_design_w_Boltzgen/input.yaml  \
  --output /home/hd/hd_hd/hd_aq354/protein_design_w_Boltzgen/workbench/test_run  \
  --protocol protein-anything \
  --num_designs 10  \
  --budget 2 \
